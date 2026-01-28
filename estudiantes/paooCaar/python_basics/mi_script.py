class CalculadoraEspacial:
    """
    Esta clase representa una calculadora para operaciones espaciales,
    como sumar combustible y verificar si es suficiente para llegar a Marte.
    """

    def __init__(self):
        # Inicializamos el combustible en 0
        self.combustible = 0

    def sumar_combustible(self, cantidad):
        """
        Suma una cantidad de combustible al total actual.
        :param cantidad: unidades de combustible a agregar
        """
        self.combustible += cantidad
        return self.combustible

    def calcular_distancia(self, velocidad, tiempo):
        """
        Calcula la distancia recorrida usando la fórmula:
        distancia = velocidad * tiempo
        :param velocidad: velocidad de la nave
        :param tiempo: tiempo de viaje
        """
        distancia = velocidad * tiempo
        return distancia

    def puede_llegar_a_marte(self):
        """
        Decide si hay suficiente combustible para llegar a Marte.
        Se necesitan al menos 100 unidades de combustible.
        """
        if self.combustible >= 100:
            return True
        else:
            return False


# Ejemplo de uso de la clase
calculadora = CalculadoraEspacial()

# Sumamos combustible
calculadora.sumar_combustible(120)

# Calculamos una distancia
distancia = calculadora.calcular_distancia(velocidad=10, tiempo=5)
print("Distancia recorrida:", distancia)

# Verificamos si podemos llegar a Marte
if calculadora.puede_llegar_a_marte():
    print("¡Tenemos suficiente combustible para llegar a Marte!")
else:
    print("No hay suficiente combustible para llegar a Marte.")

