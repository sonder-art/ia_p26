import numpy as np
import pandas as pd

from utils import DATA_RAW, RAW_COLUMNS, RANDOM_STATE, ensure_directories, save_dataframe


def _clip_round(values, low, high, decimals=0):
    clipped = np.clip(values, low, high)
    return np.round(clipped, decimals)


def _build_clients(rng, n, prefix, tipo_cliente, perfil):
    if perfil == "empresarial":
        transacciones = _clip_round(rng.gamma(6.0, 58, n), 90, 1100)
        dias_activos = _clip_round(rng.normal(245, 55, n), 80, 365)
        comercios = _clip_round(rng.normal(95, 26, n), 30, 210)
        categorias = _clip_round(rng.normal(18, 4, n), 8, 32)
        pagos_rec = _clip_round(transacciones * rng.uniform(0.16, 0.36, n), 10, 260)
        depositos_rec = _clip_round(transacciones * rng.uniform(0.07, 0.21, n), 5, 150)
        ticket_prom = _clip_round(rng.lognormal(7.25, 0.42, n), 420, 5200, 2)
        concentracion = _clip_round(rng.beta(4.0, 3.0, n), 0.18, 0.88, 3)
        estacionalidad = _clip_round(rng.beta(2.0, 5.0, n), 0.03, 0.72, 3)
        antiguedad = _clip_round(rng.normal(55, 27, n), 6, 144)
        pct_tdc = _clip_round(rng.beta(3.2, 3.0, n), 0.08, 0.91, 3)
        uso_credito = _clip_round(rng.beta(2.5, 2.8, n), 0.05, 0.92, 3)
        revolvencia = _clip_round(rng.beta(2.0, 4.0, n), 0.01, 0.78, 3)
    elif perfil == "personal_latente":
        transacciones = _clip_round(rng.gamma(5.0, 48, n), 95, 760)
        dias_activos = _clip_round(rng.normal(205, 45, n), 70, 340)
        comercios = _clip_round(rng.normal(78, 20, n), 24, 165)
        categorias = _clip_round(rng.normal(15, 4, n), 7, 28)
        pagos_rec = _clip_round(transacciones * rng.uniform(0.12, 0.31, n), 7, 190)
        depositos_rec = _clip_round(transacciones * rng.uniform(0.05, 0.18, n), 3, 105)
        ticket_prom = _clip_round(rng.lognormal(7.05, 0.42, n), 360, 4300, 2)
        concentracion = _clip_round(rng.beta(3.0, 4.0, n), 0.11, 0.76, 3)
        estacionalidad = _clip_round(rng.beta(2.2, 4.2, n), 0.04, 0.82, 3)
        antiguedad = _clip_round(rng.normal(43, 24, n), 4, 132)
        pct_tdc = _clip_round(rng.beta(3.0, 3.5, n), 0.06, 0.9, 3)
        uso_credito = _clip_round(rng.beta(2.7, 3.2, n), 0.03, 0.9, 3)
        revolvencia = _clip_round(rng.beta(2.1, 3.8, n), 0.01, 0.82, 3)
    else:
        transacciones = _clip_round(rng.gamma(3.1, 25, n), 12, 260)
        dias_activos = _clip_round(rng.normal(95, 36, n), 15, 235)
        comercios = _clip_round(rng.normal(32, 13, n), 5, 90)
        categorias = _clip_round(rng.normal(8, 2.5, n), 2, 17)
        pagos_rec = _clip_round(transacciones * rng.uniform(0.02, 0.13, n), 0, 42)
        depositos_rec = _clip_round(transacciones * rng.uniform(0.01, 0.08, n), 0, 26)
        ticket_prom = _clip_round(rng.lognormal(6.45, 0.45, n), 120, 2600, 2)
        concentracion = _clip_round(rng.beta(2.0, 7.0, n), 0.02, 0.45, 3)
        estacionalidad = _clip_round(rng.beta(1.6, 5.8, n), 0.02, 0.72, 3)
        antiguedad = _clip_round(rng.normal(38, 22, n), 3, 120)
        pct_tdc = _clip_round(rng.beta(2.2, 4.8, n), 0.01, 0.82, 3)
        uso_credito = _clip_round(rng.beta(1.9, 5.2, n), 0.0, 0.74, 3)
        revolvencia = _clip_round(rng.beta(1.5, 6.0, n), 0.0, 0.62, 3)

    pct_tdd = _clip_round(1 - pct_tdc - rng.uniform(0.0, 0.08, n), 0.02, 0.95, 3)
    ticket_med = _clip_round(ticket_prom * rng.uniform(0.68, 0.92, n), 70, None, 2)
    gasto_total = _clip_round(transacciones * ticket_prom * rng.uniform(0.82, 1.18, n), 1_000, None, 2)
    ingresos_totales = _clip_round(gasto_total * rng.uniform(1.02, 1.68, n), 1_200, None, 2)

    df = pd.DataFrame(
        {
            "cliente_id": [f"{prefix}_{i:05d}" for i in range(1, n + 1)],
            "tipo_cliente": tipo_cliente,
            "num_transacciones": transacciones.astype(int),
            "dias_activos": dias_activos.astype(int),
            "gasto_total": gasto_total,
            "ingresos_totales": ingresos_totales,
            "ticket_promedio": ticket_prom,
            "ticket_mediano": ticket_med,
            "num_comercios_distintos": comercios.astype(int),
            "num_categorias_distintas": categorias.astype(int),
            "pagos_recurrentes": pagos_rec.astype(int),
            "depositos_recurrentes": depositos_rec.astype(int),
            "porcentaje_tdc": pct_tdc,
            "porcentaje_tdd": pct_tdd,
            "uso_credito": uso_credito,
            "revolvencia": revolvencia,
            "concentracion_proveedores": concentracion,
            "estacionalidad": estacionalidad,
            "antiguedad_meses": antiguedad.astype(int),
            "perfil_sintetico": perfil,
        }
    )
    return df[RAW_COLUMNS + ["perfil_sintetico"]]


def generar_datos(n_empresariales=1200, n_personales=3500, proporcion_latente=0.12):
    rng = np.random.default_rng(RANDOM_STATE)
    n_latentes = int(round(n_personales * proporcion_latente))
    n_tradicionales = n_personales - n_latentes

    empresariales = _build_clients(rng, n_empresariales, "EMP", "empresarial", "empresarial")
    personales_trad = _build_clients(
        rng, n_tradicionales, "PER", "personal", "personal_tradicional"
    )
    personales_lat = _build_clients(
        rng, n_latentes, "PEL", "personal", "personal_comportamiento_empresarial_latente"
    )
    personales = pd.concat([personales_trad, personales_lat], ignore_index=True)
    personales = personales.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    return empresariales, personales


def main():
    ensure_directories()
    empresariales, personales = generar_datos()
    save_dataframe(empresariales, DATA_RAW / "clientes_empresariales.csv")
    save_dataframe(personales, DATA_RAW / "clientes_personales.csv")
    print("Datos sinteticos creados sin informacion personal real.")


if __name__ == "__main__":
    main()
