# Conceptos Básicos de Python

Aquí tienes una referencia rápida de la sintaxis. Puedes copiar estos snippets a tu Cursor para probarlos.

## 1. Variables y Tipos

```python
nombre = "Juan"       # String
edad = 25             # Integer
altura = 1.75         # Float
es_estudiante = True  # Boolean

print(f"Hola, soy {nombre} y tengo {edad} años.")
```

## 2. Condicionales (If/Else)

```python
nota = 85

if nota >= 90:
    print("Excelente")
elif nota >= 70:
    print("Aprobado")
else:
    print("Reprobado")
```

## 3. Bucles (Loops)

```python
# Lista de frutas
frutas = ["manzana", "banana", "cereza"]

for fruta in frutas:
    print(f"Me gusta la {fruta}")

# Rango numérico
for i in range(5):
    print(f"Número: {i}")
```

## 4. Funciones

```python
def sumar(a, b):
    return a + b

resultado = sumar(5, 3)
print(resultado) # Imprime 8
```

## 5. Clases (POO)

```python
class Perro:
    def __init__(self, nombre):
        self.nombre = nombre

    def ladrar(self):
        return f"{self.nombre} dice: ¡Guau!"

mi_perro = Perro("Firulais")
print(mi_perro.ladrar())
```

---

## 🚀 Script de Ejemplo

Hemos incluido un archivo llamado `ejemplo_clase.py` en esta misma carpeta.
Para ejecutarlo:

1.  Abre la terminal en esta carpeta.
2.  Ejecuta: `python3 ejemplo_clase.py`
3.  Analiza el código para ver cómo funciona.

> **Prompt para LLM:**
> "No entiendo la parte de `__init__` en las clases de Python. ¿Me lo puedes explicar con una analogía sencilla como si fuera una fábrica de galletas?"

