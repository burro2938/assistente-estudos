import streamlit as st
import datetime

# Configuração da Página
st.set_page_config(
    page_title="Assistente de Estudos",
    page_icon="📚",
    layout="wide"
)

# Estado da Sessão para Dados
if "logs" not in st.session_state:
    st.session_state.logs = []
if "flashcards" not in st.session_state:
    st.session_state.flashcards = [
        {"pergunta": "Qual é a capital de Portugal?", "resposta": "Lisboa"},
        {"pergunta": "Quanto é 7 x 8?", "resposta": "56"}
    ]
if "materiais" not in st.session_state:
    st.session_state.materiais = {}
if "horario" not in st.session_state:
    st.session_state.horario = {
        "Segunda-feira": ["Português", "Matemática", "Inglês", "História/Geografia"],
        "Terça-feira": ["Matemática", "Ciências Naturais", "Francês", "Físico-Química"],
        "Quarta-feira": ["Português", "Inglês", "Matemática", "Educação Física"],
        "Quinta-feira": ["História/Geografia", "Ciências Naturais", "Francês", "Físico-Química"],
        "Sexta-feira": ["Português", "Matemática", "Educação Visual", "Tecnologias"]
    }

# Barra Lateral de Navegação
st.sidebar.title("📚 Menu Principal")
menu = st.sidebar.radio(
    "Navegar para:",
    ["🏠 Início & Horário", "📝 Registo Diário", "🧠 Flashcards", "📁 Materiais de Estudo"]
)

# 1. Início & Horário
if menu == "🏠 Início & Horário":
    st.title("🎯 Meu Assistente de Estudos")
    st.write("Bem-vindo ao teu espaço centralizado de organização escolar e revisão!")
    
    col_ano1, col_ano2 = st.columns(2)
    with col_ano1:
        st.info("📌 **Ano Letivo:** 2026/2027")
    with col_ano2:
        st.success("🏫 **Escola:** Escola Básica de Manhente")

    st.markdown("---")
    st.subheader("📅 O teu Horário Semanal")
    
    dia_selecionado = st.selectbox("Seleciona o Dia da Semana", list(st.session_state.horario.keys()))
    
    st.write(f"**Aulas para {dia_selecionado}:**")
    for i, disciplina in enumerate(st.session_state.horario[dia_selecionado], 1):
        st.text(f"Módulo {i}: {disciplina}")
        
    st.markdown("---")
    st.subheader("⏳ Contagem Decrescente para Testes")
    
    col1, col2 = st.columns(2)
    with col1:
        materia_teste = st.text_input("Matéria / Disciplina do Teste")
    with col2:
        data_teste = st.date_input("Data do Teste", datetime.date.today())
        
    if st.button("Guardar Teste"):
        st.success(f"Teste de {materia_teste} agendado para {data_teste} com sucesso!")

# 2. Registo Diário
elif menu == "📝 Registo Diário":
    st.title("📝 Registo de Estudo Diário")
    
    data_hoje = st.date_input("Data", datetime.date.today())
    materia = st.selectbox("Matéria", ["Português", "Matemática", "Inglês", "Francês", "História/Geografia", "Físico-Química", "Ciências Naturais"])
    tempo = st.number_input("Tempo de estudo (minutos)", min_value=5, max_value=300, step=5)
    resumo = st.text_area("O que estudaste hoje?")
    
    if st.button("Registar Sessão"):
        st.session_state.logs.append({"data": data_hoje, "materia": materia, "tempo": tempo, "resumo": resumo})
        st.success("Sessão registada com sucesso!")
        
    if st.session_state.logs:
        st.markdown("---")
        st.subheader("📊 Histórico Recente")
        for log in reversed(st.session_state.logs):
            st.info(f"**{log['data']}** - {log['materia']} ({log['tempo']} min): {log['resumo']}")

# 3. Flashcards
elif menu == "🧠 Flashcards de Revisão":
    st.title("🧠 Flashcards Interativos")
    
    st.subheader("Criar Novo Flashcard")
    p_nova = st.text_input("Pergunta:")
    r_nova = st.text_input("Resposta:")
    if st.button("Adicionar Flashcard"):
        if p_nova and r_nova:
            st.session_state.flashcards.append({"pergunta": p_nova, "resposta": r_nova})
            st.success("Flashcard adicionado!")
        else:
            st.warning("Preenche ambos os campos.")
            
    st.markdown("---")
    st.subheader("Treinar Flashcards")
    if st.session_state.flashcards:
        idx = st.slider("Escolher número do flashcard", 0, len(st.session_state.flashcards)-1, 0)
        card = st.session_state.flashcards[idx]
        
        st.markdown(f"### Pergunta: {card['pergunta']}")
        if st.button("Mostrar Resposta"):
            st.success(f"Resposta:")
    else:
        st.write("Ainda não tens flashcards criados.")

# 4. Materiais de Estudo
elif menu == "📁 Materiais de Estudo":
    st.title("📁 Repositório de Materiais")
    
    mat_escolhida = st.selectbox("Seleciona a Matéria", ["Português", "Matemática", "Inglês", "Francês", "História/Geografia", "Físico-Química", "Ciências Naturais"])
    ficheiro = st.file_uploader("Carregar apontamento ou resumo (PDF/Imagem)", type=["pdf", "png", "jpg", "jpeg"])
    
    if ficheiro is not None:
        if mat_escolhida not in st.session_state.materiais:
            st.session_state.materiais[mat_escolhida] = []
        st.session_state.materiais[mat_escolhida].append(ficheiro.name)
        st.success(f"Ficheiro '{ficheiro.name}' guardado com sucesso em {mat_escolhida}!")
        
    if st.session_state.materiais:
        st.markdown("---")
        st.subheader("Ficheiros Guardados por Matéria")
        for m, f_list in st.session_state.materiais.items():
            st.write(f"**{m}:**")
            for f in f_list:
                st.text(f" - 📄 {f}")
