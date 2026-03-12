NECESARIO_MARTE = 100


def km_a_millas(km: float) -> float:
    """Convierte kilómetros a millas."""
    return km * 0.621371


class CalculadoraEspacial:
    def __init__(self, combustible: int = 0):
        self.combustible = combustible

    def sumar_combustible(self, extra: int) -> None:
        """Suma combustible al tanque."""
        if extra <= 0:
            print("No puedes agregar combustible negativo o cero.")
        else:
            self.combustible += extra
            print(f"Combustible actualizado: {self.combustible} unidades")

    def puede_llegar_a_marte(self) -> bool:
        """Decide si alcanza el combustible para llegar a Marte."""
        if self.combustible >= NECESARIO_MARTE:
            print("Sí alcanza para llegar a Marte.")
            return True
        else:
            faltan = NECESARIO_MARTE - self.combustible
            print(f"No alcanza. Te faltan {faltan} unidades de combustible.")
            return False

    def calcular_distancia(self, km: float) -> None:
        """Imprime distancia en km y millas."""
        millas = km_a_millas(km)
        print(f"Distancia: {km} km (~{millas:.2f} millas)")


if __name__ == "__main__":
    print("Iniciando CalculadoraEspacial...")

    nave = CalculadoraEspacial(combustible=60)
    nave.calcular_distancia(225_000_000)
    nave.puede_llegar_a_marte()

    nave.sumar_combustible(50)
    nave.puede_llegar_a_marte()