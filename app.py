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

# Estado da Sessão para Dados e Configurações do Aluno
if "logs" not in st.session_state:
    st.session_state.logs = []
if "escola" not in st.session_state:
    st.session_state.escola = "Escola Básica de Manhente"
if "ano_letivo" not in st.session_state:
    st.session_state.ano_letivo = "2026/2027"
if "ano_escolar" not in st.session_state:
    st.session_state.ano_escolar = "7.º Ano"

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
if "flashcards_gerados" not in st.session_state:
    st.session_state.flashcards_gerados = []
if "dificuldade_selecionada" not in st.session_state:
    st.session_state.dificuldade_selecionada = "Médio ⚖️"

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

# Função para gerar 30 exercícios adaptados à dificuldade e ao ano escolar
def gerar_30_exercicios(dificuldade, ano_aluno):
    exs = []
    random.seed(42)
    
    fator = 1
    if "Fácil" in dificuldade:
        fator = 1
    elif "Médio" in dificuldade:
        fator = 2
    elif "Difícil" in dificuldade:
        fator = 3
    elif "Muito" in dificuldade:
        fator = 4
    elif "Extremamente" in dificuldade:
        fator = 5

    for i in range(1, 31):
        a = random.randint(1 * fator, 5 * fator)
        b = random.randint(2 * fator, 15 * fator)
        sol = random.randint(1, 10 * fator)
        c = a * sol + b
        
        enunciado = f"{a}x + {b} = {c} (Ano base: {ano_aluno})"
        exs.append({
            "id": i,
            "enunciado": enunciado,
            "resposta_correta": float(sol)
        })
    return exs

# Função para gerar 20 Flashcards normais de estudo
def gerar_20_flashcards(materia, dificuldade, ano_aluno):
    flashcards = []
    random.seed(100)
    
    bancos_perguntas = {
        "Matemática": [
            ("O que é uma equação do 1.º grau?", "É uma igualdade com uma incógnita cujo expoente máximo é 1."),
            ("Como se isola a incógnita x numa adição simples?", "Passando o termo numérico para o outro membro com o sinal trocado (subtração)."),
            ("Qual é o valor neutro da multiplicação?", "O número 1."),
            ("O que representa o declive numa função afim?", "A taxa de variação da função."),
            ("Como se calcula a área de um retângulo?", "Multiplicando o comprimento pela largura ($A = c \\times l$)."),
            ("O que é um número primo?", "Um número natural maior do que 1 que tem apenas dois divisores: 1 e ele próprio."),
            ("Qual é a soma dos ângulos internos de um triângulo?", "$180^\\circ$."),
            ("Como se converte uma fração em percentagem?", "Multiplicando o numerador pelo denominador por 100 ou achando a fração equivalente com denominador 100."),
            ("O que significa simplificar uma fração?", "Dividir o numerador e o denominador pelo mesmo número diferente de zero até obter uma fração irredutível."),
            ("Qual é a fórmula do perímetro de uma circunferência?", "$P = 2 \\pi r$."),
            ("O que é uma proporção?", "Uma igualdade entre duas razões."),
            ("Como se calcula a média aritmética?", "Somando todos os valores e dividindo pelo número total de valores."),
            ("O que indica um expoente negativo num número?", "Indica o inverso da base elevado ao expoente positivo ($a^{-n} = \\frac{1}{a^n}$)."),
            ("Qual é a raiz quadrada de 144?", "12."),
            ("O que é um polígono regular?", "Um polígono com todos os lados e ângulos internos iguais."),
            ("Como se calcula o volume de um paralelepípedo?", "Multiplicando o comprimento, a largura e a altura ($V = c \\times l \\times a$)."),
            ("O que é uma simetria axial?", "Uma reflexão em relação a uma reta chamada eixo de simetria."),
            ("Qual é o valor de qualquer número (diferente de zero) elevado a zero?", "1."),
            ("O que são ângulos opostos pelo vértice?", "São ângulos que partilham o mesmo vértice e cujos lados são semirretas opostas; são iguais."),
            (f"Qual é o objetivo principal do estudo no {ano_aluno}?", "Consolidar bases matemáticas e aplicar raciocínio lógico avançado.")
        ],
        "Português": [
            ("O que é o sujeito numa frase?", "O ser ou objeto que pratica ou sofre a ação expressa pelo verbo."),
            ("Diferencia predicado nominal de predicado verbal:", "O predicado verbal tem um verbo principal; o predicado nominal tem um verbo copulativo e um predicado."),
            ("O que é uma palavra polissémica?", "Uma palavra que possui vários significados consoante o contexto."),
            ("Quais são os graus dos adjetivos?", "Grau normal, grau comparativo e grau superlativo."),
            ("O que é a regência verbal?", "A relação de dependência entre um verbo e o seu complemento."),
            ("O que caracteriza uma crónica literária?", "Um texto curto baseado num facto do quotidiano com uma visão crítica ou irónica."),
            ("O que são sinónimos?", "Palavras com significados iguais ou semelhantes."),
            ("O que são antónimos?", "Palavras com significados opostos."),
            ("O que é uma oração subordinada?", "Uma oração que depende sintaticamente de outra (oração principal)."),
            ("Qual é a função de um advérbio?", "Modificar o sentido de um verbo, de um adjetivo ou de outro advérbio."),
            ("O que é a acentuação grave (palavras graves)?", "Palavras cuja tonicidade recai na penúltima sílaba."),
            ("O que é uma metáfora?", "Uma figura de estilo baseada numa comparação implícita."),
            ("O que é a aliteração?", "A repetição de sons consonânticos semelhantes num verso ou frase."),
            ("O que é umneologismo?", "A criação de uma palavra nova numa língua."),
            ("Qual é a estrutura típica de uma narrativa?", "Introdução, desenvolvimento (complicação e clímax) e conclusão."),
            ("O que é um pronome pessoal?", "Um pronome que substitui o nome e indica as pessoas do discurso (eu, tu, ele...)."),
            ("O que é o pretérito mais-que-perfeito?", "Um tempo verbal que indica uma ação passada anterior a outra também passada."),
            ("O que é uma antítese?", "A aproximação de palavras com sentidos opostos na mesma frase."),
            ("O que é um ditongo?", "A sequência de uma vogal e uma semivogal (ou vice-versa) na mesma sílaba."),
            (f"Como aplicar a ortografia correta no {ano_aluno}?", "Através da leitura regular e prática de escrita formal.")
        ]
    }
    
    # Selecionar banco específico ou genérico
    banco = bancos_perguntas.get(materia, bancos_perguntas["Matemática"])
    
    for i in range(1, 21):
        pergunta, resposta = banco[(i - 1) % len(banco)]
        flashcards.append({
            "id": i,
            "pergunta": f"{pergunta} (Nível: {dificuldade})",
            "resposta": resposta
        })
    return flashcards

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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.escola = st.text_input("Escola Atual", value=st.session_state.escola)
    with col2:
        st.session_state.ano_letivo = st.text_input("Ano Letivo", value=st.session_state.ano_letivo)
    with col3:
        st.session_state.ano_escolar = st.selectbox("Ano Escolar Atual", ["5.º Ano", "6.º Ano", "7.º Ano", "8.º Ano", "9.º Ano", "10.º Ano", "11.º Ano", "12.º Ano"], index=2)
        
    st.success(f"A frequentar o **{st.session_state.ano_escolar}** (ano letivo **{st.session_state.ano_letivo}**) em **{st.session_state.escola}**.")

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
        st.markdown(f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo} (Nível: {st.session_state.ano_escolar})")
        
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

    # PASSO C: Escolha da Atividade e Botão de Dificuldade
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
        
        st.markdown("---")
        st.session_state.dificuldade_selecionada = st.radio(
            "⚡ Seleciona a Dificuldade:",
            [
                "Fácil 🟢",
                "Médio ⚖️",
                "Difícil 🟠",
                "Muito difícil 🔴",
                "Extremamente difícil 🔥"
            ],
            index=["Fácil 🟢", "Médio ⚖️", "Difícil 🟠", "Muito difícil 🔴", "Extremamente difícil 🔥"].index(st.session_state.dificuldade_selecionada) if st.session_state.dificuldade_selecionada in ["Fácil 🟢", "Médio ⚖️", "Difícil 🟠", "Muito difícil 🔴", "Extremamente difícil 🔥"] else 1,
            key="radio_dificuldade_opcao"
        )
        
        if st.button("Iniciar Atividade", key="btn_iniciar_ativ"):
            st.session_state.atividade_selecionada = atividade
            if atividade == "Exercícios":
                st.session_state.exercicios_gerados = gerar_30_exercicios(st.session_state.dificuldade_selecionada, st.session_state.ano_escolar)
            elif atividade == "Flashcards":
                st.session_state.flashcards_gerados = gerar_20_flashcards(st.session_state.materia_escolhida_estudo, st.session_state.dificuldade_selecionada, st.session_state.ano_escolar)
            st.session_state.step_estudar = "executar_atividade"
            st.rerun()

    # PASSO D: Execução da Atividade
    elif st.session_state.step_estudar == "executar_atividade":
        if st.button("⬅️ Voltar às Opções", key="btn_voltar_exec"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()
            
        st.title(f"🎯 {st.session_state.atividade_selecionada}")
        st.markdown(f"**Matéria:** {st.session_state.materia_escolhida_estudo} | **Dificuldade:** {st.session_state.dificuldade_selecionada} | **Ano:** {st.session_state.ano_escolar}")
        
        st.info("💡 **Aviso:** Se aparecer alguma pergunta sobre matéria que ainda não deste/aprendeste, basta escrever **'não'** na resposta (nos exercícios) ou assinalar.")
        
        st.markdown("---")
        
        if st.session_state.atividade_selecionada == "Exercícios":
            st.subheader("✏️ Conjunto de 30 Exercícios Práticos:")
            
            respostas_utilizador = {}
            for ex in st.session_state.exercicios_gerados:
                eid = ex["id"]
                st.markdown(f"**Exercício {eid}:**  $${ex['enunciado']}$$")
                respostas_utilizador[eid] = st.text_input(f"Valor de x para o exercício {eid} (ou escreve 'não' se ainda não aprendeste):", key=f"resp_ex_{eid}")
                st.markdown("---")
                
            if st.button("Submeter e Corrigir Respostas", key="btn_submeter_30"):
                acertos = 0
                nao_aprendidos = 0
                st.subheader("📊 Resultados da Correção:")
                for ex in st.session_state.exercicios_gerados:
                    eid = ex["id"]
                    val_str = respostas_utilizador.get(eid, "").strip().lower()
                    
                    if val_str == "não" or val_str == "nao":
                        st.info(f"Exercício {eid}: Marcado como **não aprendido** ('não').")
                        nao_aprendidos += 1
                    else:
                        try:
                            val_num = float(val_str)
                            if abs(val_num - ex["resposta_correta"]) < 1e-3:
                                st.success(f"Exercício {eid} ({ex['enunciado']}): A tua resposta ({val_str}) está **Certa!** 🎉")
                                acertos += 1
                            else:
                                st.error(f"Exercício {eid} ({ex['enunciado']}): A tua resposta ({val_str}) está **Errada.** (A correta era {int(ex['resposta_correta']) if ex['resposta_correta'].is_integer() else ex['resposta_correta']})")
                        except ValueError:
                            st.warning(f"Exercício {eid}: Valor inválido introduzido ('{val_str}').")
                
                st.markdown(f"### Pontuação Final: **{acertos} / 30 corretas** ({nao_aprendidos} assinaladas com 'não')")
                
        elif st.session_state.atividade_selecionada == "Quizzes":
            st.subheader("❓ Quiz de Avaliação Teórica:")
            q_resp = st.radio("1. Numa matéria, se ainda não deste o conteúdo correspondente, o que deves responder?", ["não", "Sim", "Talvez", "Nenhuma"], key="q_quiz_mat")
            if st.button("Submeter Quiz"):
                if q_resp.lower() == "não" or q_resp.lower() == "nao":
                    st.success("Resposta Certa! 🎉 (Utilizaste a palavra-chave correta)")
                else:
                    st.error("Resposta Errada. A palavra-chave correta é 'não'.")
                
        elif st.session_state.atividade_selecionada == "Transcrição e Consolidação de Conteúdos":
            st.subheader("📖 Resumo e Consolidação:")
            st.code(st.session_state.texto_estudo_livre if st.session_state.texto_estudo_livre else f"Matéria base para o {st.session_state.ano_escolar} e nível {st.session_state.dificuldade_selecionada}.", language="text")
            
        elif st.session_state.atividade_selecionada == "Flashcards":
            st.subheader("🃏 Conjunto de 20 Flashcards de Memorização:")
            st.write("Clica no botão respetivo de cada cartão para revelares a resposta e testares os teus conhecimentos:")
            
            for fc in st.session_state.flashcards_gerados:
                fid = fc["id"]
                st.markdown(f"**Cartão {fid}:** {fc['pergunta']}")
                
                # Estado individual para cada flashcard
                if f"mostrar_fc_{fid}" not in st.session_state:
                    st.session_state[f"mostrar_fc_{fid}"] = False
                    
                col_b1, col_b2 = st.columns([1, 4])
                with col_b1:
                    if st.button(f"Virar #{fid}", key=f"btn_virar_{fid}"):
                        st.session_state[f"mostrar_fc_{fid}"] = not st.session_state[f"mostrar_fc_{fid}"]
                        st.rerun()
                with col_b2:
                    if st.session_state[f"mostrar_fc_{fid}"]:
                        st.success(f"**Resposta:** {fc['resposta']}")
                    else:
                        st.info("*(Resposta oculta - clica em 'Virar' para ver)*")
                st.markdown("---")

        st.markdown("---")
        if st.button("🔄 Recomeçar Estudo do Zero", key="btn_recomecar_total"):
            st.session_state.step_estudar = "escolher_materia"
            st.session_state.texto_estudo_livre = ""
            st.session_state.materiais_carregados = []
            st.rerun()
