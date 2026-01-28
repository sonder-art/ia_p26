"""
Script sencillo: CalculadoraEspacial

Requisitos cubiertos:
- Una clase: CalculadoraEspacial
- Una función: main()
- Un if/else: decide si alcanza el combustible para Marte
- Imprime en consola: varios print()
"""

class CalculadoraEspacial:
    # Constante: combustible mínimo requerido para llegar a Marte
    COMBUSTIBLE_PARA_MARTE = 100

    def __init__(self, combustible_inicial: float = 0.0) -> None:
        """Inicializa la calculadora con combustible inicial."""
        self.combustible = float(combustible_inicial)

    def sumar_combustible(self, cantidad: float) -> float:
        """
        Suma combustible al total actual.
        Regresa el total de combustible actualizado.
        """
        if cantidad < 0:
            raise ValueError("La cantidad a sumar no puede ser negativa.")
        self.combustible += float(cantidad)
        return self.combustible

    def calcular_distancia(self, velocidad: float, tiempo: float) -> float:
        """
        Calcula distancia con la fórmula:
        distancia = velocidad * tiempo
        """
        if velocidad < 0 or tiempo < 0:
            raise ValueError("Velocidad y tiempo deben ser no negativos.")
        return float(velocidad) * float(tiempo)

    def suficiente_para_marte(self) -> bool:
        """
        Decide si hay suficiente combustible para llegar a Marte.
        Se requiere al menos 100 unidades.
        """
        return self.combustible >= self.COMBUSTIBLE_PARA_MARTE


def main() -> None:
    """Función principal: crea un objeto y demuestra su uso."""
    calc = CalculadoraEspacial(combustible_inicial=50)
    print("🚀 Combustible inicial:", calc.combustible)

    # Sumamos combustible
    calc.sumar_combustible(60)
    print("⛽ Combustible después de sumar:", calc.combustible)

    # Calculamos una distancia de ejemplo
    distancia = calc.calcular_distancia(velocidad=12, tiempo=5)
    print("📏 Distancia calculada (velocidad=12, tiempo=5):", distancia)

    # if/else requerido: ¿alcanza para Marte?
    if calc.suficiente_para_marte():
        print("✅ Tenemos suficiente combustible para llegar a Marte.")
    else:
        print("❌ No tenemos suficiente combustible para llegar a Marte.")


# Esto permite ejecutar el script directamente: python archivo.py
if __name__ == "__main__":
    main()
