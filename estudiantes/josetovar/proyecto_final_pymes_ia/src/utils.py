from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs"

RANDOM_STATE = 42

RAW_COLUMNS = [
    "cliente_id",
    "tipo_cliente",
    "num_transacciones",
    "dias_activos",
    "gasto_total",
    "ingresos_totales",
    "ticket_promedio",
    "ticket_mediano",
    "num_comercios_distintos",
    "num_categorias_distintas",
    "pagos_recurrentes",
    "depositos_recurrentes",
    "porcentaje_tdc",
    "porcentaje_tdd",
    "uso_credito",
    "revolvencia",
    "concentracion_proveedores",
    "estacionalidad",
    "antiguedad_meses",
]

ENGINEERED_COLUMNS = [
    "transacciones_por_dia_activo",
    "gasto_promedio_mensual",
    "ingreso_promedio_mensual",
    "ratio_ingreso_gasto",
    "indice_recurrencia",
    "diversidad_operativa",
    "exposicion_credito",
    "intensidad_operativa",
]

MODEL_FEATURES = [
    "num_transacciones",
    "dias_activos",
    "gasto_total",
    "ingresos_totales",
    "ticket_promedio",
    "ticket_mediano",
    "num_comercios_distintos",
    "num_categorias_distintas",
    "pagos_recurrentes",
    "depositos_recurrentes",
    "porcentaje_tdc",
    "porcentaje_tdd",
    "uso_credito",
    "revolvencia",
    "concentracion_proveedores",
    "estacionalidad",
    "antiguedad_meses",
    *ENGINEERED_COLUMNS,
]

PROFILE_COLUMNS = [
    "score_empresarial",
    "num_transacciones",
    "dias_activos",
    "gasto_total",
    "ingresos_totales",
    "ticket_promedio",
    "num_comercios_distintos",
    "num_categorias_distintas",
    "pagos_recurrentes",
    "depositos_recurrentes",
    "uso_credito",
    "revolvencia",
    "concentracion_proveedores",
    "estacionalidad",
    "indice_recurrencia",
    "diversidad_operativa",
]


def ensure_directories() -> None:
    for directory in (DATA_RAW, DATA_PROCESSED, OUTPUTS):
        directory.mkdir(parents=True, exist_ok=True)


def require_columns(df: pd.DataFrame, columns: list[str], dataset_name: str) -> None:
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise ValueError(f"{dataset_name} no contiene las columnas requeridas: {missing}")


def read_csv(path: Path, required_columns: list[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo esperado: {path.relative_to(PROJECT_ROOT)}")
    df = pd.read_csv(path)
    if required_columns:
        require_columns(df, required_columns, path.name)
    return df


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Archivo generado: {path.relative_to(PROJECT_ROOT)}")


def save_plot(path: Path) -> None:
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Grafica generada: {path.relative_to(PROJECT_ROOT)}")
