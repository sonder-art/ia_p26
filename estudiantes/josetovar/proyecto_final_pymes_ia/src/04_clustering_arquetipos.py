import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from utils import (
    DATA_PROCESSED,
    MODEL_FEATURES,
    OUTPUTS,
    PROFILE_COLUMNS,
    RANDOM_STATE,
    ensure_directories,
    read_csv,
    require_columns,
    save_dataframe,
    save_plot,
)


ARCHETYPE_ORDER = [
    "Dependiente de crédito",
    "Operador estacional",
    "Comerciante intensivo",
    "Negocio digital",
    "Profesionista independiente",
]


def _zscore_profiles(profiles):
    numeric = profiles.select_dtypes(include=[np.number])
    std = numeric.std(ddof=0).replace(0, 1)
    return (numeric - numeric.mean()) / std


def asignar_arquetipos(profiles):
    z = _zscore_profiles(profiles)
    reglas = {
        "Dependiente de crédito": z[["uso_credito", "revolvencia", "exposicion_credito"]].mean(axis=1),
        "Operador estacional": z["estacionalidad"],
        "Comerciante intensivo": z[
            ["num_transacciones", "gasto_total", "ingresos_totales", "pagos_recurrentes"]
        ].mean(axis=1),
        "Negocio digital": z[
            ["num_comercios_distintos", "num_categorias_distintas", "depositos_recurrentes"]
        ].mean(axis=1),
        "Profesionista independiente": z[
            ["ticket_promedio", "ticket_mediano", "ratio_ingreso_gasto"]
        ].mean(axis=1),
    }

    disponibles = set(profiles.index)
    asignaciones = {}
    for arquetipo in ARCHETYPE_ORDER:
        if not disponibles:
            break
        candidato = reglas[arquetipo].loc[list(disponibles)].idxmax()
        asignaciones[candidato] = arquetipo
        disponibles.remove(candidato)
    return asignaciones


def graficar_scores(df):
    umbral = df["score_empresarial"].quantile(0.90)
    plt.figure(figsize=(9, 5))
    sns.histplot(df["score_empresarial"], bins=35, color="#457B9D", edgecolor="white")
    plt.axvline(umbral, color="#E76F51", linestyle="--", linewidth=2, label="Percentil 90")
    plt.title("Distribucion de scores de similitud empresarial")
    plt.xlabel("Score empresarial")
    plt.ylabel("Numero de clientes personales")
    plt.legend()
    save_plot(OUTPUTS / "distribucion_scores.png")


def graficar_pca(seleccionados):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=seleccionados,
        x="pca_1",
        y="pca_2",
        hue="arquetipo",
        palette="Set2",
        s=56,
        edgecolor="white",
        linewidth=0.4,
    )
    plt.title("Clientes seleccionados: visualizacion PCA")
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")
    plt.legend(title="Arquetipo", bbox_to_anchor=(1.02, 1), loc="upper left")
    save_plot(OUTPUTS / "clusters_pca.png")


def graficar_perfiles(resumen):
    variables = [
        "score_promedio",
        "num_transacciones_promedio",
        "gasto_total_promedio",
        "ingresos_totales_promedio",
        "pagos_recurrentes_promedio",
        "depositos_recurrentes_promedio",
        "uso_credito_promedio",
        "estacionalidad_promedio",
    ]
    matriz = resumen.set_index("arquetipo")[variables]
    matriz_norm = (matriz - matriz.min()) / (matriz.max() - matriz.min()).replace(0, 1)
    plt.figure(figsize=(10, 5.5))
    sns.heatmap(matriz_norm, annot=True, fmt=".2f", cmap="viridis", cbar_kws={"label": "Valor normalizado"})
    plt.title("Perfil comparativo de arquetipos")
    plt.xlabel("")
    plt.ylabel("")
    save_plot(OUTPUTS / "perfil_arquetipos.png")


def main():
    ensure_directories()
    df = read_csv(DATA_PROCESSED / "clientes_personales_scoreados.csv")
    require_columns(df, ["cliente_id", "score_empresarial", "seleccionado", *MODEL_FEATURES], df.name if hasattr(df, "name") else "scoreados")

    seleccionados = df[df["seleccionado"] == True].copy()
    if seleccionados.empty:
        raise ValueError("No hay clientes seleccionados para segmentar.")

    x = seleccionados[MODEL_FEATURES]
    x_scaled = StandardScaler().fit_transform(x)
    k = min(5, len(seleccionados))
    if k < 2:
        seleccionados["cluster"] = 0
        seleccionados["pca_1"] = 0.0
        seleccionados["pca_2"] = 0.0
    else:
        pca = PCA(n_components=2, random_state=RANDOM_STATE)
        componentes = pca.fit_transform(x_scaled)
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=25)
        seleccionados["cluster"] = kmeans.fit_predict(x_scaled)
        seleccionados["pca_1"] = componentes[:, 0]
        seleccionados["pca_2"] = componentes[:, 1]

    perfiles_cluster = seleccionados.groupby("cluster")[MODEL_FEATURES].mean()
    asignaciones = asignar_arquetipos(perfiles_cluster)
    seleccionados["arquetipo"] = seleccionados["cluster"].map(asignaciones)

    df.loc[seleccionados.index, "cluster"] = seleccionados["cluster"].astype(int)
    df.loc[seleccionados.index, "arquetipo"] = seleccionados["arquetipo"]
    df.loc[~df["seleccionado"], "arquetipo"] = "No seleccionado"

    resumen = (
        seleccionados.groupby("arquetipo")
        .agg(
            numero_clientes=("cliente_id", "count"),
            score_promedio=("score_empresarial", "mean"),
            num_transacciones_promedio=("num_transacciones", "mean"),
            dias_activos_promedio=("dias_activos", "mean"),
            gasto_total_promedio=("gasto_total", "mean"),
            ingresos_totales_promedio=("ingresos_totales", "mean"),
            ticket_promedio_promedio=("ticket_promedio", "mean"),
            num_comercios_distintos_promedio=("num_comercios_distintos", "mean"),
            num_categorias_distintas_promedio=("num_categorias_distintas", "mean"),
            pagos_recurrentes_promedio=("pagos_recurrentes", "mean"),
            depositos_recurrentes_promedio=("depositos_recurrentes", "mean"),
            uso_credito_promedio=("uso_credito", "mean"),
            revolvencia_promedio=("revolvencia", "mean"),
            concentracion_proveedores_promedio=("concentracion_proveedores", "mean"),
            estacionalidad_promedio=("estacionalidad", "mean"),
        )
        .reset_index()
        .sort_values("numero_clientes", ascending=False)
    )
    resumen = resumen.round(4)

    save_dataframe(df, DATA_PROCESSED / "clientes_personales_scoreados.csv")
    save_dataframe(resumen, DATA_PROCESSED / "resumen_arquetipos.csv")
    graficar_scores(df)
    graficar_pca(seleccionados)
    graficar_perfiles(resumen)


if __name__ == "__main__":
    main()
