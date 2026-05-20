import numpy as np

from utils import (
    DATA_PROCESSED,
    DATA_RAW,
    RAW_COLUMNS,
    ensure_directories,
    read_csv,
    save_dataframe,
)


def construir_features(df):
    features = df.copy()
    features["transacciones_por_dia_activo"] = (
        features["num_transacciones"] / features["dias_activos"].clip(lower=1)
    ).round(4)
    features["gasto_promedio_mensual"] = (
        features["gasto_total"] / features["antiguedad_meses"].clip(lower=1)
    ).round(2)
    features["ingreso_promedio_mensual"] = (
        features["ingresos_totales"] / features["antiguedad_meses"].clip(lower=1)
    ).round(2)
    features["ratio_ingreso_gasto"] = (
        features["ingresos_totales"] / features["gasto_total"].clip(lower=1)
    ).round(4)
    features["indice_recurrencia"] = (
        (features["pagos_recurrentes"] + features["depositos_recurrentes"])
        / features["num_transacciones"].clip(lower=1)
    ).round(4)
    features["diversidad_operativa"] = (
        (features["num_comercios_distintos"] + features["num_categorias_distintas"])
        / features["num_transacciones"].clip(lower=1)
    ).round(4)
    features["exposicion_credito"] = (
        features[["porcentaje_tdc", "uso_credito", "revolvencia"]].mean(axis=1)
    ).round(4)
    features["intensidad_operativa"] = np.log1p(
        features["num_transacciones"] * features["dias_activos"]
    ).round(4)
    return features


def main():
    ensure_directories()
    empresariales = read_csv(DATA_RAW / "clientes_empresariales.csv", RAW_COLUMNS)
    personales = read_csv(DATA_RAW / "clientes_personales.csv", RAW_COLUMNS)

    empresariales_features = construir_features(empresariales)
    personales_features = construir_features(personales)

    save_dataframe(
        empresariales_features,
        DATA_PROCESSED / "clientes_empresariales_features.csv",
    )
    save_dataframe(
        personales_features,
        DATA_PROCESSED / "clientes_personales_features.csv",
    )


if __name__ == "__main__":
    main()
