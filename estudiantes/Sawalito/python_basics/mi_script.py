"""
Script sencillo con una clase CalculadoraEspacial.

La idea es simular cálculos básicos relacionados con
combustible y distancias en un viaje espacial.
"""


class CalculadoraEspacial:
    """
    Clase que representa una calculadora para misiones espaciales.

    Atributos:
        combustible (float): cantidad de combustible disponible.
    """

    def __init__(self, combustible_inicial: float = 0.0) -> None:
        """
        Constructor de la CalculadoraEspacial.

        Args:
            combustible_inicial (float): combustible con el que empezamos.
                Por defecto es 0.0.
        """
        self.combustible = combustible_inicial

    def agregar_combustible(self, cantidad: float) -> None:
        """
        Suma combustible al tanque actual.

        Args:
            cantidad (float): cantidad de combustible a agregar.
        """
        # Validamos que la cantidad sea positiva
        if cantidad < 0:
            raise ValueError("La cantidad de combustible no puede ser negativa.")

        # Sumamos la cantidad al combustible actual
        self.combustible += cantidad

    def calcular_distancia_maxima(self, consumo_por_unidad: float) -> float:
        """
        Calcula la distancia máxima que se puede recorrer con el combustible actual.

        Suponemos un modelo muy simple:
        - Por cada unidad de combustible se pueden recorrer
          'consumo_por_unidad' unidades de distancia.

        Args:
            consumo_por_unidad (float): distancia que se puede recorrer
                con una unidad de combustible.

        Returns:
            float: distancia máxima posible.
        """
        if consumo_por_unidad <= 0:
            raise ValueError("El consumo por unidad debe ser mayor que cero.")

        # Distancia máxima = combustible disponible * distancia por unidad
        return self.combustible * consumo_por_unidad

    def tiene_combustible_para_marte(self) -> bool:
        """
        Indica si hay suficiente combustible para llegar a Marte.

        Para este ejemplo, decidimos que necesitamos al menos
        100 unidades de combustible para llegar.

        Returns:
            bool: True si hay 100 o más unidades, False en caso contrario.
        """
        combustible_necesario = 100
        return self.combustible >= combustible_necesario


if __name__ == "__main__":
    # Ejemplo de uso de la clase CalculadoraEspacial

    # Creamos una calculadora con 50 unidades de combustible inicial
    calculadora = CalculadoraEspacial(combustible_inicial=50)

    # Agregamos 60 unidades más
    calculadora.agregar_combustible(60)

    # Calculamos la distancia máxima con un consumo de 2 unidades de distancia
    # por cada unidad de combustible.
    distancia = calculadora.calcular_distancia_maxima(consumo_por_unidad=2)

    print(f"Combustible disponible: {calculadora.combustible}")
    print(f"Distancia máxima posible: {distancia}")
    print(
        "¿Hay suficiente combustible para llegar a Marte?",
        calculadora.tiene_combustible_para_marte(),
    )

