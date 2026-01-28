# Este script es un ejemplo básico de Python para la tarea 02
# Incluye una clase, una función, un if/else y prints en consola

class CalculadoraEspacial:
    """
    Clase que representa una calculadora para misiones espaciales.
    Permite sumar combustible y verificar si alcanza para llegar a Marte.
    """

    def __init__(self, combustible_inicial):
        # Guardamos el combustible inicial
        self.combustible = combustible_inicial

    def sumar_combustible(self, cantidad):
        """
        Suma combustible a la nave.
        """
        self.combustible += cantidad
        print(f"Combustible actual: {self.combustible}")

    def puede_llegar_a_marte(self):
        """
        Verifica si hay suficiente combustible para llegar a Marte.
        Se necesitan al menos 100 unidades.
        """
        if self.combustible >= 100:
            print("✅ Tenemos suficiente combustible para llegar a Marte.")
            return True
        else:
            print("❌ No hay suficiente combustible para llegar a Marte.")
            return False


def calcular_distancia(velocidad, tiempo):
    """
    Función que calcula distancia usando la fórmula:
    distancia = velocidad * tiempo
    """
    distancia = velocidad * tiempo
    print(f"La distancia recorrida es {distancia} km.")
    return distancia


# --- Código principal ---
if __name__ == "__main__":
    print("🚀 Iniciando simulación espacial")

    # Creamos una calculadora con combustible inicial
    nave = CalculadoraEspacial(60)

    # Sumamos combustible
    nave.sumar_combustible(30)

    # Verificamos si podemos llegar a Marte
    nave.puede_llegar_a_marte()

    # Calculamos una distancia de ejemplo
    calcular_distancia(velocidad=10, tiempo=5)
