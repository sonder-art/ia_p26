"""
mi_script.py
Calculadora simple: dado cuántos días llevas sin comer carne,
estima cuántos animales has "salvado" según una conversión configurable.

Nota: Este cálculo es una aproximación educativa; no representa una medida real.
"""


class CalculadoraAnimales:
    """
    Clase que encapsula la lógica de conversión de días sin carne -> animales salvados.

    Puedes cambiar el factor de conversión si quieres otra estimación.
    Ejemplo: 1 animal por cada 7 días (valor por defecto).
    """

    def __init__(self, dias_por_animal: int = 7) -> None:
        # Validamos el parámetro para evitar divisiones raras o valores sin sentido.
        if dias_por_animal <= 0:
            raise ValueError("dias_por_animal debe ser un entero positivo.")
        self.dias_por_animal = dias_por_animal

    def animales_salvados(self, dias_sin_carne: int) -> float:
        """
        Calcula animales salvados como una razón:
        animales = dias_sin_carne / dias_por_animal
        """
        return dias_sin_carne / self.dias_por_animal


def main() -> None:
    """Función principal: pide datos al usuario, valida, calcula e imprime resultados."""

    print("=== Calculadora de animales 'salvados' ===")
    print("Dime cuántos días llevas sin comer carne y haré una estimación.\n")

    # Pedimos input por consola. Esto devuelve texto, así que hay que convertirlo a int.
    entrada = input("¿Cuántos días llevas sin comer carne? ")

    # Validación con if/else (requisito): controlamos si el usuario escribió un número entero.
    if entrada.strip().lstrip("-").isdigit():
        dias = int(entrada)

        # Otro if/else: validamos que no sea negativo.
        if dias < 0:
            print("Error: los días no pueden ser negativos. Inténtalo de nuevo.")
            return

        calc = CalculadoraAnimales(dias_por_animal=7)
        animales = calc.animales_salvados(dias)

        # Imprimimos el resultado con formato (2 decimales).
        print("\nResultado:")
        print(f"- Días sin carne: {dias}")
        print(f"- Estimación de animales salvados: {animales:.2f}")

        # Mensaje extra para hacerlo más amigable.
        if dias == 0:
            print("\nTip: ¡puedes empezar hoy! Incluso un día cuenta.")
        else:
            print("\n¡Buen trabajo! Cada decisión suma.")
    else:
        print("Error: por favor escribe un número entero (por ejemplo: 0, 3, 14).")


# Este patrón permite ejecutar main() solo cuando se corre el archivo directamente:
# python3 mi_script.py
if __name__ == "__main__":
    main()
