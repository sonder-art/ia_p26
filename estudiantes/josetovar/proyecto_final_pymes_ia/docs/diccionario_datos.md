# Diccionario de datos

| variable | descripcion | interpretacion esperada |
|---|---|---|
| cliente_id | Identificador sintetico del cliente. | Permite unir resultados sin usar informacion personal real. |
| tipo_cliente | Universo sintetico del cliente: empresarial o personal. | Define la poblacion de referencia o evaluacion. |
| num_transacciones | Numero total de transacciones agregadas. | Valores altos sugieren mayor actividad operativa. |
| dias_activos | Dias con actividad transaccional. | Mas dias activos indican continuidad operativa. |
| gasto_total | Suma sintetica de egresos del cliente. | Mayor gasto puede reflejar operacion comercial mas intensa. |
| ingresos_totales | Suma sintetica de ingresos del cliente. | Mayor volumen de ingresos puede acercarse a patrones empresariales. |
| ticket_promedio | Monto promedio por transaccion. | Tickets altos pueden indicar ventas, compras de insumos o servicios profesionales. |
| ticket_mediano | Monto mediano por transaccion. | Ayuda a controlar valores extremos del ticket promedio. |
| num_comercios_distintos | Numero de contrapartes o comercios distintos. | Mayor diversidad puede reflejar red operativa mas amplia. |
| num_categorias_distintas | Numero de categorias transaccionales distintas. | Mayor diversidad de categorias sugiere operacion mas compleja. |
| pagos_recurrentes | Conteo de pagos repetidos a contrapartes. | Mas recurrencia puede asociarse a proveedores, rentas o servicios operativos. |
| depositos_recurrentes | Conteo de entradas recurrentes. | Mas recurrencia puede asociarse a ventas, clientes frecuentes o cobros periodicos. |
| porcentaje_tdc | Proporcion de transacciones asociadas a tarjeta de credito. | Valores altos pueden indicar financiamiento operativo o consumo con credito. |
| porcentaje_tdd | Proporcion de transacciones asociadas a tarjeta de debito. | Valores altos pueden indicar operacion con liquidez disponible. |
| uso_credito | Indicador sintetico de uso de credito. | Mayor uso puede sugerir dependencia financiera o capital de trabajo. |
| revolvencia | Indicador sintetico de saldo revolvente. | Mayor revolvencia puede asociarse a financiamiento recurrente. |
| concentracion_proveedores | Concentracion de gasto en pocos proveedores. | Valores altos sugieren dependencia de contrapartes especificas. |
| estacionalidad | Variacion sintetica por temporadas. | Valores altos sugieren ciclos de actividad marcados. |
| antiguedad_meses | Meses de relacion sintetica con la institucion. | Mayor antiguedad aporta contexto historico al comportamiento. |
| transacciones_por_dia_activo | Transacciones promedio por dia activo. | Mide intensidad diaria de actividad. |
| gasto_promedio_mensual | Gasto total dividido entre antiguedad. | Aproxima escala mensual de egresos. |
| ingreso_promedio_mensual | Ingreso total dividido entre antiguedad. | Aproxima escala mensual de entradas. |
| ratio_ingreso_gasto | Relacion entre ingresos y gastos. | Valores mayores a 1 indican entradas superiores a egresos. |
| indice_recurrencia | Pagos y depositos recurrentes sobre transacciones. | Mide peso de patrones repetitivos. |
| diversidad_operativa | Comercios y categorias sobre transacciones. | Resume amplitud operativa relativa. |
| exposicion_credito | Promedio de porcentaje TDC, uso de credito y revolvencia. | Resume intensidad de uso de credito. |
| intensidad_operativa | Transformacion logaritmica de transacciones por dias activos. | Resume escala de actividad evitando dominancia de extremos. |
| score_empresarial | Score normalizado de similitud empresarial entre 0 y 1. | Valores altos indican mayor similitud con el universo empresarial sintetico. |
| seleccionado | Indicador de pertenencia al percentil 90 del score. | Identifica clientes personales priorizados para segmentacion. |
| cluster | Grupo asignado por K-means para clientes seleccionados. | Numero tecnico de agrupamiento. |
| arquetipo | Nombre interpretable del cluster. | Facilita comunicar el perfil comportamental. |
