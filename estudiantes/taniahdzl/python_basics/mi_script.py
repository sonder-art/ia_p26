# Clase solicitada
class CalculadoraEspacial:
    def __init__(self, combustible):
        self.combustible = combustible

    # Función/Método para verificar el viaje
    def viaje_a_marte(self):
        # Uso de if/else
        if self.combustible >= 100:
            print("🚀 ¡Combustible suficiente! Despegando a Marte...")
        else:
            print("❌ Error: Necesitas al menos 100 unidades de combustible.")

# Ejecución del script
if __name__ == "__main__":
    # Creamos la nave con 120 unidades
    mi_nave = CalculadoraEspacial(120)
    mi_nave.viaje_a_marte()