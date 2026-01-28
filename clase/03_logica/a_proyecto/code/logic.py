from sympy import Symbol, And, Or, Not, Implies, Equivalent
from sympy.logic.inference import satisfiable

class KnowledgeBase:
    """
    Motor de Lógica (Backend). 
    Esta clase debe gestionar la Base de Conocimiento (KB).
    """
    def __init__(self):
        # Almacena los símbolos (variables) para no duplicarlos
        self.symbols = {}
        # Lista de fórmulas que forman la Base de Conocimiento
        self.kb = []

    def get_symbol(self, name):
        """Crea o recupera un símbolo por su nombre."""
        if name not in self.symbols:
            self.symbols[name] = Symbol(name)
        return self.symbols[name]

    def add_rule(self, formula):
        """Agrega una regla o axioma a la KB."""
        self.kb.append(formula)

    def ask(self, query, facts):
        """
        Determina si la KB + hechos implican la consulta (query).
        Implementa aquí tu lógica de inferencia.
        
        Pista: Puedes usar sympy.logic.inference.satisfiable para implementar 
        una prueba por contradicción: (KB ∧ facts ∧ ¬query) es insatisfacible.
        """
        # combined = And(*self.kb, *facts, Not(query))
        # return not satisfiable(combined)
        return None

    def get_model(self, facts):
        """
        Busca un modelo (asignación V/F) que satisfaga la KB y los hechos.
        Útil para problemas de planeación o búsqueda de fallos.
        """
        pass
