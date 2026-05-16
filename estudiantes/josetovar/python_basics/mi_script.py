# mi_script.py
# CalculadoraEspacial — tarea A.6.4

class CalculadoraEspacial:
    """Clase para calcular viajes espaciales."""

    COMBUSTIBLE_MARTE = 100

    def __init__(self, nombre_nave):
        self.nombre_nave = nombre_nave
        self.combustible = 0

    def cargar_combustible(self, cantidad):
        """Agrega combustible a la nave."""
        self.combustible += cantidad
        print(f"{self.nombre_nave}: combustible total = {self.combustible} unidades")

    def puede_ir_a_marte(self):
        """Decide si hay suficiente combustible para llegar a Marte."""
        if self.combustible >= self.COMBUSTIBLE_MARTE:
            print(f"¡{self.nombre_nave} tiene suficiente combustible para llegar a Marte!")
            return True
        else:
            faltante = self.COMBUSTIBLE_MARTE - self.combustible
            print(f"{self.nombre_nave} NO puede llegar a Marte. Faltan {faltante} unidades.")
            return False


def calcular_distancia(velocidad_km_h, horas):
    """Calcula la distancia recorrida dado velocidad y tiempo."""
    return velocidad_km_h * horas


# --- Programa principal ---
nave = CalculadoraEspacial("Apolo-99")
nave.cargar_combustible(60)
nave.cargar_combustible(50)
nave.puede_ir_a_marte()

distancia = calcular_distancia(28000, 24)
print(f"Distancia en 24 horas a 28,000 km/h: {distancia:,} km")
