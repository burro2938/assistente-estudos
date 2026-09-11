import streamlit as st
import datetime

# Configuração da Página
st.set_page_config(
    page_title="Assistente de Estudos",
    page_icon="📚",
    layout="wide"
)

# Importar a fonte Comfortaa e aplicar corretamente a todos os elementos de texto e seletores
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&display=swap');

    /* Forçar a fonte Comfortaa em toda a aplicação, exceto nos ícones internos do sistema */
    html, body, [class*="css"], .stApp, p, span, div, label, input, textarea, button, select, h1, h2, h3, h4, h5, h6 {
        font-family: 'Comfortaa', cursive, sans-serif !important;
    }

    /* Exceção estrita para manter os ícones do Streamlit intocados e evitar o erro do keyboard */
    span[class*="icon"], div[class*="icon"], [data-testid*="icon"] {
        font-family: 'Material Icons', 'Streamlit-Icons', sans-serif !important;
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

# Estado da Sessão para Dados
if "logs" not in st.session_state:
    st.session_state.logs = []
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

# Estados para o fluxo do Registo Diário interativo
if "step_registo" not in st.session_state:
    st.session_state.step_registo = "formulario"
if "materia_escolhida_estudo" not in st.session_state:
    st.session_state.materia_escolhida_estudo = ""
if "materiais_carregados" not in st.session_state:
    st.session_state.materiais_carregados = []
if "num_aulas_extra" not in st.session_state:
    st.session_state.num_aulas_extra = {}

# Lista oficial de matérias solicitada
LISTA_MATERIAS = [
    "E.F. (Educação Física)",
    "Matemática",
    "Inglês",
    "Português",
    "Físico-Química",
    "Francês",
    "TIC (Tecnologias de Informação e Comunicação)",
    "Geografia",
    "Ciências Naturais",
    "História",
    "E.T. (Educação Tecnológica)",
    "E.V. (Educação Visual)",
    "Cidadania e Desenvolvimento"
]

# Barra Lateral de Navegação
st.sidebar.markdown("# Menu Principal")
menu = st.sidebar.radio(
    "Navegar para:",
    [
        "🏠 Início & Escola",
        "📅 Agenda & Horário",
        "📝 Registo Diário"
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

# 3. Registo Diário & Fluxo Interativo
elif menu == "📝 Registo Diário":
    
    # PASSO 1: Formulário de Registo Diário
    if st.session_state.step_registo == "formulario":
        st.title("📝 Registo de Estudo Diário")
        
        hoje = datetime.date.today()
        dias_portugal = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        dia_atual_idx = hoje.weekday()
        
        if dia_atual_idx >= 5:
            dia_automatico = "Segunda-feira"
        else:
            dia_automatico = dias_portugal[dia_atual_idx]
            
        st.markdown(f"### Hoje é **{dia_automatico}** ({hoje.strftime('%d/%m/%Y')})")
        
        aulas_do_dia = st.session_state.horario.get(dia_automatico, [])
        disciplinas_dia = []
        for aula in aulas_do_dia:
            disc = aula.get("disc", "") if isinstance(aula, dict) else str(aula)
            if disc and disc not in disciplinas_dia:
                disciplinas_dia.append(disc)
                
        resumos_por_materia = {}
        if disciplinas_dia:
            st.write("O que estudaste hoje em cada disciplina?")
            for disc in disciplinas_dia:
                resumos_por_materia[disc] = st.text_area(f"Matéria: {disc}", key=f"res_{dia_automatico}_{disc}")
        else:
            st.info("Não tens disciplinas configuradas para hoje.")
            
        if st.button("Registar Sessão"):
            registo_novo = {
                "data": str(hoje),
                "dia": dia_automatico,
                "resumos": resumos_por_materia
            }
            st.session_state.logs.append(registo_novo)
            st.success("Sessão registada com sucesso!")
            st.session_state.step_registo = "flashcards_pos"
            st.rerun()
            
        if st.session_state.logs:
            st.markdown("---")
            st.subheader("📊 Histórico Recente")
            for log in reversed(st.session_state.logs):
                st.info(f"**{log.get('data', '')}** ({log.get('dia', '')})")
                for d, r in log.get("resumos", {}).items():
                    if r:
                        st.write(f"- **{d}:** {r}")

    # PASSO 2: Flashcards de Revisão Pós-Registo
    elif st.session_state.step_registo == "flashcards_pos":
        if st.button("⬅️ Voltar"):
            st.session_state.step_registo = "formulario"
            st.rerun()
            
        st.title("🧠 Revisão Rápida (Flashcards)")
        st.write("Responde a estas perguntas de escolha múltipla geradas com base no que estudaste hoje para fixar a matéria:")
        
        perguntas_exemplo = [
            {"p": "Qual dos seguintes conceitos esteve mais em destaque na matéria de hoje?", "opcoes": ["Opção A", "Opção B", "Opção C", "Nenhuma das anteriores"], "correta": 0},
            {"p": "Identifica a principal regra ou propriedade abordada na aula:", "opcoes": ["Propriedade Distributiva", "Lei Geral de Ocorrência", "Estrutura Base", "Nenhum dos anteriores"], "correta": 0},
            {"p": "Assinala a afirmação correta sobre o tema estudado:", "opcoes": ["Aplica-se apenas em casos isolados", "É uma norma universal do tema", "Não tem aplicação prática", "Depende do contexto temporal"], "correta": 1},
            {"p": "De acordo com os apontamentos, qual é o elemento principal?", "opcoes": ["Fator X", "Fator Y", "Fator Z", "Nenhum"], "correta": 0},
            {"p": "Qual é o objetivo principal do exercício prático analisado?", "opcoes": ["Memorização", "Compreensão estrutural", "Cálculo direto", "Análise crítica"], "correta": 1},
            {"p": "Se surgisse uma exceção à regra estudada, qual seria?", "opcoes": ["Variação de ambiente", "Erro de cálculo", "Inexistência de exceção", "Condição externa"], "correta": 2},
            {"p": "Como se categoriza o principal tópico da lição?", "opcoes": ["Teórico", "Prático-Experimental", "Híbrido", "Introdutório"], "correta": 1},
            {"p": "Qual destas ferramentas ou métodos foi associada ao estudo?", "opcoes": ["Esquema de síntese", "Tabela periódica", "Linha temporal", "Nenhum"], "correta": 0},
            {"p": "Seleciona o sinónimo ou termo equivalente abordado:", "opcoes": ["Conceito Base", "Termo Secundário", "Variável Livre", "Constante"], "correta": 0},
            {"p": "Qual foi a conclusão principal retirada da matéria de hoje?", "opcoes": ["Consolidação da base teórica", "Avanço para novos módulos", "Revisão geral", "Avaliação pendente"], "correta": 0}
        ]
        
        for i, q in enumerate(perguntas_exemplo):
            st.markdown(f"**Questão {i+1}:** {q['p']}")
            st.radio(f"Escolhe uma opção para a questão {i+1}:", q['opcoes'], key=f"q_pos_{i}")
            st.markdown("---")
            
        if st.button("Avançar para o Estudo"):
            st.session_state.step_registo = "escolher_materia"
            st.rerun()

    # PASSO 3: Seleção de Matéria de Estudo com Sugestão Inteligente
    elif st.session_state.step_registo == "escolher_materia":
        if st.button("⬅️ Voltar"):
            st.session_state.step_registo = "flashcards_pos"
            st.rerun()
            
        st.title("📚 Estudo")
        st.subheader("O que queres estudar hoje?")
        
        sugestao = "Matemática"
        if st.session_state.logs:
            ultimo_log = st.session_state.logs[-1]
            resumos_ult = ultimo_log.get("resumos", {})
            if resumos_ult:
                sugestao = list(resumos_ult.keys())[0]
                
        st.info(f"💡 **Sugestão:** {sugestao} (com base no teu registo anterior)")
        
        materia_escolhida = st.selectbox("Escolhe a matéria que queres aprofundar:", LISTA_MATERIAS)
        
        if st.button("Avançar"):
            st.session_state.materia_escolhida_estudo = materia_escolhida
            st.session_state.step_registo = "upload_materiais"
            st.rerun()

    # PASSO 4: Materiais de Estudo para a Matéria Escolhida
    elif st.session_state.step_registo == "upload_materiais":
        if st.button("⬅️ Voltar"):
            st.session_state.step_registo = "escolher_materia"
            st.rerun()
            
        st.title("📚 Estudo")
        st.subheader("Materiais de Estudo")
        st.markdown(f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo}")
        
        ficheiros = st.file_uploader(
            "Carrega os teus documentos (PDF, Imagens PNG/JPG, Documentos, Áudios e Vídeos):",
            type=["pdf", "png", "jpg", "jpeg", "docx", "txt", "mp3", "mp4", "wav"],
            accept_multiple_files=True
        )
        
        if ficheiros:
            st.session_state.materiais_carregados = ficheiros
            for f in ficheiros:
                st.text(f"📄 Carregado: {f.name}")
                
        if st.button("Avançar"):
            st.session_state.step_registo = "escolher_atividade"
            st.rerun()

    # PASSO 5: Escolha da Atividade Principal Baseada nos Ficheiros
    elif st.session_state.step_registo == "escolher_atividade":
        if st.button("⬅️ Voltar"):
            st.session_state.step_registo = "upload_materiais"
            st.rerun()
            
        st.title("📚 Estudo")
        st.subheader("O que queres fazer primeiro?")
        
        atividade = st.radio(
            "Seleciona a opção pretendida:",
            [
                "Exercícios",
                "Quizzes",
                "Transcrição e Consolidação de Conteúdos",
                "Flashcards"
            ]
        )
        
        if st.button("Iniciar Atividade"):
            st.success(f"A iniciar a atividade: **{atividade}** para a matéria **{st.session_state.materia_escolhida_estudo}** com base nos ficheiros enviados!")
            if st.button("🔄 Recomeçar Novo Registo Diário"):
                st.session_state.step_registo = "formulario"
                st.rerun()
