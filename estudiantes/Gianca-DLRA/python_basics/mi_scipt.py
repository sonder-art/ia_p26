class CalculadoraEspacial:
    """Calculadora simple para operaciones espaciales."""

    def __init__(self, combustible_inicial=0):
        # Guardamos el combustible disponible al inicio.
        self.combustible = combustible_inicial

    def sumar_combustible(self, cantidad):
        # Sumamos combustible y devolvemos el total actualizado.
        self.combustible += cantidad
        return self.combustible

    def calcular_distancia(self, velocidad, tiempo):
        # Distancia = velocidad * tiempo.
        return velocidad * tiempo

    def suficiente_para_marte(self):
        # Se necesitan al menos 100 unidades de combustible para llegar a Marte.
        return self.combustible >= 100


def distancia_de_vuelo(velocidad, tiempo):
    # Función simple que calcula la distancia de un vuelo.
    return velocidad * tiempo


if __name__ == "__main__":
    # Ejemplo básico de uso de la calculadora espacial.
    calc = CalculadoraEspacial(combustible_inicial=50)
    calc.sumar_combustible(60)
    distancia = distancia_de_vuelo(velocidad=20, tiempo=5)
    if calc.suficiente_para_marte():
        mensaje = "Sí, tenemos suficiente combustible para Marte."
    else:
        mensaje = "No, aún falta combustible para Marte."

    print(f"Combustible total: {calc.combustible}")
    print(f"Distancia calculada: {distancia}")
    print(mensaje)
