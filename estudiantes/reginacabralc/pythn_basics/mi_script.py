class CalculadoraEspacial:
    def __init__(self, combustible_inicial=0):
        # El constructor inicializa el nivel de combustible de la nave
        self.combustible = combustible_inicial

    def agregar_combustible(self, cantidad):
        """Suma unidades de combustible al tanque."""
        self.combustible += cantidad
        print(f"⛽ Se han añadido {cantidad} unidades. Combustible total: {self.combustible}")

    def calcular_distancia(self, velocidad, tiempo):
        """Calcula la distancia recorrida (Distancia = Velocidad * Tiempo)."""
        distancia = velocidad * tiempo
        return distancia

    def puede_llegar_a_marte(self):
        """Verifica si el combustible es suficiente (mínimo 100 unidades)."""
        objetivo = 100
        if self.combustible >= objetivo:
            return True
        else:
            faltante = objetivo - self.combustible
            print(f"⚠️ Alerta: Te faltan {faltante} unidades para llegar a Marte.")
            return False