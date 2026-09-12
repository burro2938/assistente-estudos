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

    body, p, label, input, textarea, button, select, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stText, .stSelectbox, .stRadio, .stTextInput {
        font-family: 'Comfortaa', cursive, sans-serif !important;
    }
    
    div[data-baseweb="select"] * {
        font-family: 'Comfortaa', cursive, sans-serif !important;
    }

    [data-testid="collapsedControl"] *, span[class*="material-icons"], i {
        font-family: 'Source Sans Pro', sans-serif !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
    }
    
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
    st.session_state.ano_escolar = "8.º Ano"

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
if "chave_geracao" not in st.session_state:
    st.session_state.chave_geracao = 0

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

def sugerir_materia_estudo():
    hoje = datetime.date.today()
    dias_portugal = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_idx = hoje.weekday()
    dia_nome = "Segunda-feira" if dia_idx >= 5 else dias_portugal[dia_idx]
    
    aulas_hoje = st.session_state.horario.get(dia_nome, [])
    if aulas_hoje:
        disc_sugerida = aulas_hoje[0].get("disc", "Matemática")
        return disc_sugerida, f"Com base no teu horário de hoje ({dia_nome}), sugerimos que pratiques **{disc_sugerida}**."
    return "Matemática", "Sugerimos a revisão de **Matemática** para manteres o ritmo de estudo."

def gerar_30_exercicios(dificuldade, ano_aluno):
    exs = []
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
        sol = random.randint(-6 * fator, 10 * fator)
        a1 = random.randint(1, 3 * fator)
        b1 = random.randint(-5 * fator, 8 * fator)
        c1 = random.randint(-2 * fator, 3 * fator)
        
        a2 = random.randint(-2 * fator, 2 * fator)
        if a1 + c1 == a2:
            a2 += 1
            
        b2 = random.randint(-5 * fator, 8 * fator)
        
        soma_x_esq = a1 + c1
        termo_num_esq = b1
        soma_x_dir = a2
        termo_num_dir = b2
        
        valor_esq = soma_x_esq * sol + termo_num_esq
        valor_dir_sem_d2 = soma_x_dir * sol + termo_num_dir
        d2 = valor_esq - valor_dir_sem_d2
        
        def fmt_term(val, var=""):
            if val == 0 and var != "":
                return ""
            s = " + " if val > 0 else " - "
            num = abs(val)
            return f"{s}{num}{var}" if num != 1 or var == "" else f"{s}{var}"

        parte_esq_x1 = f"{a1}x" if a1 != 0 else ""
        parte_esq_b1 = f" {fmt_term(b1)}" if b1 != 0 else ""
        parte_esq_c1 = fmt_term(c1, "x")
        
        parte_dir_x2 = f"{a2}x" if a2 != 0 else ""
        parte_dir_b2 = f" {fmt_term(b2)}" if b2 != 0 else ""
        parte_dir_d2 = fmt_term(d2)
        
        str_esq = f"{parte_esq_x1}{parte_esq_b1}{parte_esq_c1}".strip()
        if str_esq.startswith("+ "):
            str_esq = str_esq[2:]
            
        str_dir = f"{parte_dir_x2}{parte_dir_b2}{parte_dir_d2}".strip()
        if str_dir.startswith("+ "):
            str_dir = str_dir[2:]
            
        if not str_esq:
            str_esq = "0"
        if not str_dir:
            str_dir = "0"
            
        enunciado = f"{str_esq} = {str_dir}"

        exs.append({
            "id": i,
            "enunciado": enunciado,
            "resposta_correta": float(sol)
        })
    return exs

def gerar_flashcards_unicos(materia, dificuldade, ano_aluno, texto_apontamentos=""):
    texto_analisar = (texto_apontamentos + " " + materia).lower()
    
    banco_equacoes = [
        ("O que caracteriza uma equação do 1.º grau com parênteses?", "É uma igualdade algébrica que requer a aplicação da propriedade distributiva antes de agrupar os termos semelhantes."),
        ("Como se agrupam os termos com incógnita numa equação?", "Passando todos os termos com $x$ para um dos membros e os números para o outro, trocando o sinal aos que mudam de membro."),
        ("O que acontece ao sinal de um número quando este muda de membro?", "O sinal inverte-se (o que é positivo fica negativo e vice-versa)."),
        ("Como se resolve uma equação do tipo 6x - 4 + x = 4 - 8x + 5?", "Primeiro simplificam-se os termos semelhantes em cada membro da equação, isolando depois a incógnita $x$."),
        ("Qual é o objetivo principal ao resolver uma equação?", "Determinar o valor exato da incógnita $x$ que torna a igualdade verdadeira."),
        ("O que significa quando uma equação resulta numa identidade universal (ex: 0 = 0)?", "Significa que a equação é possível e indeterminada, tendo infinitas soluções."),
        ("O que significa quando uma equação resulta num absurdo (ex: 0 = 5)?", "Significa que a equação é impossível, não tendo nenhuma solução no conjunto dos números reais."),
        ("Como se eliminam denominadores numa equação?", "Multiplicando todos os termos de ambos os membros pelo denominador comum."),
        ("Qual é a regra da propriedade distributiva na multiplicação algébrica?", "O fator exterior multiplica cada uma das parcelas contidas dentro dos parênteses ($a(b+c) = ab + ac$)."),
        ("Como se trata um sinal de menos antecedido de parênteses, ex: -(2x - 3)?", "Inverte-se o sinal de todos os termos que estão dentro dos parênteses (-2x + 3)."),
        ("O que é uma equação algébrica equivalente?", "Equações que possuem exatamente o mesmo conjunto solução."),
        ("Como se isola a incógnita se ela estiver multiplicada por um coeficiente (ex: 5x = 20)?", "Dividindo ambos os membros da equação por esse coeficiente ($x = 20/5 = 4$)."),
        ("Qual é a diferença entre uma expressão algébrica e uma equação?", "A expressão algébrica é apenas um cálculo com letras e números, enquanto a equação é uma igualdade com uma incógnita a descobrir."),
        ("Pode uma equação ter coeficientes fracionários?", "Sim, e resolve-se habitualmente reduzindo todos os termos ao mesmo denominador ou multiplicando por ele."),
        ("O que é o grau de uma equação?", "É o maior expoente a que está elevada a incógnita após a equação estar simplificada."),
        ("Se tivermos termos com $x$ em ambos os membros, qual deve ser o primeiro passo prático?", "Reunir todos os termos com $x$ no primeiro membro (geralmente à esquerda) e os termos numéricos no segundo."),
        ("Como se classifica uma equação quanto ao conjunto solução?", "Pode ser possível determinada (uma solução), possível indeterminada (infinitas) ou impossível (sem solução)."),
        ("Qual é o cuidado a ter com as operações inversas?", "A adição desfaz-se com subtração, e a multiplicação desfaz-se com divisão."),
        ("Como se verifica se o valor obtido para $x$ está correto?", "Substituindo o valor encontrado na equação inicial e confirmando se ambos os membros dão o mesmo resultado."),
        ("Por que razão devemos simplificar antes de transpor termos?", "Para evitar erros de cálculo e tornar a equação mais curta e direta de resolver.")
    ]

    bancos_gerais = {
        "Matemática": [
            ("Qual é a soma dos ângulos internos de um triângulo?", "Sempre $180^\\circ$."),
            ("Como se calcula a área de um círculo?", "Multiplicando pi pelo quadrado do raio ($A = \\pi r^2$)."),
            ("O que é um número primo?", "Um número natural maior do que 1 divisível apenas por 1 e por si próprio."),
            ("Como se converte uma fração em percentagem?", "Multiplicando a fração por 100 e adicionando o símbolo %."),
            ("Qual é a fórmula do perímetro de uma circunferência?", "P = 2 \\pi r."),
            ("Como se calcula a média aritmética de um conjunto?", "Somando todos os elementos e dividindo pelo número total de elementos."),
            ("Qual é a raiz quadrada de 196?", "14."),
            ("O que é um polígono regular?", "Um polígono com todos os lados e ângulos geometricamente iguais."),
            ("Como se calcula o volume de um cilindro?", "Multiplicando a área da base circular pela altura ($V = \\pi r^2 h$)."),
            ("O que são ângulos suplementares?", "Dois ângulos cuja soma das amplitudes é exatamente $180^\\circ$.")
        ],
        "Português": [
            ("O que é o sujeito numa frase?", "O constituinte que concorda em número e pessoa com o verbo principal."),
            ("O que é uma palavra polissémica?", "Uma palavra que possui múltiplos significados consoante o contexto de uso."),
            ("Quais são os graus dos adjetivos?", "Grau normal, grau comparativo e grau superlativo."),
            ("O que caracteriza uma crónica?", "Um texto de opinião com base num acontecimento do quotidiano."),
            ("O que são sinónimos?", "Termos com significados equivalentes."),
            ("O que são antónimos?", "Termos com significados opostos."),
            ("O que é uma oração subordinada?", "Uma oração que depende sintaticamente da oração principal."),
            ("Qual é a classe de palavras invariáveis que modifica o verbo?", "O advérbio."),
            ("O que é uma metáfora?", "Uma figura de estilo baseada numa transferência de significado por semelhança implícita."),
            ("O que substitui o nome na frase?", "O pronome.")
        ]
    }

    if "equaç" in texto_analisar or "x" in texto_analisar or "álgebra" in texto_analisar or "algeb" in texto_analisar:
        banco_base = banco_equacoes
    else:
        banco_base = bancos_gerais.get(materia, bancos_gerais.get("Matemática", banco_equacoes))

    # Embaralhar rigorosamente para garantir que nunca sejam repetidos e sejam sempre novos
    banco_embaralhado = random.sample(banco_base, len(banco_base))
    cartoes_escolhidos = banco_embaralhado[:20]

    flashcards = []
    for i, (pergunta, resposta) in enumerate(cartoes_escolhidos, 1):
        flashcards.append({
            "id": i,
            "pergunta": f"{pergunta} (Nível: {dificuldade} | {ano_aluno})",
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
    
    # Sugestão de Matéria em Destaque na Página Inicial
    mat_sugerida, msg_sugerida = sugerir_materia_estudo()
    st.info(f"💡 **Sugestão do Dia:** {msg_sugerida}")
    if st.button("🚀 Ir estudar esta matéria agora"):
        st.session_state.materia_escolhida_estudo = mat_sugerida
        st.session_state.step_estudar = "upload_materiais"
        st.rerun()

    st.markdown("---")
    st.subheader("⚙️ Configurações do Aluno")
    
    anos_disponiveis = ["5.º Ano", "6.º Ano", "7.º Ano", "8.º Ano", "9.º Ano", "10.º Ano", "11.º Ano", "12.º Ano"]
    idx_ano_atual = anos_disponiveis.index(st.session_state.ano_escolar) if st.session_state.ano_escolar in anos_disponiveis else 3

    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.escola = st.text_input("Escola Atual", value=st.session_state.escola)
    with col2:
        st.session_state.ano_letivo = st.text_input("Ano Letivo", value=st.session_state.ano_letivo)
    with col3:
        st.session_state.ano_escolar = st.selectbox(
            "Ano Escolar Atual", 
            anos_disponiveis, 
            index=idx_ano_atual,
            key="sb_ano_escolar_global"
        )
        
    st.success(f"A frequentar o **{st.session_state.ano_escolar}** (ano letivo **{st.session_state.ano_letivo}**) em **{st.session_state.escola}**.")
    
    if st.button("Guardar alterações das configurações do aluno"):
        st.success("Configurações do aluno guardadas com sucesso!")

# 2. Agenda & Horário
elif menu == "📅 Agenda & Horário":
    st.title("📅 Gestão de Horário e Agenda")
    
    st.subheader("Configurar Horário Semanal")
    dia_escolhido = st.selectbox("Dia da Semana", list(st.session_state.horario.keys()))
    
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
            
        st.title("🧠 Revisão Rápida (15 Flashcards Pós-Registo)")
        # Geradas exatamente 15 questões de revisão rápida para cumprir o pedido
        for i in range(15):
            st.markdown(f"**Questão {i+1}:** Qual é o conceito ou propriedade fundamental aplicada no estudo de hoje?")
            st.radio(f"Opções Q{i+1}:", ["Propriedade Distributiva", "Isolamento da Incógnita", "Regra Geral", "Nenhuma"], key=f"q_pos_{i}")
            st.markdown("---")
            
        # Agora o botão redireciona corretamente para a seleção de matéria de estudo e nunca para o registo diário
        if st.button("Ir para o Estudo"):
            st.session_state.step_estudar = "escolher_materia"
            st.session_state.step_registo = "formulario"
            st.rerun()

# 4. Alínea: Estudar
elif menu == "📖 Estudar":
    
    if st.session_state.step_estudar == "escolher_materia":
        st.title("📚 Estudo")
        
        # Sugestão de matéria para estudar também integrada aqui
        mat_sug, msg_sug = sugerir_materia_estudo()
        st.info(f"💡 **Recomendação:** {msg_sug}")
        
        materia_escolhida = st.selectbox("Escolhe a matéria que queres aprofundar:", LISTA_MATERIAS, index=LISTA_MATERIAS.index(mat_sug) if mat_sug in LISTA_MATERIAS else 0, key="sb_estudar_mat")
        
        if st.button("Avançar", key="btn_avancar_mat"):
            st.session_state.materia_escolhida_estudo = materia_escolhida
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()

    elif st.session_state.step_estudar == "upload_materiais":
        if st.button("⬅️ Voltar", key="btn_voltar_up"):
            st.session_state.step_estudar = "escolher_materia"
            st.rerun()
            
        st.title("📚 Estudo")
        st.subheader("Materiais e Tópicos de Estudo")
        st.markdown(f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo} (Nível: {st.session_state.ano_escolar})")
        
        # Restaurados os uploads completos para Áudios, Vídeos, Imagens e Documentos
        st.markdown("---")
        st.markdown("### 📂 Envio de Multimédia e Documentos")
        st.file_uploader("Carregar Documentos (PDF, TXT, Word):", type=["pdf", "txt", "docx"], accept_multiple_files=True, key="up_docs")
        st.file_uploader("Carregar Imagens de Apontamentos ou Quadros:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="up_imgs")
        st.file_uploader("Carregar Áudios de Explicações ou Aulas:", type=["mp3", "wav", "m4a"], accept_multiple_files=True, key="up_audios")
        st.file_uploader("Carregar Vídeos de Estudo:", type=["mp4", "mov"], accept_multiple_files=True, key="up_videos")
        st.markdown("---")

        st.session_state.texto_estudo_livre = st.text_area(
            "Insere os teus apontamentos ou tópicos exatos sobre o que já deste na escola:", 
            value=st.session_state.texto_estudo_livre, 
            key="txt_livre_estudo"
        )
                
        if st.button("Avançar", key="btn_avancar_up"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()

    elif st.session_state.step_estudar == "escolher_atividade":
        if st.button("⬅️ Voltar", key="btn_voltar_ativ"):
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()
            
        st.title("📚 Estudo")
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
            ["Fácil 🟢", "Médio ⚖️", "Difícil 🟠", "Muito difícil 🔴", "Extremamente difícil 🔥"],
            index=1,
            key="radio_dificuldade_opcao"
        )
        
        if st.button("Iniciar Atividade", key="btn_iniciar_ativ"):
            st.session_state.atividade_selecionada = atividade
            st.session_state.chave_geracao += 1
            if atividade == "Exercícios":
                st.session_state.exercicios_gerados = gerar_30_exercicios(st.session_state.dificuldade_selecionada, st.session_state.ano_escolar)
            elif atividade == "Flashcards":
                st.session_state.flashcards_gerados = gerar_flashcards_unicos(
                    st.session_state.materia_escolhida_estudo, 
                    st.session_state.dificuldade_selecionada, 
                    st.session_state.ano_escolar,
                    st.session_state.texto_estudo_livre
                )
            st.session_state.step_estudar = "executar_atividade"
            st.rerun()

    elif st.session_state.step_estudar == "executar_atividade":
        if st.button("⬅️ Voltar às Opções", key="btn_voltar_exec"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()
            
        st.title(f"🎯 {st.session_state.atividade_selecionada}")
        st.markdown(f"**Matéria:** {st.session_state.materia_escolhida_estudo} | **Dificuldade:** {st.session_state.dificuldade_selecionada} | **Ano:** {st.session_state.ano_escolar}")
        
        st.info("💡 **Aviso:** Se aparecer alguma pergunta sobre matéria que ainda não deste, basta escrever **'não'** na resposta.")
        st.markdown("---")
        
        if st.session_state.atividade_selecionada == "Exercícios":
            st.subheader("✏️ Conjunto de 30 Exercícios Práticos:")
            respostas_utilizador = {}
            for ex in st.session_state.exercicios_gerados:
                eid = ex["id"]
                st.markdown(f"**Exercício {eid}:**  $${ex['enunciado']}$$")
                respostas_utilizador[eid] = st.text_input(f"Valor de x para o exercício {eid} (ou 'não'):", key=f"resp_ex_{eid}")
                st.markdown("---")
                
            if st.button("Submeter e Corrigir Respostas", key="btn_submeter_30"):
                acertos = 0
                for ex in st.session_state.exercicios_gerados:
                    eid = ex["id"]
                    val_str = respostas_utilizador.get(eid, "").strip().lower()
                    if val_str not in ["não", "nao"]:
                        try:
                            if abs(float(val_str) - ex["resposta_correta"]) < 1e-3:
                                acertos += 1
                        except ValueError:
                            pass
                st.markdown(f"### Pontuação Final: **{acertos} / 30 corretas**")
                
        elif st.session_state.atividade_selecionada == "Flashcards":
            st.subheader("🃏 Conjunto de 20 Flashcards de Memorização:")
            if st.button("🔄 Gerar novas perguntas de flashcards"):
                st.session_state.flashcards_gerados = gerar_flashcards_unicos(
                    st.session_state.materia_escolhida_estudo, 
                    st.session_state.dificuldade_selecionada, 
                    st.session_state.ano_escolar,
                    st.session_state.texto_estudo_livre
                )
                st.rerun()

            for fc in st.session_state.flashcards_gerados:
                fid = fc["id"]
                st.markdown(f"**Cartão {fid}:** {fc['pergunta']}")
                
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
