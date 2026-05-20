# Guia de presentacion

| slide | titulo sugerido | mensaje principal | visual sugerido | bullets recomendados |
|---|---|---|---|---|
| 1 | Titulo | El proyecto detecta similitud empresarial latente en clientes personales mediante IA. | Portada con nombre del proyecto y autor. | Contexto financiero; proyecto final; enfoque de aprendizaje automatico. |
| 2 | Problema | Algunos clientes personales pueden operar con patrones similares a negocios sin estar clasificados legalmente como PyME. | Diagrama simple de universos: empresarial, personal tradicional y personal latente. | No es clasificacion legal; oportunidad analitica; comportamiento transaccional agregado. |
| 3 | Objetivo | Crear un pipeline reproducible para scorear y segmentar clientes personales. | Flujo del pipeline de punta a punta. | Generar datos; entrenar similitud; seleccionar percentil 90; crear arquetipos. |
| 4 | Datos | La base es sintetica, coherente y sin datos personales reales. | Tabla resumen de clientes empresariales y personales. | Variables agregadas; patrones diferenciados; 12% personal latente sintetico. |
| 5 | Variables construidas | Las variables resumen actividad, escala, recurrencia, diversidad y uso de credito. | Barras o matriz de familias de variables. | Actividad; montos; recurrencia; diversidad; credito; estacionalidad. |
| 6 | Modelo de similitud | Isolation Forest aprende el patron empresarial y evalua compatibilidad de clientes personales. | Esquema de entrenamiento con empresariales y aplicacion a personales. | Entrenamiento solo empresarial; score 0 a 1; mas alto implica mayor similitud. |
| 7 | Seleccion de clientes | El percentil 90 identifica el decil superior de similitud empresarial. | Histograma `distribucion_scores.png`. | Umbral transparente; foco analitico; clientes personales priorizados. |
| 8 | Segmentacion en arquetipos | PCA y K-means organizan a los clientes seleccionados en perfiles interpretables. | Grafica `clusters_pca.png`. | Estandarizacion; PCA para visualizar; K-means con k=5; nombres interpretables. |
| 9 | Resultados | Los arquetipos muestran diferencias en escala, recurrencia, credito y estacionalidad. | `perfil_arquetipos.png` y tabla `resumen_arquetipos.csv`. | Comerciante intensivo; profesionista independiente; negocio digital; operador estacional; dependiente de crédito. |
| 10 | Conclusiones | El enfoque permite detectar comportamiento empresarial latente sin asumir una clasificacion legal. | Slide final con hallazgos y limitaciones. | Score interpretable; segmentacion accionable; limitaciones sinteticas; mejoras con datos reales. |
