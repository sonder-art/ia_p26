import random
import datetime

class AsistenteIA:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conocimientos = ["Python", "Git", "Machine Learning", "Datos"]

    def saludar(self):
        hora = datetime.datetime.now().hour
        if hora < 12:
            momento = "Buenos días"
        elif hora < 18:
            momento = "Buenas tardes"
        else:
            momento = "Buenas noches"
        
        return f"¡{momento}! Soy {self.nombre}, tu asistente virtual."

    def dar_consejo(self):
        consejos = [
            "Recuerda hacer commit frecuentemente.",
            "Usa nombres de variables descriptivos.",
            "Si te atoras, pregúntale a un LLM.",
            "Mantén tu código limpio y comentado.",
            "¡No olvides tomar agua!"
        ]
        return random.choice(consejos)

def main():
    # Creamos una instancia de la clase
    mi_bot = AsistenteIA("CursorBot")
    
    print("-" * 40)
    print(mi_bot.saludar())
    print("-" * 40)
    
    print(f"Mis conocimientos son: {', '.join(mi_bot.conocimientos)}")
    
    print("\nAquí tienes un consejo del día:")
    print(f"💡 {mi_bot.dar_consejo()}")
    print("-" * 40)

if __name__ == "__main__":
    main()

