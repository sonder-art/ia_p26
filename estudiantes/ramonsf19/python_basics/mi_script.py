# Mi primer script de Python para la clase
# Incluye: clase, función, if/else e impresión en consola

class CalculadoraEspacial:
    """
    Clase que modela una calculadora simple para una misión espacial.
    """

    def __init__(self, combustible):
        # Guardamos la cantidad de combustible disponible
        self.combustible = combustible

    def puede_llegar_a_marte(self):
        """
        Decide si tenemos suficiente combustible para llegar a Marte.
        Se necesitan al menos 100 unidades.
        """
        if self.combustible >= 100:
            print("🚀 ¡Tenemos suficiente combustible para llegar a Marte!")
        else:
            print("⛽ No hay suficiente combustible para llegar a Marte.")


def sumar_combustible(actual, extra):
    """
    Función que suma combustible adicional al combustible actual.
    """
    return actual + extra


# --------- PROGRAMA PRINCIPAL ---------

if __name__ == "__main__":
    # Combustible inicial de la nave
    combustible_inicial = 70

    # Combustible extra que conseguimos
    combustible_extra = 50

    # Usamos la función para sumar combustible
    total_combustible = sumar_combustible(
        combustible_inicial, combustible_extra
    )

    print(f"Combustible total: {total_combustible}")

    # Creamos un objeto de la clase y evaluamos la misión
    calculadora = CalculadoraEspacial(total_combustible)
    calculadora.puede_llegar_a_marte()
