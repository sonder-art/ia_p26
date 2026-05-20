from pathlib import Path

import pandas as pd

from utils import DATA_PROCESSED, OUTPUTS, PROJECT_ROOT


ARCHIVOS_ESPERADOS = [
    DATA_PROCESSED / "clientes_empresariales_features.csv",
    DATA_PROCESSED / "clientes_personales_features.csv",
    DATA_PROCESSED / "clientes_personales_scoreados.csv",
    DATA_PROCESSED / "resumen_arquetipos.csv",
    OUTPUTS / "distribucion_scores.png",
    OUTPUTS / "clusters_pca.png",
    OUTPUTS / "importancia_variables.png",
    OUTPUTS / "perfil_arquetipos.png",
]


def validar_archivos(paths: list[Path]) -> None:
    faltantes = [path for path in paths if not path.exists() or path.stat().st_size == 0]
    if faltantes:
        faltantes_txt = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in faltantes)
        raise FileNotFoundError(f"Faltan archivos esperados o estan vacios: {faltantes_txt}")


def main():
    validar_archivos(ARCHIVOS_ESPERADOS)
    scoreados = pd.read_csv(DATA_PROCESSED / "clientes_personales_scoreados.csv")
    resumen = pd.read_csv(DATA_PROCESSED / "resumen_arquetipos.csv")

    total = len(scoreados)
    seleccionados = int(scoreados["seleccionado"].sum())
    porcentaje = seleccionados / total * 100

    print("Validacion completa del proyecto final.")
    print(f"Clientes personales evaluados: {total}")
    print(f"Clientes seleccionados por percentil 90: {seleccionados} ({porcentaje:.1f}%)")
    print("Resumen de arquetipos:")
    print(resumen[["arquetipo", "numero_clientes", "score_promedio"]].to_string(index=False))


if __name__ == "__main__":
    main()
