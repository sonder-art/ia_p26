# Metodologia

## Alcance conceptual

Este proyecto no realiza una clasificacion legal de PyMEs. La condicion de PyME depende de criterios regulatorios, fiscales, laborales y administrativos que no pueden inferirse de manera valida solo con comportamiento transaccional sintetico. Por ello, el resultado se interpreta como una medida de similitud empresarial y no como una etiqueta juridica o fiscal.

## Aprendizaje de similitud

El objetivo es identificar clientes personales cuyo patron agregado se parece al universo empresarial sintetico. Este planteamiento es mas adecuado que una clasificacion directa porque el grupo de interes no tiene una etiqueta real observada: se busca detectar comportamiento latente, no confirmar una categoria formal.

## Uso de Isolation Forest

Isolation Forest se entrena solo con clientes empresariales sinteticos para aprender la zona de comportamiento considerada normal dentro de ese universo. Al aplicar el modelo a clientes personales, aquellos que resultan menos anomalos respecto al patron empresarial reciben un score mas alto de similitud. El score se normaliza entre 0 y 1 para facilitar su lectura.

## Interpretacion del score empresarial

Un score cercano a 1 indica mayor similitud con patrones empresariales sinteticos: mayor actividad, recurrencia, diversidad operativa, volumen de ingresos y gasto, o uso financiero mas intenso. Un score bajo indica mayor distancia respecto al universo empresarial sintetico. La seleccion final usa el percentil 90 del score, de modo que se analiza el decil superior de clientes personales.

## Modelo auxiliar de interpretabilidad

Se entrena un Random Forest auxiliar para distinguir clientes empresariales sinteticos contra clientes personales sinteticos. Su proposito es estimar importancia aproximada de variables y apoyar la explicacion del proyecto. Este modelo no genera el score empresarial ni determina la seleccion final.

## Uso de PCA

PCA reduce las variables estandarizadas a dos componentes para visualizar la distribucion de los clientes personales seleccionados. Su funcion principal es exploratoria y grafica; no reemplaza las variables originales ni define por si mismo la similitud empresarial.

## Uso de K-means

K-means agrupa a los clientes personales seleccionados en perfiles relativamente homogeneos. Se usa `k=5` para producir arquetipos interpretables: Comerciante intensivo, Profesionista independiente, Negocio digital, Operador estacional y Dependiente de credito.

## Limitaciones

- La base es sintetica y no representa poblaciones reales.
- Las distribuciones fueron disenadas con supuestos razonables, pero no calibradas con datos observados.
- El score no debe usarse para decisiones crediticias, regulatorias o comerciales reales sin validacion adicional.
- Isolation Forest captura similitud estadistica, no causalidad.
- Los nombres de arquetipos son interpretaciones analiticas y pueden cambiar con datos reales.

## Mejoras con datos reales

Con datos reales se podria calibrar la generacion de variables, validar estabilidad temporal, incorporar series de tiempo, medir precision contra etiquetas observadas, revisar sesgos, aplicar validacion fuera de muestra y construir explicaciones locales por cliente. Tambien seria necesario aplicar controles de privacidad, seguridad, gobierno de datos y cumplimiento normativo.
