import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from utils import (
    DATA_PROCESSED,
    MODEL_FEATURES,
    OUTPUTS,
    RANDOM_STATE,
    ensure_directories,
    read_csv,
    require_columns,
    save_dataframe,
    save_plot,
)


def entrenar_isolation_forest(empresariales):
    scaler = StandardScaler()
    x_emp = scaler.fit_transform(empresariales[MODEL_FEATURES])
    modelo = IsolationForest(
        n_estimators=300,
        contamination="auto",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    modelo.fit(x_emp)
    return modelo, scaler


def calcular_score(modelo, scaler, personales):
    x_personal = scaler.transform(personales[MODEL_FEATURES])
    decision = modelo.decision_function(x_personal).reshape(-1, 1)
    score = MinMaxScaler(feature_range=(0, 1)).fit_transform(decision).ravel()
    return score.round(6)


def importancia_random_forest(empresariales, personales):
    datos = pd.concat(
        [
            empresariales.assign(objetivo_empresarial=1),
            personales.assign(objetivo_empresarial=0),
        ],
        ignore_index=True,
    )
    x = datos[MODEL_FEATURES]
    y = datos["objetivo_empresarial"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )
    modelo = RandomForestClassifier(
        n_estimators=350,
        max_depth=9,
        min_samples_leaf=8,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    modelo.fit(x_train, y_train)
    importancias = pd.DataFrame(
        {
            "variable": MODEL_FEATURES,
            "importancia": modelo.feature_importances_,
        }
    ).sort_values("importancia", ascending=False)
    importancias["accuracy_validacion"] = modelo.score(x_test, y_test)
    return importancias


def graficar_importancias(importancias):
    top = importancias.head(14).sort_values("importancia", ascending=True)
    plt.figure(figsize=(9, 6))
    sns.barplot(data=top, x="importancia", y="variable", color="#2A9D8F")
    plt.title("Importancia aproximada de variables")
    plt.xlabel("Importancia Random Forest auxiliar")
    plt.ylabel("")
    save_plot(OUTPUTS / "importancia_variables.png")


def main():
    ensure_directories()
    empresariales = read_csv(DATA_PROCESSED / "clientes_empresariales_features.csv")
    personales = read_csv(DATA_PROCESSED / "clientes_personales_features.csv")
    require_columns(empresariales, MODEL_FEATURES, "clientes_empresariales_features.csv")
    require_columns(personales, MODEL_FEATURES, "clientes_personales_features.csv")

    modelo, scaler = entrenar_isolation_forest(empresariales)
    personales_scoreados = personales.copy()
    personales_scoreados["score_empresarial"] = calcular_score(modelo, scaler, personales)
    umbral = personales_scoreados["score_empresarial"].quantile(0.90)
    personales_scoreados["seleccionado"] = personales_scoreados["score_empresarial"] >= umbral
    personales_scoreados["cluster"] = pd.NA
    personales_scoreados["arquetipo"] = "No seleccionado"

    columnas_salida = [
        "cliente_id",
        "tipo_cliente",
        "score_empresarial",
        "seleccionado",
        "cluster",
        "arquetipo",
        *MODEL_FEATURES,
    ]
    if "perfil_sintetico" in personales_scoreados.columns:
        columnas_salida.append("perfil_sintetico")

    save_dataframe(
        personales_scoreados[columnas_salida],
        DATA_PROCESSED / "clientes_personales_scoreados.csv",
    )

    importancias = importancia_random_forest(empresariales, personales)
    save_dataframe(importancias, DATA_PROCESSED / "importancia_variables.csv")
    graficar_importancias(importancias)
    print(f"Umbral percentil 90 del score empresarial: {umbral:.4f}")


if __name__ == "__main__":
    main()
