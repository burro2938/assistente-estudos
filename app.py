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
if "escola" not in st.session_state:
    st.session_state.escola = "Escola Básica de Manhente"
if "ano_letivo" not in st.session_state:
    st.session_state.ano_letivo = "2026/2027"
if "horario" not in st.session_state:
    st.session_state.horario = {
        "Segunda-feira": [
            {"hora": "08:30 - 09:15", "disc": "Educação Física"},
            {"hora": "09:25 - 10:10", "disc": "Matemática"},
            {"hora": "10:30 - 11:15", "disc": "Inglês"},
            {"hora": "11:25 - 12:10", "disc": "Português"}
        ],
        "Terça-feira": [
            {"hora": "08:30 - 09:15", "disc": "Matemática"},
            {"hora": "09:25 - 10:10", "disc": "Ciências Naturais"},
            {"hora": "10:30 - 11:15", "disc": "Francês"},
            {"hora": "11:25 - 12:10", "disc": "Físico-Química"}
        ],
        "Quarta-feira": [
            {"hora": "08:30 - 09:15", "disc": "Português"},
            {"hora": "09:25 - 10:10", "disc": "Inglês"},
            {"hora": "10:30 - 11:15", "disc": "Matemática"},
            {"hora": "11:25 - 12:10", "disc": "Educação Física"}
        ],
        "Quinta-feira": [
            {"hora": "08:30 - 09:15", "disc": "História/Geografia"},
            {"hora": "09:25 - 10:10", "disc": "Ciências Naturais"},
            {"hora": "10:30 - 11:15", "disc": "Francês"},
            {"hora": "11:25 - 12:10", "disc": "Físico-Química"}
        ],
        "Sexta-feira": [
            {"hora": "08:30 - 09:15", "disc": "Português"},
            {"hora": "09:25 - 10:10", "disc": "Matemática"},
            {"hora": "10:30 - 11:15", "disc": "Educação Visual"},
            {"hora": "11:25 - 12:10", "disc": "Tecnologias"}
        ]
    }

# Chave de controlo para o número de linhas por dia em tempo de execução
if "num_aulas_extra" not in st.session_state:
    st.session_state.num_aulas_extra = {}

# Barra Lateral de Navegação
st.sidebar.title("📚 Menu Principal")
menu = st.sidebar.radio(
    "Navegar para:",
    [
        "🏠 Início & Escola",
        "📅 Agenda & Horário",
        "📝 Registo Diário",
        "🧠 Flashcards",
        "📁 Materiais de Estudo"
    ]
)

# 1. Início & Escola
if menu == "🏠 Início & Escola":
    st.title("🎯 Meu Assistente de Estudos")
    st.write("Bem-vindo ao teu espaço centralizado de organização escolar e revisão!")
    
    st.markdown("---")
    st.subheader("⚙️ Configurações do Aluno")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.escola = st.text_input("Escola Atual", value=st.session_state.escola)
    with col2:
        st.session_state.ano_letivo = st.text_input("Ano Letivo", value=st.session_state.ano_letivo)
        
    st.success(f"A frequentar o ano letivo **{st.session_state.ano_letivo}** em **{st.session_state.escola}**.")

# 2. Agenda & Horário
elif menu == "📅 Agenda & Horário":
    st.title("📅 Gestão de Horário e Agenda")
    
    st.subheader("Configurar Horário Semanal")
    dia_escolhido = st.selectbox("Dia da Semana", list(st.session_state.horario.keys()))
    
    st.write(f"Edita as horas e as disciplinas para **{dia_escolhido}**:")
    
    current_aulas = st.session_state.horario[dia_escolhido]
    
    if dia_escolhido not in st.session_state.num_aulas_extra:
        st.session_state.num_aulas_extra[dia_escolhido] = len(current_aulas)
        
    novo_dia = []
    
    # Renderizar campos para cada aula existente ou adicionada
    for idx in range(st.session_state.num_aulas_extra[dia_escolhido]):
        item = current_aulas[idx] if idx < len(current_aulas) else {"hora": "", "disc": ""}
        if not isinstance(item, dict):
            item = {"hora": "", "disc": str(item)}
            
        col1, col2 = st.columns(2)
        with col1:
            nova_hora = st.text_input(f"Hora da Aula {idx+1}", value=item.get("hora", ""), key=f"h_{dia_escolhido}_{idx}")
        with col2:
            nova_disc = st.text_input(f"Disciplina {idx+1}", value=item.get("disc", ""), key=f"d_{dia_escolhido}_{idx}")
        novo_dia.append({"hora": nova_hora, "disc": nova_disc})
        
    if st.button("➕ Adicionar Aula"):
        st.session_state.num_aulas_extra[dia_escolhido] += 1
        st.rerun()

    if st.button("Guardar Alterações do Horário"):
        st.session_state.horario[dia_escolhido] = novo_dia
        st.success(f"Horário de {dia_escolhido} guardado com sucesso!")
        
    st.markdown("---")
    st.subheader("⏳ Contagem Decrescente para Testes")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        materia_teste = st.text_input("Matéria / Disciplina do Teste")
    with col_t2:
        data_teste = st.date_input("Data do Teste", datetime.date.today())
        
    if st.button("Guardar Teste"):
        st.success(f"Teste de {materia_teste} agendado para {data_teste} com sucesso!")

# 3. Registo Diário
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

# 4. Flashcards
elif menu == "🧠 Flashcards":
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

# 5. Materiais de Estudo
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
