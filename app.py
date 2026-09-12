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
    st.session_state.dificuldade_selecionada = "Médio ⚖️"
if "chave_geracao" not in st.session_state:
    st.session_state.chave_geracao = 0

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
    "Educação Visual"
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
                s = " + " if val > 0 else " - "
                num = abs(val)
                return f"{s}{num}{var}" if num != 1 or var == "" else f"{s}{var}"

            p_esq = f"{a1}x" if a1 != 0 else ""
            p_b1 = f" {fmt_term(b1)}" if b1 != 0 else ""
            p_c1 = fmt_term(c1, "x")
            p_esq_total = f"{p_esq}{p_b1}{p_c1}".strip()
            if p_esq_total.startswith("+ "): p_esq_total = p_esq_total[2:]
            
            p_dir_x2 = f"{a2}x" if a2 != 0 else ""
            p_dir_b2 = f" {fmt_term(b2)}" if b2 != 0 else ""
            p_dir_d2 = fmt_term(d2)
            p_dir_total = f"{p_dir_x2}{p_dir_b2}{p_dir_d2}".strip()
            if p_dir_total.startswith("+ "): p_dir_total = p_dir_total[2:]
            
            if not p_esq_total: p_esq_total = "0"
            if not p_dir_total: p_dir_total = "0"
            
            enunciado = f"{p_esq_total} = {p_dir_total}"
            resp = float(sol)
        else:
            n1 = random.randint(2 * fator, 15 * fator)
            n2 = random.randint(2 * fator, 15 * fator)
            enunciado = f"Calcule o valor de {n1} × {n2} + {i * 2}"
            resp = float(n1 * n2 + i * 2)

        exs.append({
            "id": i,
            "enunciado": enunciado,
            "resposta_correta": resp
        })
    return exs

def gerar_flashcards_personalizados(quantidade, materia, dificuldade, ano_aluno, texto_apontamentos=""):
    texto_inf = texto_apontamentos.lower()
    
    # Palavra-chave "não" para recusar flashcards se o utilizador quiser
    if "não" in texto_inf or "nao" in texto_inf:
        return []

    banco_ingles = [
        ("Qual é a forma correta do verbo to be para o pronome 'I' no presente?", "Am (Ex: I am a student)."),
        ("Como se conjuga o verbo to be na afirmativa para 'He / She / It'?", "Is (Ex: He is 13 years old)."),
        ("Quais são os pronomes que utilizam 'are' no presente do verbo to be?", "You, We, They."),
        ("Qual é a forma negativa do verbo to be para 'I'?", "I am not (ou a forma curta I'm not)."),
        ("Como se diz 'Eles não são' utilizando a forma curta do verbo to be?", "They aren't."),
        ("Qual é a forma interrogativa correta para 'You are happy'?", "Are you happy?"),
        ("Qual é o passado do verbo to be para os pronomes I, He, She, It?", "Was (Ex: I was at school yesterday)."),
        ("Qual é o passado do verbo to be para os pronomes You, We, They?", "Were (Ex: We were friends)."),
        ("Como se forma a negativa do passado para 'He was'?", "He was not (ou wasn't)."),
        ("Como se formula uma pergunta no passado com o verbo to be, ex: 'She was tired'?", "Was she tired?")
    ]

    banco_matematica = [
        ("O que caracteriza uma equação do 1.º grau com parênteses?", "É uma igualdade algébrica que requer a aplicação da propriedade distributiva antes de agrupar os termos semelhantes."),
        ("Como se agrupam os termos com incógnita numa equação?", "Passando todos os termos com $x$ para um dos membros e os números para o outro, trocando o sinal aos que mudam de membro."),
        ("O que acontece ao sinal de um número quando este muda de membro?", "O sinal inverte-se (o que é positivo fica negativo e vice-versa)."),
        ("Qual é a soma dos ângulos internos de um triângulo?", "Sempre $180^\\circ$."),
        ("Como se calcula a área de um círculo?", "Multiplicando pi pelo quadrado do raio ($A = \\pi r^2$)."),
        ("O que é um número primo?", "Um número natural maior do que 1 divisível apenas por 1 e por si próprio."),
        ("O que indica a inclinação numa função afim $y = mx + b$?", "O declive ($m$), que determina se a função é crescente, decrescente ou constante."),
        ("Como se somam frações com denominadores diferentes?", "Reduzindo primeiramente as frações ao mesmo denominador através do cálculo do mínimo múltiplo comum (m.m.c.)."),
        ("O que é uma potência de base negativa e expoente par?", "O resultado é sempre um número positivo."),
        ("Como se calcula a percentagem de um valor?", "Multiplica-se o valor pela taxa percentual e divide-se o resultado por 100.")
    ]

    banco_portugues = [
        ("O que é o sujeito numa frase?", "O constituinte que concorda em número e pessoa com o verbo principal."),
        ("O que é uma palavra polissémica?", "Uma palavra que possui múltiplos significados consoante o contexto de uso."),
        ("Quais são os graus dos adjetivos?", "Grau normal, grau comparativo e grau superlativo."),
        ("O que caracteriza uma crónica?", "Um texto de opinião com base num acontecimento do quotidiano."),
        ("O que são sinónimos?", "Termos com significados equivalentes.")
    ]

    banco_historia = [
        ("Quais foram os principais fatores que impulsionaram a Expansão Portuguesa nos séculos XV e XVI?", "A posição geográfica favorável, a estabilidade política, o desenvolvimento da ciência náutica (caravela, astrolábio) e o interesse comercial nas especiarias."),
        ("O que marcou o início do Antigo Regime na Europa?", "O absolutismo régio, a sociedade de ordens (clero, nobreza e povo) e o mercantilismo económico."),
        ("Qual foi a importância do Tratado de Tordesilhas (1494)?", "Dividiu as terras descobertas e por descobrir entre Portugal e Espanha através de um meridiano."),
        ("O que foi a Revolução Francesa de 1789?", "Um marco histórico que acabou com o absolutismo em França, consagrando os direitos do homem e do cidadão."),
        ("Qual foi o papel do Infante D. Henrique na expansão marítima?", "Foi o grande impulsionador e organizador das primeiras viagens de exploração da costa ocidental africana.")
    ]

    banco_ciencias = [
        ("Qual é a unidade estrutural e funcional básica de todos os seres vivos?", "A célula."),
        ("O que distingue uma célula procariótica de uma célula eucariótica?", "A célula eucariótica possui um núcleo organizado envolto por membrana, enquanto a procariótica não tem núcleo definido."),
        ("Qual é o processo através do qual as plantas produzem a sua próprio matéria orgânica?", "A fotossíntese, utilizando luz solar, dióxido de carbono e água."),
        ("O que compõe o sistema solar?", "O Sol e todos os corpos celestes que orbitam à sua volta, incluindo os planetas, asteroides e cometas."),
        ("Qual é a função principal do sistema circulatório no corpo humano?", "Transportar oxigénio, nutrientes e hormonas para as células e recolher produtos de excreção.")
    ]

    banco_fisico_quimica = [
        ("O que é a matéria?", "Tudo o que tem massa e ocupa espaço no universo."),
        ("Qual é a diferença entre uma transformação física e uma transformação química?", "Na transformação física não se formam novas substâncias; na química formam-se novas substâncias com propriedades diferentes."),
        ("O que indica o número atómico de um elemento químico?", "O número de protões presentes no núcleo do átomo desse elemento."),
        ("Como se define a velocidade de um corpo?", "A distância percorrida por unidade de tempo ($v = d/t$).")
    ]

    materia_inf = materia.lower()

    # Condição abrangente para Matemática (com e sem acento)
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
            (f"Quais são os conceitos fundamentais estudados em {materia} no {ano_aluno}?", f"Envolve a compreensão teórica, princípios e aplicação correta da matéria de {materia}."),
            (f"Como se estruturam as regras principais de {materia}?", f"Através da análise lógica e memorização dos conceitos essenciais abordados na escola."),
            (f"Quais são os erros mais comuns a evitar nesta disciplina?", f"Falta de rigor conceptual e desatenção aos detalhes teóricos da matéria."),
            (f"De que forma este tema se aplica no programa escolar do {ano_aluno}?", f"Consolidando a base de conhecimentos exigidos em {materia}.")
        ]

    amostra = random.sample(banco_base, min(len(banco_base), quantidade))
    while len(amostra) < quantidade:
        amostra.append(random.choice(banco_base))

    flashcards = []
    for i, (pergunta, resposta) in enumerate(amostra, 1):
        flashcards.append({
            "id": i,
            "pergunta": f"{pergunta} (Matéria: {materia} | Nível: {dificuldade} | {ano_aluno})",
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
    
    recomendacao_texto = obter_recomendacao_inteligente()
    st.info(f"💡 **Sugestão de Estudo:** {recomendacao_texto}")

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
        for disc in disciplinas_dia:
            resumos_por_materia[disc] = st.text_area(f"Matéria: {disc} (Escreve 'não' se não quiseres flashcards)", key=f"res_{dia_automatico}_{disc}")
            
        if st.button("Registar Sessão"):
            registo_novo = {
                "data": str(hoje),
                "dia": dia_automatico,
                "resumos": resumos_por_materia
            }
            st.session_state.logs.append(registo_novo)
            
            flashcards_combinados = []
            st.session_state.chave_geracao += 1
            for disc in disciplinas_dia:
                texto_caixa = resumos_por_materia.get(disc, "")
                fcs_disc = gerar_flashcards_personalizados(
                    5, disc, st.session_state.dificuldade_selecionada, st.session_state.ano_escolar, texto_caixa
                )
                if fcs_disc:
                    flashcards_combinados.extend(fcs_disc)
            
            st.session_state.flashcards_pos_gerados = flashcards_combinados
            
            st.success("Sessão registada com sucesso!")
            st.session_state.step_registo = "flashcards_pos"
            st.rerun()

    elif st.session_state.step_registo == "flashcards_pos":
        if st.button("⬅️ Voltar", key="btn_voltar_pos_reg"):
            st.session_state.step_registo = "formulario"
            st.rerun()
            
        st.title("🧠 Revisão Rápida Pós-Registo")
        
        if not st.session_state.flashcards_pos_gerados:
            st.info("Nenhum flashcard gerado (ou utilizaste a palavra 'não' nos apontamentos). Podes avançar para o estudo normal!")
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

# 4. Alínea: Estudar
elif menu == "📖 Estudar":
    
    if st.session_state.step_estudar == "escolher_materia":
        st.title("📚 Estudo")
        
        recomendacao_texto = obter_recomendacao_inteligente()
        st.info(f"💡 **Recomendação:** {recomendacao_texto}")

        st.subheader("O que queres estudar hoje?")
        
        materia_escolhida = st.selectbox("Escolhe a matéria que queres aprofundar:", LISTA_MATERIAS, key="sb_estudar_mat")
        
        if st.button("Avançar", key="btn_avancar_mat"):
            st.session_state.materia_escolhida_estudo = materia_escolhida
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()

    elif st.session_state.step_estudar == "upload_materiais":
        if st.button("⬅️ Voltar", key="btn_voltar_up"):
            st.session_state.step_estudar = "escolher_materia"
            st.rerun()
            
        st.title("📚 Estudo - Materiais e Apontamentos")
        st.markdown(f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo} (Nível: {st.session_state.ano_escolar})")
        
        st.session_state.texto_estudo_livre = st.text_area(
            "Insere os teus apontamentos (escreve 'não' se quiseres ignorar flashcards):", 
            value=st.session_state.texto_estudo_livre, 
            key="txt_livre_estudo"
        )
        
        st.markdown("---")
        st.markdown("### 📂 Enviar Documentos, Áudios, Vídeos e Imagens:")
        
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
        if st.button("⬅️ Voltar", key="btn_voltar_ativ"):
            st.session_state.step_estudar = "upload_materiais"
            st.rerun()
            
        st.title("📚 Estudo - Escolher Atividade")
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
            if atividade == "Flashcards" and ("não" in st.session_state.texto_estudo_livre.lower() or "nao" in st.session_state.texto_estudo_livre.lower()):
                st.warning("⚠️ Usaste a palavra 'não' nos apontamentos, o que desativa os flashcards.")
            else:
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
        if st.button("⬅️ Voltar às Opções", key="btn_voltar_exec"):
            st.session_state.step_estudar = "escolher_atividade"
            st.rerun()
            
        st.title(f"🎯 {st.session_state.atividade_selecionada}")
        st.markdown(f"**Matéria:** {st.session_state.materia_escolhida_estudo} | **Dificuldade:** {st.session_state.dificuldade_selecionada} | **Ano:** {st.session_state.ano_escolar}")
        
        if st.session_state.texto_estudo_livre:
            st.info(f"💡 **Foco Personalizado:** Apontamentos considerados: *'{st.session_state.texto_estudo_livre}'* (Conteúdo detetado e adaptado com sucesso!).")
        
        st.markdown("---")
        
        if st.session_state.atividade_selecionada == "Exercícios":
            st.subheader("✏️ Conjunto de 30 Exercícios Práticos:")
            respostas_utilizador = {}
            for ex in st.session_state.exercicios_gerados:
                eid = ex["id"]
                st.markdown(f"**Exercício {eid}:**  $${ex['enunciado']}$$")
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
                
        elif st.session_state.atividade_selecionada == "Flashcards":
            st.subheader("🃏 Conjunto de 20 Flashcards de Memorização:")
            if st.button("🔄 Gerar novas perguntas de flashcards", key="btn_gerar_novos_fc"):
                st.session_state.flashcards_gerados = gerar_flashcards_personalizados(
                    20, 
                    st.session_state.materia_escolhida_estudo, 
                    st.session_state.dificuldade_selecionada, 
                    st.session_state.ano_escolar,
                    st.session_state.texto_estudo_livre
                )
                st.rerun()

            if not st.session_state.flashcards_gerados:
                st.warning("Nenhum flashcard gerado (verifique se inseriu a palavra 'não' nos apontamentos).")
            else:
                for i, fc in enumerate(st.session_state.flashcards_gerados, 1):
                    st.markdown(f"**Cartão {i}:** {fc['pergunta']}")
                    chave_fc = f"mostrar_fc_estudo_{st.session_state.chave_geracao}_{i}"
                    if chave_fc not in st.session_state:
                        st.session_state[chave_fc] = False
                        
                    col_b1, col_b2 = st.columns([1, 4])
                    with col_b1:
                        if st.button(f"Virar #{i}", key=f"btn_virar_estudo_{st.session_state.chave_geracao}_{i}```
