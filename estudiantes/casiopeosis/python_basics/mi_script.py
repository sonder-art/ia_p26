class AnalizaProba:
    def __init__(self, datos):
        self.datos = datos
        self.n = len(datos)
    
    def promedio(self):
        return sum(self.datos) / self.n
    
    def varianza(self):
        mu = self.promedio()
        return sum((x - mu) ** 2 for x in self.datos) / self.n
    
    def desv_est(self):
        return self.varianza() ** 0.5
    
    def z_score(self, value):
        mu = self.promedio()
        sigma = self.desv_est()
        return (value - mu) / sigma if sigma != 0 else 0
    
    def analizar_valor(self, value):
        z = self.z_score(value)
        
        if abs(z) > 2:
            clasificacion = "extremo"
        else:
            clasificacion = "típico"
        
        return clasificacion, z


def tiradas_de_dados(n_rolls):
    import random
    return [random.randint(1, 6) for _ in range(n_rolls)]


rolls = tiradas_de_dados(1000)
analyzer = AnalizaProba(rolls)

print(f"Análisis de {len(rolls)} tiradas de dado:")
print(f"Media: {analyzer.promedio():.2f}")
print(f"Varianza: {analyzer.varianza():.2f}")
print(f"Desviación estándar: {analyzer.desv_est():.2f}")

test_value = 6
clasificacion, z_score = analyzer.analizar_valor(test_value)

print(f"\nValor analizado: {test_value}")
print(f"Z-score: {z_score:.2f}")
print(f"Clasificación: {clasificacion}")

if clasificacion == "extremo":
    print("Este valor está lejos de lo esperado (>2 desviaciones estándar)")
else:
    print("Este valor está dentro del rango esperado")