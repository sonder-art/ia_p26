# Deteccion de comportamiento empresarial latente en clientes personales mediante aprendizaje automatico

## Descripcion del problema

En instituciones financieras puede existir un grupo de clientes registrados como personales que muestran patrones transaccionales parecidos a los de clientes empresariales. Identificar estos patrones permite entender mejor su comportamiento, disenar propuestas de valor mas adecuadas y priorizar analisis comerciales o de riesgo. Este proyecto no afirma que dichos clientes sean legalmente PyMEs; solo estima similitud comportamental a partir de variables sinteticas agregadas.

## Objetivo general

Construir un pipeline reproducible que genere datos sinteticos, construya variables agregadas por cliente, entrene un modelo de similitud empresarial usando clientes empresariales sinteticos, aplique el score a clientes personales y segmente a los clientes personales de mayor similitud en arquetipos interpretables.

## Hipotesis de trabajo

Algunos clientes personales presentan mayor actividad, recurrencia, diversidad operativa y volumen transaccional que el promedio de clientes personales tradicionales. Estos patrones pueden aproximarse mediante aprendizaje de similitud y posteriormente organizarse en arquetipos utiles para interpretacion.

## Descripcion de los datos

La base es completamente sintetica y no contiene informacion personal real. Se generan dos universos:

- Clientes empresariales sinteticos: mayor numero de transacciones, dias activos, diversidad, recurrencia y volumen.
- Clientes personales sinteticos: principalmente patrones de consumo cotidiano, con un subgrupo de comportamiento empresarial latente equivalente a aproximadamente 12% del universo personal.

Las variables incluyen actividad transaccional, montos, diversidad de comercios y categorias, recurrencia, uso de credito, concentracion de proveedores, estacionalidad y antiguedad.

## Metodologia

1. Generacion de bases sinteticas empresariales y personales.
2. Construccion de variables derivadas por cliente.
3. Entrenamiento de Isolation Forest usando solo clientes empresariales.
4. Aplicacion del modelo al universo personal.
5. Normalizacion del score empresarial entre 0 y 1.
6. Seleccion de clientes personales ubicados en el percentil 90 del score.
7. Segmentacion de clientes seleccionados mediante estandarizacion, PCA y K-means.
8. Exportacion de tablas, graficas y documentacion.

## Modelos utilizados

- **Isolation Forest:** modelo principal de similitud. Aprende la region de comportamiento empresarial sintetico y evalua que tan compatible es cada cliente personal con ese patron.
- **Random Forest auxiliar:** modelo de interpretabilidad usado solo para estimar importancia aproximada de variables al distinguir clientes empresariales sinteticos contra personales sinteticos. No se usa para asignar el score final.
- **PCA:** reduccion a dos componentes para visualizar clientes seleccionados.
- **K-means:** agrupamiento de clientes personales seleccionados en cinco arquetipos interpretables.

## Resultados generados

- `data/processed/clientes_empresariales_features.csv`
- `data/processed/clientes_personales_features.csv`
- `data/processed/clientes_personales_scoreados.csv`
- `data/processed/resumen_arquetipos.csv`
- `outputs/distribucion_scores.png`
- `outputs/clusters_pca.png`
- `outputs/importancia_variables.png`
- `outputs/perfil_arquetipos.png`

## Estructura del repositorio

```text
estudiantes/josetovar/proyecto_final_pymes_ia/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── outputs/
└── docs/
```

## Instrucciones de ejecucion

Desde la carpeta `estudiantes/josetovar/proyecto_final_pymes_ia/`:

```bash
pip install -r requirements.txt
python src/01_generar_datos.py
python src/02_feature_engineering.py
python src/03_modelo_similitud.py
python src/04_clustering_arquetipos.py
python src/05_generar_resultados.py
```

El flujo completo puede ejecutarse sin datos externos, sin credenciales y sin conexion a internet.
