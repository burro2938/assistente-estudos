import streamlit as st
import datetime
import random
import calendar

# Configuração da Página
st.set_page_config(
    page_title="Assistente de Estudos",
    page_icon="",
    layout="wide"
)

# Importar a fonte Comfortaa e aplicar corretamente mantendo os ícones intactos
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@400;700&display=swap');
    body, p, label, input, textarea, button, select, h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stText, stSelectbox, stRadio, .stTextInput {
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
    st.session_state.ano_escolar = "8.° Ano"
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
            {"hora": "08:30 - 09:15", "disc": "História"},
            {"hora": "09:25 - 10:10", "disc": "Ciências Naturais"},
            {"hora": "10:30 - 11:15", "disc": "Francês"},
            {"hora": "11:25 - 12:10", "disc": "Físico-Química"}
        ],
        "Sexta-feira": [
            {"hora": "08:30 - 09:15", "disc": "Português"},
            {"hora": "09:25 - 10:10", "disc": "Matemática"},
            {"hora": "10:30 - 11:15", "disc": "Educação Visual"},
            {"hora": "11:25 - 12:10", "disc": "TIC"}
        ]
    }
if "testes" not in st.session_state:
    st.session_state.testes = []
if "step_registo" not in st.session_state:
    st.session_state.step_registo = "formulario"
if "step_estudar" not in st.session_state:
    st.session_state.step_estudar = "escolher_materia"
if "materia_escolhida_estudo" not in st.session_state:
    st.session_state.materia_escolhida_estudo = ""
if "texto_estudo_livre" not in st.session_state:
    st.session_state.texto_estudo_livre = ""
if "num_aulas_extra" not in st.session_state:
    st.session_state.num_aulas_extra = {}
if "exercicios_gerados" not in st.session_state:
    st.session_state.exercicios_gerados = []
if "flashcards_gerados" not in st.session_state:
    st.session_state.flashcards_gerados = []
if "flashcards_pos_gerados" not in st.session_state:
    st.session_state.flashcards_pos_gerados = []
if "dificuldade_selecionada" not in st.session_state:
    st.session_state.dificuldade_selecionada = "Médio"
if "chave_geracao" not in st.session_state:
    st.session_state.chave_geracao = 0
if "atividade_selecionada" not in st.session_state:
    st.session_state.atividade_selecionada = "Exercícios"

# Estado para navegação do calendário e detalhe do dia
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None
if "cal_year" not in st.session_state:
    st.session_state.cal_year = datetime.date.today().year
if "cal_month" not in st.session_state:
    st.session_state.cal_month = datetime.date.today().month

LISTA_MATERIAS = [
    "Matemática",
    "Português",
    "Inglês",
    "Físico-Química",
    "Francês",
    "Ciências Naturais",
    "História",
    "Geografia",
    "TIC (Tecnologias de Informação e Comunicação)",
    "Educação Física",
    "Educação Visual",
    "Educação Tecnológica",
    "Cidadania e Desenvolvimento"
]

def gerar_30_exercicios(dificuldade, ano_aluno, texto_contexto=""):
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
        
    texto_inf = texto_contexto.lower()
    eh_equacoes = "equaç" in texto_inf or "x" in texto_inf or "álgebra" in texto_inf
    
    for i in range(1, 31):
        if eh_equacoes:
            sol = random.randint(-8 * fator, 12 * fator)
            a1 = random.randint(1, 4 * fator)
            b1 = random.randint(-6 * fator, 9 * fator)
            c1 = random.randint(-3 * fator, 4 * fator)
            a2 = random.randint(-3 * fator, 3 * fator)
            if a1 + c1 == a2:
                a2 += 1
            b2 = random.randint(-6 * fator, 9 * fator)
            
            valor_esq = (a1 + c1) * sol + b1
            valor_dir_sem_d2 = a2 * sol + b2
            d2 = valor_esq - valor_dir_sem_d2
            
            def fmt_term(val, var=""):
                if val == 0 and var != "":
                    return ""
                s = "+" if val > 0 else " -"
                num = abs(val)
                return f"{s}{num}{var}" if num != 1 or var == "" else f"{s}{var}"
            
            p_esq = f"{a1}x" if a1 != 0 else ""
            p_b1 = f" {fmt_term(b1)}" if b1 != 0 else ""
            p_c1 = fmt_term(c1, "x")
            p_esq_total = f"{p_esq}{p_b1}{p_c1}".strip()
            if p_esq_total.startswith("+ "): 
                p_esq_total = p_esq_total[2:]
                
            p_dir_x2 = f"{a2}x" if a2 != 0 else ""
            p_dir_b2 = f" {fmt_term(b2)}" if b2 != 0 else ""
            p_dir_d2 = fmt_term(d2)
            p_dir_total = f"{p_dir_x2}{p_dir_b2}{p_dir_d2}".strip()
            if p_dir_total.startswith("+"): 
                p_dir_total = p_dir_total[2:]
                
            if not p_esq_total: 
                p_esq_total = "0"
            if not p_dir_total: 
                p_dir_total = "0"
                
            enunciado = f"{p_esq_total} = {p_dir_total}"
            resp = float(sol)
        else:
            n1 = random.randint(2 * fator, 15 * fator)
            n2 = random.randint(2 * fator, 15 * fator)
            enunciado = f"Calcule o valor de {n1} * {n2} + {i * 2}"
            resp = float(n1 * n2 + i * 2)
            
        exs.append({
            "id": i,
            "enunciado": enunciado,
            "resposta_correta": resp
        })
    return exs

def gerar_flashcards_personalizados(quantidade, materia, dificuldade, ano_aluno, texto_apontamentos=""):
    flashcards = []
    texto_limpo = texto_apontamentos.strip()
    
    # Extração detalhada e rica de apontamentos inseridos pelo utilizador para garantir flashcards específicos
    if texto_limpo:
        linhas_ou_frases = [f.strip() for f in texto_limpo.replace("\n", ".").split(".") if f.strip()]
        if not linhas_ou_frases:
            linhas_ou_frases = [texto_limpo]
            
        for i in range(1, quantidade + 1):
            frase_base = linhas_ou_frases[(i - 1) % len(linhas_ou_frases)]
            tipo_pergunta = i % 4
            
            if tipo_pergunta == 0:
                perq = f"Aprofundamento de {materia} ({ano_aluno}): Explica rigorosamente o conceito apresentado em '{frase_base}'."
                resp = f"Análise detalhada: No âmbito de {materia}, este princípio estabelece que {frase_base}, sendo fulcral para a resolução de problemas práticos e consolidação teórica."
            elif tipo_pergunta == 1:
                perq = f"Aplicação prática em {materia}: Como se emprega diretamente a regra referida em '{frase_base}'?"
                resp = f"Resolução: A aplicação correta exige considerar que {frase_base}, garantindo o rigor científico e metodológico exigido no programa escolar vigente."
            elif tipo_pergunta == 2:
                perq = f"Identificação concisa: Qual é o postulado central contido em '{frase_base}'?"
                resp = f"Conclusão teórica: O conceito central baseia-se exatamente em prever que {frase_base}, fundamentando os raciocínios subsequentes."
            else:
                perq = f"Avaliação de competências em {materia}: Justifica a relevância de dominar o tópico '{frase_base}'."
                resp = f"Justificação pedagógica: É indispensável porque {frase_base}, constituindo matéria estruturante e de alta relevância para as avaliações."
                
            flashcards.append({
                "id": i,
                "pergunta": perq,
                "resposta": resp
            })
        return flashcards

    # Bancos curriculares específicos e aprofundados por disciplina (completamente detalhados) para o programa escolar em Portugal
    banco_ingles = [
        ("Como se aplica o Present Simple para ações habituais com a terceira pessoa do singular (He/She/It)?", "Acrescenta-se o sufixo -s ou -es ao verbo principal na afirmativa (Ex: She plays tennis; He watches TV)."),
        ("Qual é a estrutura correta para formar frases na negativa no Present Continuous?", "Sujeito + verbo to be (am/is/are) + not + verbo com terminação -ing (Ex: They aren't listening)."),
        ("Quando se deve utilizar os pronomes relativos 'who' e 'which' em inglês?", "'Who' emprega-se estritamente para pessoas, ao passo que 'which' se refere a objetos ou animais."),
        ("Como se formam os comparativos de superioridade com adjetivos longos (ex: expensive)?", "Utiliza-se a estrutura 'more + adjetivo + than' (Ex: This phone is more expensive than that one)."),
        ("Qual é a regra geral para formar o superlativo de adjetivos curtos (ex: tall)?", "Usa-se 'the + adjetivo com terminação -est' (Ex: He is the tallest student in the class)."),
        ("Quais são os auxiliares utilizados no Past Simple para frases interrogativas e negativas?", "O auxiliar 'did' para perguntas e 'didn't' para a forma negativa, seguido do verbo no infinitivo."),
        ("Como se exprimem planos futuros utilizando a estrutura 'to be going to'?", "Sujeito + verbo to be conjugado + going to + verbo principal no infinitivo (Ex: We are going to visit Rome)."),
        ("Qual é a diferença de uso entre os quantificadores 'much' e 'many'?", "'Much' utiliza-se exclusivamente com substantivos incontáveis, enquanto 'many' aplica-se a substantivos contáveis no plural."),
        ("Como se conjuga o verbo modal 'should' para dar conselhos ou recomendações?", "Usa-se 'should' (ou 'shouldn't' na negativa) seguido do infinitivo sem 'to' (Ex: You should study harder)."),
        ("Em que contextos se empregam os advérbios de frequência (always, never, often)?", "Colocam-se habitualmente antes do verbo principal, mas após o verbo to be (Ex: She is always punctual)."),
        ("Como se formam as frases interrogativas no Present Simple com verbos principais ordinários?", "Utiliza-se o auxiliar 'Do' (ou 'Does' para a 3.ª pessoa do singular) no início da frase, seguido do sujeito e do verbo principal no infinitivo sem 'to'."),
        ("Qual é a função e a colocação dos pronomes objectivos (object pronouns) numa frase em inglês?", "Substituem o nome e colocam-se habitualmente após o verbo principal ou após uma preposição (Ex: Give it to me).")
    ]
    banco_matematica = [
        ("O que define uma equação do 1.º grau redutível com parênteses?", "Uma igualdade algébrica que obriga à aplicação prévia da propriedade distributiva da multiplicação sobre a adição."),
        ("Qual é o procedimento algébrico correto ao transpor termos entre os membros de uma equação?", "Isolar os termos com incógnita num membro e os valores numéricos no oposto, invertendo simetricamente o sinal de cada termo transposto."),
        ("Como se enuncia o Teorema de Pitágoras num triângulo retângulo?", "O quadrado da hipotenusa é estritamente igual à soma dos quadrados dos catetos ($a^2 = b^2 + c^2$)."),
        ("O que caracteriza uma função afim e qual é a sua expressão analítica geral?", "É uma função da forma $f(x) = mx + b$, cujo gráfico cartesiano representa uma linha reta não vertical."),
        ("Como se calcula a área lateral e total de um cilindro circular reto?", "Área lateral = $2\pi r h$; Área total = Área lateral mais a área das duas bases circulares ($2\pi r^2$)."),
        ("O que representa a frequência relativa de um dado num conjunto estatístico?", "O quociente entre a frequência absoluta desse dado e o número total de observações efetuadas."),
        ("Qual é a regra fundamental para somar ou subtrair frações algébricas?", "Reduzir obrigatoriamente as frações ao mesmo denominador comum antes de operar com os numeradores."),
        ("Como se determinam as coordenadas do ponto médio de um segmento de reta num referencial?", "Calculando a média aritmética das coordenadas correspondentes dos dois pontos extremos."),
        ("Qual é a propriedade distributiva da multiplicação em relação à adição algébrica?", "Permite multiplicar um número por uma soma distribuindo-o por cada uma das parcelas: $a(b + c) = ab + ac$."),
        ("Como se calcula a probabilidade de um acontecimento num espaço de resultados equiprováveis?", "Através do quociente entre o número de casos favoráveis e o número total de casos possíveis do espaço amostral.")
    ]
    banco_portugues = [
        ("O que distingue uma oração subordinada adverbial causal de uma final?", "A causal indica a causa ou motivo da ação principal (introduzida por 'porque'), ao passo que a final exprime a intenção ou objetivo."),
        ("Quais são as funções sintáticas internas do grupo verbal que completam o sentido do verbo?", "O complemento direto, o complemento indireto, o complemento oblíquo e o predicativo do sujeito."),
        ("Como se caracteriza o tom lírico e temático na poesia de Amália Rodrigues?", "Pela expressão profunda de melancolia, saudade, destino e vivência trágica do quotidiano português."),
        ("O que define estruturalmente uma crónica jornalística moderna?", "Um texto literário de cariz brevíssimo baseado num acontecimento trivial do dia a dia, tratado com ironia ou reflexão crítica."),
        ("Quais são os graus dos adjetivos e como se divide o grau superlativo?", "Grau normal, comparativo (superioridade, igualdade, inferioridade) e superlativo (relativo e absoluto sintético/analítico)."),
        ("Qual é a função do sujeito poético num texto lírico?", "Representa a voz que enuncia o poema, transmitindo sentimentos, emoções e estados de alma na primeira pessoa."),
        ("O que caracteriza uma oração subordinada relativa restritiva?", "Limita ou restringe o sentido do antecedente a que se refere, sem vir isolada por vírgulas na representação gráfica.")
    ]
    banco_historia = [
        ("Quais foram os principais fatores determinantes do expansionismo marítimo português no século XV?", "A centralização régia precoce, a ausência de conflitos internos graves, o conhecimento náutico avançado e a busca de rotas comerciais diretas para o Oriente."),
        ("O que caracterizava a sociedade de ordens durante o Antigo Regime europeu?", "Uma divisão estamental rígida composta pelo Clero, pela Nobreza (ordens privilegiadas) e pelo Povo ou Terceiro Estado."),
        ("Qual foi o alcance geoestratégico do Tratado de Tordesilhas assinado em 1494?", "Estabeleceu um meridiano demarcador a 370 léguas a oeste de Cabo Verde, dividindo as esferas de exploração ultramarina entre Portugal e Espanha."),
        ("Quais foram os ideais fundamentais consagrados pela Revolução Francesa de 1789?", "A Liberdade, a Igualdade e a Fraternidade, sintetizados na Declaração dos Direitos do Homem e do Cidadão."),
        ("Qual foi o papel desempenhado pelas feiras medievais na dinamização económica europeia?", "Estimularam o renascimento urbano, o comércio monetário de longa distância e a emancipação económica dos burgueses.")
    ]
    banco_ciencias = [
        ("Qual é a diferença estrutural fundamental entre células procarióticas e eucarióticas?", "A célula eucariótica possui um núcleo verdadeiro delimitado por invólucro nuclear e organelos membranares; a procariótica carece de núcleo organizado."),
        ("Em que organelo celular ocorre o processo de respiração aeróbia e qual é a sua finalidade?", "Ocorre nas mitocôndrias e destina-se a libertar energia útil para as atividades celulares através da oxidação de compostos orgânicos."),
        ("Quais são os reagentes essenciais e os produtos resultantes da fotossíntese?", "Reagentes: dióxido de carbono, água e energia solar; Produtos: glicose (matéria orgânica) e oxigénio molecular."),
        ("Como se define a tectónica de placas na dinâmica interna da Terra?", "A teoria científica que postula que a litosfera está fraturada em blocos rígidos (placas) que se movimentam sobre a astenosfera devido a correntes de convecção."),
        ("Qual é a função desempenhada pelo sistema linfático no organismo humano?", "Drenar o excesso de líquido intersticial, absorver lípidos ao nível intestinal e assegurar a defesa imunitária do corpo.")
    ]
    banco_fisico_quimica = [
        ("Qual é a distinção crucial entre uma transformação física e uma transformação química?", "Na transformação física não se alteram as propriedades químicas nem se formam novas substâncias; na química ocorre rearranjo atómico com formação de novas substâncias."),
        ("Como se calcula a velocidade média de um corpo em movimento retilíneo?", "Através do quociente entre a distância total percorrida e o intervalo de tempo gasto ($v = d / \Delta t$)."),
        ("O que representa o número mássico de um átomo na tabela periódica?", "A soma total do número de protões e de neutrões presentes no núcleo atómico."),
        ("O que estabelece a Lei da Conservação da Massa (Lavoisier) nas reações químicas?", "Num sistema fechado, a massa total das substâncias reagentes é estritamente igual à massa total dos produtos da reação.")
    ]

    materia_inf = materia.lower()
    if "matemática" in materia_inf or "matematica" in materia_inf:
        banco_base = banco_matematica
    elif "português" in materia_inf or "portugues" in materia_inf:
        banco_base = banco_portugues
    elif "inglês" in materia_inf or "ingles" in materia_inf or "english" in materia_inf:
        banco_base = banco_ingles
    elif "história" in materia_inf or "historia" in materia_inf:
        banco_base = banco_historia
    elif "ciências" in materia_inf or "ciencias" in materia_inf:
        banco_base = banco_ciencias
    elif "físico-química" in materia_inf or "fisico-quimica" in materia_inf:
        banco_base = banco_fisico_quimica
    else:
        banco_base = [
            (f"Quais são os tópicos fundamentais e teóricos abordados em {materia} no {ano_aluno}?", f"O domínio da disciplina exige a compreensão rigorosa de conceitos essenciais, regras metodológicas e aplicação prática em {materia}."),
            (f"Como se estruturam os principais teoremas ou preceitos em {materia}?", f"Através da análise sistemática, dedução lógica e memorização ativa dos conteúdos lecionados na escola."),
            (f"Quais são os erros mais frequentes a acautelar ao estudar esta matéria?", f"A desatenção aos critérios de rigor científico e a falha na fundamentação teórica dos conceitos."),
            (f"Qual é a utilidade prática dos saberes adquiridos em {materia} no contexto académico?", f"Permitem consolidar o raciocínio crítico e assegurar o sucesso nas avaliações do {ano_aluno}.")
        ]

    amostra = random.sample(banco_base, min(len(banco_base), quantidade))
    while len(amostra) < quantidade:
        amostra.append(random.choice(banco_base))
        
    for i, (pergunta, resposta) in enumerate(amostra, 1):
        flashcards.append({
            "id": i,
            "pergunta": f"{pergunta} [Disciplina: {materia} | Nível: {dificuldade} | {ano_aluno}]",
            "resposta": resposta
        })
    return flashcards

def obter_recomendacao_inteligente():
    hoje_obj = datetime.date.today()
    dias_pt = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_idx = hoje_obj.weekday()
    dia_nome = "Segunda-feira" if dia_idx >= 5 else dias_pt[dia_idx]
    aulas_hoje = st.session_state.horario.get(dia_nome, [])
    if st.session_state.logs:
        ultimo_registo = st.session_state.logs[-1]
        resumos_recentes = list(ultimo_registo.get("resumos", {}).keys())
        if resumos_recentes:
            materia_recente = resumos_recentes[0]
            return f"Com base no teu horário de hoje ({dia_nome}) e no que estudaste recentemente ({materia_recente}), sugerimos que dês continuidade a essa matéria ou pratiques exercícios práticos relacionados."
    sugestao_materia = aulas_hoje[0]["disc"] if aulas_hoje else "Matemática"
    return f"Com base no teu horário de hoje ({dia_nome}), sugerimos que pratiques {sugestao_materia}."

# Barra Lateral de Navegação
st.sidebar.markdown("# Menu Principal")
menu = st.sidebar.radio(
    "Navegar para:",
    [
        "Início & Escola",
        "Calendário",
        "Agenda & Horário",
        "Registo Diário",
        "Estudar"
    ]
)

# 1. Início & Escola
if menu == "Início & Escola":
    st.title("Meu Assistente de Estudos")
    st.write("Bem-vindo ao teu espaço centralizado de organização escolar e revisão!")
    recomendacao_texto = obter_recomendacao_inteligente()
    st.info(f"**Sugestão de Estudo:** {recomendacao_texto}")
    st.markdown("---")
    st.subheader("Configurações do Aluno")
    
    anos_disponiveis = ["5.° Ano", "6.º Ano", "7.º Ano", "8.º Ano", "9.º Ano", "10.° Ano", "11.° Ano", "12.º Ano"]
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

# 2. Calendário
elif menu == "Calendário":
    st.title("Calendário")
    if st.session_state.selected_date is not None:
        d_str = st.session_state.selected_date.strftime("%d/%m/%Y")
        st.subheader(f"Detalhes do dia {d_str}")
        registo_encontrado = None
        for log in st.session_state.logs:
            if log.get("data") == str(st.session_state.selected_date):
                registo_encontrado = log
                break
        if registo_encontrado:
            st.markdown("### Matéria Estudada / Resumos:")
            for disc, res in registo_encontrado.get("resumos", {}).items():
                if res:
                    st.markdown(f"- <span style='font-size: 1.3em;'>**{disc}**: {res}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"- <span style='font-size: 1.3em;'>**{disc}**: *(Sem apontamentos escritos)*</span>", unsafe_allow_html=True)
            metodo_registado = registo_encontrado.get("metodo", "Exercícios")
            st.markdown("### Ficheiros e Métodos de Estudo:")
            st.markdown(f"- <span style='font-size: 1.3em;'>**Método utilizado:** {metodo_registado}</span>", unsafe_allow_html=True)
        else:
            st.info("Não existem registos de estudo guardados para este dia.")
            
        testes_dia = [t for t in st.session_state.testes if t.get("data") == str(st.session_state.selected_date)]
        if testes_dia:
            st.markdown("### Testes Agendados para este Dia:")
            for t in testes_dia:
                st.markdown(f"- <span style='font-size: 1.3em;'>**Teste de {t['materia']}**</span>", unsafe_allow_html=True)
        if st.button("Voltar ao Calendário Mensal"):
            st.session_state.selected_date = None
            st.rerun()
    else:
        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
        with col_m1:
            if st.button("Mês Anterior"):
                if st.session_state.cal_month == 1:
                    st.session_state.cal_month = 12
                    st.session_state.cal_year -= 1
                else:
                    st.session_state.cal_month -= 1
                st.rerun()
        with col_m2:
            meses_nomes = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            st.markdown(f"<h3 style='text-align: center;'>{meses_nomes[st.session_state.cal_month]} {st.session_state.cal_year}</h3>", unsafe_allow_html=True)
        with col_m3:
            if st.button("Mês Seguinte"):
                if st.session_state.cal_month == 12:
                    st.session_state.cal_month = 1
                    st.session_state.cal_year += 1
                else:
                    st.session_state.cal_month += 1
                st.rerun()
        st.markdown("---")
        
        cal = calendar.Calendar(firstweekday=0)
        mes_dias = cal.monthdayscalendar(st.session_state.cal_year, st.session_state.cal_month)
        dias_semana_cabecalho = ["s", "t", "q", "q", "s", "s", "d"]
        cols_cab = st.columns(7)
        for idx, d_nome in enumerate(dias_semana_cabecalho):
            with cols_cab[idx]:
                st.markdown(f"<p style='text-align: center; font-weight: bold; color: gray;'>{d_nome}</p>", unsafe_allow_html=True)
                
        logs_por_data = {log.get("data"): log for log in st.session_state.logs}
        testes_por_data = {}
        for t in st.session_state.testes:
            d_t = t.get("data")
            if d_t not in testes_por_data:
                testes_por_data[d_t] = []
            testes_por_data[d_t].append(t["materia"])
            
        for semana in mes_dias:
            cols = st.columns(7)
            for idx_col, dia in enumerate(semana):
                with cols[idx_col]:
                    if dia == 0:
                        st.markdown("<p style='text-align: center; color: #d3d3d3;'>-</p>", unsafe_allow_html=True)
                    else:
                        data_atual_loop = datetime.date(st.session_state.cal_year, st.session_state.cal_month, dia)
                        data_str = str(data_atual_loop)
                        resumo_resumido = ""
                        metodo_resumido = ""
                        if data_str in logs_por_data:
                            resumos_dict = logs_por_data[data_str].get("resumos", {})
                            materias_estudadas = [k for k, v in resumos_dict.items() if v.strip()]
                            resumo_resumido = ", ".join(materias_estudadas) if materias_estudadas else "Estudado"
                            metodo_resumido = logs_por_data[data_str].get("metodo", "Exercícios")
                            
                        testes_dia_str = f"Teste: {', '.join(testes_por_data[data_str])}" if data_str in testes_por_data else ""
                        
                        st.markdown(f"<p style='text-align: center; color: gray; margin-bottom: 0px;'><b>{dia}</b></p>", unsafe_allow_html=True)
                        if resumo_resumido:
                            st.markdown(f"<p style='text-align: center; font-size: 15px; color: #4b6584; margin-top: 0px; margin-bottom: 0px;'><b>{resumo_resumido}</b></p>", unsafe_allow_html=True)
                        if metodo_resumido:
                            st.markdown(f"<p style='text-align: center; font-size: 13px; color: #718093; margin-top: 0px;'><i>Método: {metodo_resumido}</i></p>", unsafe_allow_html=True)
                        if testes_dia_str:
                            st.markdown(f"<p style='text-align: center; font-size: 12px; color: #d63031; margin-top: 0px;'><b>{testes_dia_str}</b></p>", unsafe_allow_html=True)
                        if not resumo_resumido and not testes_dia_str:
                            st.markdown("<p style='text-align: center; font-size: 13px; color: #b2bec3; margin-top: 0px;'>-</p>", unsafe_allow_html=True)
                            
                        if st.button("Ver", key=f"btn_dia_{st.session_state.cal_year}_{st.session_state.cal_month}_{dia}"):
                            st.session_state.selected_date = data_atual_loop
                            st.rerun()

# 3. Agenda & Horário
elif menu == "Agenda & Horário":
    st.title("Gestão de Horário e Agenda")
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
        
    if st.button("Adicionar Aula"):
        st.session_state.num_aulas_extra[dia_escolhido] += 1
        st.rerun()
    if st.button("Guardar Alterações do Horário"):
        st.session_state.horario[dia_escolhido] = novo_dia
        st.success(f"Horário de {dia_escolhido} guardado com sucesso!")
        
    st.markdown("---")
    st.subheader("Gestão de Testes e Provas")
    with st.form("form_adicionar_teste"):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            materia_teste = st.selectbox("Matéria do Teste", LISTA_MATERIAS, key="fb_mat_teste")
        with col_t2:
            data_teste = st.date_input("Data do Teste", value=datetime.date.today(), key="fb_data_teste")
        with col_t3:
            st.markdown("<br>", unsafe_allow_html=True)
        submit_teste = st.form_submit_button("+ Adicionar Teste")
        if submit_teste:
            st.session_state.testes.append({
                "materia": materia_teste,
                "data": str(data_teste)
            })
            st.success(f"Teste de {materia_teste} agendado para {data_teste.strftime('%d/%m/%Y')} com sucesso!")
            
    if st.session_state.testes:
        st.markdown("### Testes Atualmente Agendados:")
        for idx, t in enumerate(st.session_state.testes):
            col_info, col_del = st.columns([4, 1])
            with col_info:
                d_obj = datetime.datetime.strptime(t["data"], "%Y-%m-%d").date()
                st.write(f"- **{t['materia']}** - Dia {d_obj.strftime('%d/%m/%Y')}")
            with col_del:
                if st.button("Remover", key=f"btn_del_teste_{idx}"):
                    st.session_state.testes.pop(idx)
                    st.rerun()

# 4. Registo Diário
elif menu == "Registo Diário":
    if st.session_state.step_registo == "formulario":
        st.title("Registo de Estudo Diário")
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
        for disc in disciplinas_dia:
            resumos_por_materia[disc] = st.text_area(f"Matéria: {disc}", key=f"res_{dia_automatico}_{disc}")
            
        if st.button("Registar Sessão"):
            registo_novo = {
                "data": str(hoje),
                "dia": dia_automatico,
                "resumos": resumos_por_materia,
                "metodo": "Registo Diário"
            }
            st.session_state.logs.append(registo_novo)
            flashcards_combinados = []
            st.session_state.chave_geracao += 1
            for disc in disciplinas_dia:
                texto_caixa = resumos_por_materia.get(disc, "")
                fcs_disc = gerar_flashcards_personalizados(5, disc, st.session_state.dificuldade_selecionada, st.session_state.ano_escolar, texto_caixa)
                if fcs_disc:
                    flashcards_combinados.extend(fcs_disc)
            st.session_state.flashcards_pos_gerados = flashcards_combinados
            st.success("Sessão registada com sucesso!")
            st.session_state.step_registo = "flashcards_pos"
            st.rerun()
            
    elif st.session_state.step_registo == "flashcards_pos":
        if st.button("Voltar", key="btn_voltar_pos_reg"):
            st.session_state.step_registo = "formulario"
            st.rerun()
        st.title("Revisão Rápida Pós-Registo")
        if not st.session_state.flashcards_pos_gerados:
            st.info("Não há flashcards gerados (certifica-te de que preencheste pelo menos uma matéria com texto válido).")
        else:
            for i, fc in enumerate(st.session_state.flashcards_pos_gerados, 1):
                st.markdown(f"**Cartão {i}:** {fc['pergunta']}")
                chave_estado = f"mostrar_pos_{st.session_state.chave_geracao}_{i}"
                if chave_estado not in st.session_state:
                    st.session_state[chave_estado] = False
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button(f"Virar #{i}", key=f"btn_virar_pos_card_{st.session_state.chave_geracao}_{i}"):
                        st.session_state[chave_estado] = not st.session_state[chave_estado]
                        st.rerun()
                with c2:
                    if st.session_state[chave_estado]:
                        st.success(f"**Resposta:** {fc['resposta']}")
                    else:
                        st.info("*(Resposta oculta - clica em 'Virar' para ver)*")
                st.markdown("---")
        if st.button("Ir para o Estudo", key="btn_ir_estudo_pos"):
            st.session_state.step_estudar = "escolher_materia"
            st.session_state.step_registo = "formulario"
            st.rerun()

# 5. Estudar
elif menu == "Estudar":
    if st.session_state.step_estudar == "escolher_materia":
        st.title("Estudo")
        recomendacao_texto = obter_recomendacao_inteligente()
        st.info(f"**Recomendação:** {recomendacao_texto}")
        st.subheader("O que queres estudar hoje?")
        materia_escolhida = st.selectbox("Escolhe a matéria que queres aprofundar:", LISTA_MATERIAS, key="sb_estudar_mat")
        if st.button("Avançar", key="btn_avancar_mat"):
            st.session_state.materia_escolhida_estudo = materia_escolhida
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()
            
    elif st.session_state.step_estudar == "upload_materiais":
        if st.button("Voltar", key="btn_voltar_up"):
            st.session_state.step_estudar = "escolher_materia"
            st.rerun()
        st.title("Estudo - Materiais e Apontamentos")
        st.markdown(f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo} (Nível: {st.session_state.ano_escolar})")
        st.session_state.texto_estudo_livre = st.text_area(
            "Insere os teus apontamentos exatos ou tópicos estudados na escola (ex: Verb to be, equações...):",
            value=st.session_state.texto_estudo_livre,
            key="txt_livre_estudo"
        )
        st.markdown("---")
        st.markdown("### Enviar Documentos, Áudios, Vídeos e Imagens:")
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            st.file_uploader("Enviar Documentos / PDFs / Apontamentos", type=["pdf", "docx", "txt"], key="up_docs")
            st.file_uploader("Enviar Gravações de Áudio", type=["mp3", "wav", "m4a"], key="up_audios")
        with col_up2:
            st.file_uploader("Enviar Vídeos de Aulas", type=["mp4", "mov"], key="up_videos")
            st.file_uploader("Enviar Imagens ou Fotografias", type=["png", "jpg", "jpeg"], key="up_imagens")
        if st.button("Avançar para Atividades", key="btn_avancar_up"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()
            
    elif st.session_state.step_estudar == "escolher_atividade":
        if st.button("Voltar", key="btn_voltar_ativ"):
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()
        st.title("Estudo - Escolher Atividade")
        atividade = st.radio(
            "Seleciona a opção pretendida:",
            ["Exercícios", "Quizzes", "Transcrição e Consolidação de Conteúdos", "Flashcards"],
            key="radio_ativ_estudar"
        )
        st.markdown("---")
        st.session_state.dificuldade_selecionada = st.radio(
            "Seleciona a Dificuldade:",
            ["Fácil", "Médio", "Difícil", "Muito difícil", "Extremamente difícil"],
            index=1,
            key="radio_dificuldade_opcao"
        )
        if st.button("Iniciar Atividade", key="btn_iniciar_ativ"):
            st.session_state.atividade_selecionada = atividade
            st.session_state.chave_geracao += 1
            if atividade == "Exercícios":
                st.session_state.exercicios_gerados = gerar_30_exercicios(
                    st.session_state.dificuldade_selecionada,
                    st.session_state.ano_escolar,
                    st.session_state.texto_estudo_livre
                )
            elif atividade == "Flashcards":
                st.session_state.flashcards_gerados = gerar_flashcards_personalizados(
                    20,
                    st.session_state.materia_escolhida_estudo,
                    st.session_state.dificuldade_selecionada,
                    st.session_state.ano_escolar,
                    st.session_state.texto_estudo_livre
                )
            st.session_state.step_estudar = "executar_atividade"
            st.rerun()
            
    elif st.session_state.step_estudar == "executar_atividade":
        if st.button("Voltar às Opções", key="btn_voltar_exec"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()
        st.title(f"{st.session_state.atividade_selecionada}")
        st.markdown(f"**Matéria:** {st.session_state.materia_escolhida_estudo} | **Dificuldade:** {st.session_state.dificuldade_selecionada} | **Ano:** {st.session_state.ano_escolar}")
        if st.session_state.texto_estudo_livre:
            st.info(f"**Foco Personalizado:** Apontamentos considerados: **{st.session_state.texto_estudo_livre}**.")
        st.markdown("---")
        
        if st.session_state.atividade_selecionada == "Exercícios":
            st.subheader("Conjunto de 30 Exercícios Práticos:")
            respostas_utilizador = {}
            for ex in st.session_state.exercicios_gerados:
                eid = ex["id"]
                st.markdown(f"**Exercício {eid}:** $${ex['enunciado']}$$")
                respostas_utilizador[eid] = st.text_input(f"Resposta para o exercício {eid}:", key=f"resp_ex_{eid}")
                st.markdown("---")
            if st.button("Submeter e Corrigir Respostas", key="btn_submeter_30"):
                acertos = 0
                for ex in st.session_state.exercicios_gerados:
                    eid = ex["id"]
                    val_str = str(respostas_utilizador.get(eid, "")).strip().lower()
                    if val_str not in ["não", "nao", ""]:
                        try:
                            if abs(float(val_str) - ex["resposta_correta"]) < 1e-3:
                                acertos += 1
                        except ValueError:
                            pass
                st.markdown(f"### Pontuação Final: **{acertos} / 30 corretas**")
                
                hoje_str = str(datetime.date.today())
                dias_portugal = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
                dia_atual_nome = dias_portugal[datetime.date.today().weekday()] if datetime.date.today().weekday() < 5 else "Segunda-feira"
                registo_existente = None
                for log in st.session_state.logs:
                    if log.get("data") == hoje_str:
                        registo_existente = log
                        break
                materia_atual = st.session_state.materia_escolhida_estudo
                texto_resumo_estudo = st.session_state.texto_estudo_livre or f"Pontuação: {acertos}/30"
                if registo_existente:
                    if "resumos" not in registo_existente:
                        registo_existente["resumos"] = {}
                    registo_existente["resumos"][materia_atual] = texto_resumo_estudo
                    registo_existente["metodo"] = st.session_state.atividade_selecionada
                else:
                    novo_registo = {
                        "data": hoje_str,
                        "dia": dia_atual_nome,
                        "resumos": {materia_atual: texto_resumo_estudo},
                        "metodo": st.session_state.atividade_selecionada
                    }
                    st.session_state.logs.append(novo_registo)
                st.success("Respostas corrigidas e guardadas no calendário com sucesso!")
                
        elif st.session_state.atividade_selecionada == "Flashcards":
            st.subheader("Conjunto de 20 Flashcards de Memorização:")
            if not st.session_state.flashcards_gerados:
                st.warning("⚠️ Não foram gerados flashcards para esta matéria.")
            else:
                if st.button("Gerar novas perguntas de flashcards", key="btn_gerar_novos_fc"):
                    st.session_state.flashcards_gerados = gerar_flashcards_personalizados(
                        20,
                        st.session_state.materia_escolhida_estudo,
                        st.session_state.dificuldade_selecionada,
                        st.session_state.ano_escolar,
                        st.session_state.texto_estudo_livre
                    )
                    st.rerun()
                for i, fc in enumerate(st.session_state.flashcards_gerados, 1):
                    st.markdown(f"**Cartão {i}:** {fc['pergunta']}")
                    chave_fc = f"mostrar_fc_estudo_{st.session_state.chave_geracao}_{i}"
                    if chave_fc not in st.session_state:
                        st.session_state[chave_fc] = False
                    col_b1, col_b2 = st.columns([1, 4])
                    with col_b1:
                        if st.button(f"Virar #{i}", key=f"btn_virar_estudo_{st.session_state.chave_geracao}_{i}"):
                            st.session_state[chave_fc] = not st.session_state[chave_fc]
                            st.rerun()
                    with col_b2:
                        if st.session_state[chave_fc]:
                            st.success(f"**Resposta:** {fc['resposta']}")
                        else:
                            st.info("*(Resposta oculta - clica em 'Virar' para ver)*")
                    st.markdown("---")
                    
                if st.button("Guardar Sessão de Flashcards no Calendário"):
                    hoje_str = str(datetime.date.today())
                    dias_portugal = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
                    dia_atual_nome = dias_portugal[datetime.date.today().weekday()] if datetime.date.today().weekday() < 5 else "Segunda-feira"
                    registo_existente = None
                    for log in st.session_state.logs:
                        if log.get("data") == hoje_str:
                            registo_existente = log
                            break
                    materia_atual = st.session_state.materia_escolhida_estudo
                    texto_resumo_estudo = st.session_state.texto_estudo_livre or "Revisão com Flashcards"
                    if registo_existente:
                        if "resumos" not in registo_existente:
                            registo_existente["resumos"] = {}
                        registo_existente["resumos"][materia_atual] = texto_resumo_estudo
                        registo_existente["metodo"] = st.session_state.atividade_selecionada
                    else:
                        novo_registo = {
                            "data": hoje_str,
                            "dia": dia_atual_nome,
                            "resumos": {materia_atual: texto_resumo_estudo},
                            "metodo": st.session_state.atividade_selecionada
                        }
                        st.session_state.logs.append(novo_registo)
                    st.success("Sessão de Flashcards guardada no calendário com sucesso!")
        else:
            st.info("Atividade interativa pronta a utilizar.")
            if st.button("Concluir e Guardar no Calendário"):
                hoje_str = str(datetime.date.today())
                dias_portugal = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
                dia_atual_nome = dias_portugal[datetime.date.today().weekday()] if datetime.date.today().weekday() < 5 else "Segunda-feira"
                registo_existente = None
                for log in st.session_state.logs:
                    if log.get("data") == hoje_str:
                        registo_existente = log
                        break
                materia_atual = st.session_state.materia_escolhida_estudo
                texto_resumo_estudo = st.session_state.texto_estudo_livre or "Estudo concluído"
                if registo_existente:
                    if "resumos" not in registo_existente:
                        registo_existente["resumos"] = {}
                    registo_existente["resumos"][materia_atual] = texto_resumo_estudo
                    registo_existente["metodo"] = st.session_state.atividade_selecionada
                else:
                    novo_registo = {
                        "data": hoje_str,
                        "dia": dia_atual_nome,
                        "resumos": {materia_atual: texto_resumo_estudo},
                        "metodo": st.session_state.atividade_selecionada
                    }
                    st.session_state.logs.append(novo_registo)
                st.success("Guardado no calendário com sucesso!")
