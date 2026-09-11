st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&display=swap');

    /* Aplicar a fonte Comfortaa aos textos gerais */
    body, p, label, input, textarea, button, select, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stText, .stSelectbox, .stRadio, .stTextInput {
        font-family: 'Comfortaa', cursive, sans-serif !important;
    }
    
    /* Garantir que os seletores mantêm a fonte */
    div[data-baseweb="select"] * {
        font-family: 'Comfortaa', cursive, sans-serif !important;
    }

    /* Proteger os ícones do Streamlit (incluindo o botão de fechar/abrir a barra lateral) para não mostrarem texto raso */
    [data-testid="collapsedControl"] *, span[class*="material-icons"], i {
        font-family: 'Source Sans Pro', sans-serif !important;
    }

    /* Título "Menu Principal" na barra lateral */
    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
    }
    
    /* Opções de navegação da barra lateral */
    section[data-testid="stSidebar"] .stRadio label p {
        font-size: 15px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
