"""
Script educativo: CalculadoraEspacial
Gestiona combustible, calcula distancias y determina si es posible viajar a Marte.
"""

class CalculadoraEspacial:
    """Clase que gestiona combustible y cálculos de distancia para misiones espaciales."""

    def __init__(self):
        """Constructor: inicializa el combustible del tanque en 0 unidades."""
        self.combustible = 0

    def sumar_combustible(self, cantidad):
        """Agrega combustible al tanque. cantidad: unidades a sumar."""
        self.combustible += cantidad

    def calcular_distancia(self, velocidad, tiempo):
        """Calcula la distancia con la fórmula distancia = velocidad × tiempo."""
        return velocidad * tiempo

    def puede_ir_a_marte(self):
        """Verifica si hay suficiente combustible para llegar a Marte (>= 100 unidades)."""
        if self.combustible >= 100:
            return True
        else:
            return False


def mostrar_estado(calculadora):
    """Función auxiliar: imprime el estado actual de combustible de la calculadora."""
    print(f"Combustible actual: {calculadora.combustible} unidades")


if __name__ == "__main__":
    # Crear una instancia de la calculadora espacial
    calc = CalculadoraEspacial()

    # Sumar combustible varias veces
    calc.sumar_combustible(30)
    calc.sumar_combustible(50)
    calc.sumar_combustible(25)

    # Mostrar estado del combustible
    mostrar_estado(calc)

    # Calcular una distancia de ejemplo (velocidad × tiempo)
    distancia = calc.calcular_distancia(velocidad=10, tiempo=5)
    print(f"Distancia calculada: {distancia} unidades")

    # Verificar si podemos ir a Marte
    if calc.puede_ir_a_marte():
        print("¡Sí podemos llegar a Marte!")
    else:
        print("No hay suficiente combustible para llegar a Marte (se necesitan 100 unidades).")
