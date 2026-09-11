import streamlit as st
import datetime
import random

# Configuração da Página
st.set_page_config(
    page_title="Assistente de Estudos",
    page_icon="📚",
    layout="wide"
)

# Importar a fonte Comfortaa e aplicar corretamente mantendo os ícones intactos
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

    /* Proteger os ícones do Streamlit para o símbolo « voltar a aparecer corretamente */
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

# Estados para os fluxos interativos
if "step_registo" not in st.session_state:
    st.session_state.step_registo = "formulario"
if "step_estudar" not in st.session_state:
    st.session_state.step_estudar = "escolher_materia"
if "materia_escolhida_estudo" not in st.session_state:
    st.session_state.materia_escolhida_estudo = ""
if "materiais_carregados" not in st.session_state:
    st.session_state.materiais_carregados = []
if "texto_estudo_livre" not in st.session_state:
    st.session_state.texto_estudo_livre = ""
if "num_aulas_extra" not in st.session_state:
    st.session_state.num_aulas_extra = {}
if "exercicios_gerados" not in st.session_state:
    st.session_state.exercicios_gerados = []

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

# Função para gerar 30 exercícios automáticos de Matemática (Equações)
def gerar_30_exercicios():
    exs = []
    random.seed(42) # Para manter a consistência na sessão
    for i in range(1, 31):
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        sol = random.randint(1, 15)
        c = a * sol + b
        # Equação do tipo: a*x + b = c -> a*x = c - b -> x = sol
        enunciado = f"{a}x + {b} = {c}"
        exs.append({
            "id": i,
            "enunciado": enunciado,
            "resposta_correta": float(sol)
        })
    return exs

# Barra Lateral de Navegação
st.sidebar.markdown("# Menu Principal")
menu = st.sidebar.radio(
    "Navegar para:",
    [
        "🏠 Início & Escola",
        "📅 Agenda & Horário",
        "📝 Registo Diário",
        "📖 Estudar"
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

# 3. Registo Diário
elif menu == "📝 Registo Diário":
    if st.session_state.step_registo == "formulario":
        st.title("📝 Registo de Estudo Diário")
        
        hoje = datetime.date.today()
        dias_portugal = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        dia_atual_idx = hoje.weekday()
        dia_automatico = "Segunda-feira" if dia_atual_idx >= 5 else dias_portugal[dia_atual_idx]
            
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

    elif st.session_state.step_registo == "flashcards_pos":
        if st.button("⬅️ Voltar"):
            st.session_state.step_registo = "formulario"
            st.rerun()
            
        st.title("🧠 Revisão Rápida (Flashcards)")
        st.write("Responde a estas perguntas geradas com base no que estudaste hoje:")
        
        for i in range(5):
            st.markdown(f"**Questão {i+1}:** Qual é a propriedade principal aplicada no cálculo de hoje?")
            st.radio(f"Opções Q{i+1}:", ["Propriedade Distributiva", "Isolamento da Incógnita", "Regra Geral", "Nenhuma"], key=f"q_pos_{i}")
            st.markdown("---")
            
        if st.button("Ir para o Estudo"):
            st.session_state.step_estudar = "escolher_materia"
            st.session_state.step_registo = "formulario"
            st.rerun()

# 4. Alínea: Estudar
elif menu == "📖 Estudar":
    
    # PASSO A: Escolha de Matéria
    if st.session_state.step_estudar == "escolher_materia":
        st.title("📚 Estudo")
        st.subheader("O que queres estudar hoje?")
        
        sugestao = "Matemática"
        if st.session_state.logs:
            ultimo_log = st.session_state.logs[-1]
            resumos_ult = ultimo_log.get("resumos", {})
            if resumos_ult:
                sugestao = list(resumos_ult.keys())[0]
                
        st.info(f"💡 **Sugestão:** {sugestao} (com base no teu registo anterior)")
        
        materia_escolhida = st.selectbox("Escolhe a matéria que queres aprofundar:", LISTA_MATERIAS, key="sb_estudar_mat")
        
        if st.button("Avançar", key="btn_avancar_mat"):
            st.session_state.materia_escolhida_estudo = materia_escolhida
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()

    # PASSO B: Upload ou Texto Direto (Opcional)
    elif st.session_state.step_estudar == "upload_materiais":
        if st.button("⬅️ Voltar", key="btn_voltar_up"):
            st.session_state.step_estudar = "escolher_materia"
            st.rerun()
            
        st.title("📚 Estudo")
        st.subheader("Materiais de Estudo")
        st.markdown(f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo}")
        
        ficheiros = st.file_uploader(
            "Carrega os teus documentos (PDF, Imagens PNG/JPG, Documentos, Áudios e Vídeos):",
            type=["pdf", "png", "jpg", "jpeg", "docx", "txt", "mp3", "mp4", "wav"],
            accept_multiple_files=True,
            key="up_materiais_estudar"
        )
        
        if ficheiros:
            st.session_state.materiais_carregados = ficheiros
            for f in ficheiros:
                st.text(f"📄 Carregado: {f.name}")
                
        st.markdown("---")
        st.write("Caso não queira carregar ficheiros, escreva a matéria ou os apontamentos abaixo (ou avance diretamente):")
        st.session_state.texto_estudo_livre = st.text_area(
            "Apontamentos / Tópicos da Matéria:", 
            value=st.session_state.texto_estudo_livre, 
            key="txt_livre_estudo"
        )
                
        if st.button("Avançar", key="btn_avancar_up"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()

    # PASSO C: Escolha da Atividade
    elif st.session_state.step_estudar == "escolher_atividade":
        if st.button("⬅️ Voltar", key="btn_voltar_ativ"):
            st.session_state.step_estudar = "upload_materiais"
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
            ],
            key="radio_ativ_estudar"
        )
        
        if st.button("Iniciar Atividade", key="btn_iniciar_ativ"):
            st.session_state.atividade_selecionada = atividade
            if atividade == "Exercícios":
                st.session_state.exercicios_gerados = gerar_30_exercicios()
            st.session_state.step_estudar = "executar_atividade"
            st.rerun()

    # PASSO D: Execução da Atividade com os 30 Exercícios e Validação Certo/Errado
    elif st.session_state.step_estudar == "executar_atividade":
        if st.button("⬅️ Voltar às Opções", key="btn_voltar_exec"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()
            
        st.title(f"🎯 {st.session_state.atividade_selecionada}")
        st.markdown(f"**Matéria:** {st.session_state.materia_escolhida_estudo}")
        
        if st.session_state.texto_estudo_livre:
            st.info(f"**Notas inseridas:**\n\n{st.session_state.texto_estudo_livre}")
        else:
            st.info("Nenhum apontamento inserido: a gerar exercícios padrão automaticamente com base na matéria.")
        
        st.markdown("---")
        
        if st.session_state.atividade_selecionada == "Exercícios":
            st.subheader("✏️ Conjunto de 30 Exercícios Práticos (Calcula o valor de x):")
            
            respostas_utilizador = {}
            for ex in st.session_state.exercicios_gerados:
                eid = ex["id"]
                st.markdown(f"**Exercício {eid}:**  $${ex['enunciado']}$$")
                respostas_utilizador[eid] = st.text_input(f"Valor de x para o exercício {eid}:", key=f"resp_ex_{eid}")
                st.markdown("---")
                
            if st.button("Submeter e Corrigir Respostas", key="btn_submeter_30"):
                acertos = 0
                st.subheader("📊 Resultados da Correção:")
                for ex in st.session_state.exercicios_gerados:
                    eid = ex["id"]
                    val_str = respostas_utilizador.get(eid, "").strip()
                    try:
                        val_num = float(val_str)
                        if abs(val_num - ex["resposta_correta"]) < 1e-3:
                            st.success(f"Exercício {eid} ({ex['enunciado']}): A tua resposta ({val_str}) está **Certa!** 🎉")
                            acertos += 1
                        else:
                            st.error(f"Exercício {eid} ({ex['enunciado']}): A tua resposta ({val_str}) está **Errada.** (A correta era {int(ex['resposta_correta']) if ex['resposta_correta'].is_integer() else ex['resposta_correta']})")
                    except ValueError:
                        st.warning(f"Exercício {eid}: Não introduziste um número válido (Resposta: '{val_str}').")
                
                st.markdown(f"### Pontuação Final: **{acertos} / 30**")
                
        elif st.session_state.atividade_selecionada == "Quizzes":
            st.subheader("❓ Quiz de Avaliação Teórica:")
            q_resp = st.radio("1. Numa equação do 1.º grau, qual é o objetivo principal?", ["Isolar a incógnita x", "Somar todos os números", "Eliminar o sinal de igual", "Nenhuma"], key="q_quiz_mat")
            if st.button("Submeter Quiz"):
                if q_resp == "Isolar a incógnita x":
                    st.success("Resposta Certa! 🎉")
                else:
                    st.error("Resposta Errada. O objetivo é isolar a incógnita x.")
                
        elif st.session_state.atividade_selecionada == "Transcrição e Consolidação de Conteúdos":
            st.subheader("📖 Resumo e Consolidação:")
            st.code(st.session_state.texto_estudo_livre if st.session_state.texto_estudo_livre else "Matéria base: Resolução de equações e propriedades algébricas fundamentais.", language="text")
            
        elif st.session_state.atividade_selecionada == "Flashcards":
            st.subheader("🃏 Flashcards de Memorização:")
            st.info("Pergunta: O que deves fazer quando passas um termo com sinal positivo para o outro lado da equação?\n\n(Clica em 'Ver Resposta')")
            if st.button("Ver Resposta"):
                st.success("Resposta: Passa com o sinal trocado (negativo / subtração).")

        st.markdown("---")
        if st.button("🔄 Recomeçar Estudo do Zero", key="btn_recomecar_total"):
            st.session_state.step_estudar = "escolher_materia"
            st.session_state.texto_estudo_livre = ""
            st.session_state.materiais_carregados = []
            st.rerun()
