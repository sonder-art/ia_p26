import streamlit as st
from logic import KnowledgeBase # Importamos el motor lógico
from sympy import Not

def main():
    st.set_page_config(page_title="Logic Project Skeleton", page_icon="🧠")
    st.title("🧠 Logic Project Interface")
    st.info("Este es un cascarón base. Puedes modificarlo o usar cualquier otro framework (JS, HTML, etc.).")

    # Inicializar el motor en la sesión de Streamlit
    if 'engine' not in st.session_state:
        st.session_state.engine = KnowledgeBase()
        # Aquí puedes precargar tus reglas fijas
        # st.session_state.engine.add_rule(...)

    # --- SIDEBAR: HECHOS ---
    st.sidebar.header("📥 Entrada de Hechos")
    # Ejemplo: checkbox para capturar estados del mundo
    # fact_a = st.sidebar.checkbox("¿Ocurrió el evento A?")

    # --- MAIN: CONSULTA ---
    st.write("### ❓ Razonamiento")
    # query_input = st.text_input("¿Qué quieres preguntar al sistema?")

    if st.button("Ejecutar Motor de Inferencia"):
        # 1. Preparar hechos
        facts = []
        # if fact_a: facts.append(st.session_state.engine.get_symbol("A"))
        
        # 2. Consultar al motor
        # result = st.session_state.engine.ask(query_symbol, facts)
        
        st.warning("Motor no implementado. Configura logic.py y conecta los inputs aquí.")

    # --- DEBUG: VER KB ---
    with st.expander("🔍 Ver Base de Conocimiento Actual"):
        # st.write(st.session_state.engine.kb)
        pass

if __name__ == "__main__":
    main()
