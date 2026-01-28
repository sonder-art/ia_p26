class CalculadoraEspacial:
    def __init__(self, combustible_inicial=0):
        # El constructor inicializa el tanque de combustible
        self.combustible = combustible_inicial
        # Distancia base a Marte en millones de km (promedio)
        self.distancia_marte = 225 

    def cargar_combustible(self, cantidad):
        """Suma unidades de combustible al tanque."""
        self.combustible += cantidad
        print(f"-> Se han cargado {cantidad} unidades. Combustible total: {self.combustible}")

    def calcular_distancia_restante(self, km_recorridos):
        """Calcula cuánto falta para llegar basándose en una distancia promedio."""
        restante = self.distancia_marte - km_recorridos
        return max(0, restante) # Evita distancias negativas

    def checar_mision_marte(self):
        """Verifica si el combustible es suficiente (mínimo 100 unidades)."""
        objetivo = 100
        if self.combustible >= objetivo:
            print("🚀 ¡Todo listo! Tienes combustible suficiente para el salto a Marte.")
            return True
        else:
            faltante = objetivo - self.combustible
            print(f"⚠️ Alerta: No hay suficiente energía. Faltan {faltante} unidades.")
            return False