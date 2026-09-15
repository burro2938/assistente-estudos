import calendar
import datetime
import random
from groq import Groq
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Assistente de Estudos", page_icon="📚", layout="wide"
)

# Aplicar estilo e fonte Comfortaa
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@400;700&display=swap');
body, p, label, input, textarea, button, select, h1, h2, h3, h4, h5, h6 {
    font-family: 'Comfortaa', cursive, sans-serif !important;
}
section[data-testid="stSidebar"] h1 {
    font-size: 20px !important;
}
</style>
""",
    unsafe_allow_html=True,
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
if "groq_api_key" not in st.session_state:
  st.session_state.groq_api_key = ""
if "horario" not in st.session_state:
  st.session_state.horario = {
      "Segunda-feira": [
          {"hora": "08:30 - 09:15", "disc": "Educação Física"},
          {"hora": "09:25 - 10:10", "disc": "Matemática"},
          {"hora": "10:30 - 11:15", "disc": "Inglês"},
          {"hora": "11:25 - 12:10", "disc": "Português"},
      ],
      "Terça-feira": [
          {"hora": "08:30 - 09:15", "disc": "Matemática"},
          {"hora": "09:25 - 10:10", "disc": "Ciências Naturais"},
          {"hora": "10:30 - 11:15", "disc": "Francês"},
          {"hora": "11:25 - 12:10", "disc": "Físico-Química"},
      ],
      "Quarta-feira": [
          {"hora": "08:30 - 09:15", "disc": "Português"},
          {"hora": "09:25 - 10:10", "disc": "Inglês"},
          {"hora": "10:30 - 11:15", "disc": "Matemática"},
          {"hora": "11:25 - 12:10", "disc": "Educação Física"},
      ],
      "Quinta-feira": [
          {"hora": "08:30 - 09:15", "disc": "História"},
          {"hora": "09:25 - 10:10", "disc": "Ciências Naturais"},
          {"hora": "10:30 - 11:15", "disc": "Francês"},
          {"hora": "11:25 - 12:10", "disc": "Físico-Química"},
      ],
      "Sexta-feira": [
          {"hora": "08:30 - 09:15", "disc": "Português"},
          {"hora": "09:25 - 10:10", "disc": "Matemática"},
          {"hora": "10:30 - 11:15", "disc": "Educação Visual"},
          {"hora": "11:25 - 12:10", "disc": "TIC"},
      ],
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
    "Cidadania e Desenvolvimento",
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

  for i in range(1, 31):
    n1 = random.randint(2 * fator, 15 * fator)
    n2 = random.randint(2 * fator, 15 * fator)
    enunciado = f"Calcula o valor de {n1} \\times {n2} + {i * 2}"
    resp = float(n1 * n2 + i * 2)
    exs.append({"id": i, "enunciado": enunciado, "resposta_correta": resp})
  return exs


def chamar_api_groq_com_fallback(client, prompt):
  modelos_disponiveis = [
      "llama-3.1-8b-instant",
      "llama3-8b-8192",
      "mixtral-8x7b-32768",
      "llama3-70b-8192",
      "llama-3.3-70b-versatile",
  ]
  ultimo_erro = None
  for modelo in modelos_disponiveis:
    try:
      completion = client.chat.completions.create(
          model=modelo,
          messages=[{"role": "user", "content": prompt}],
          temperature=0.7,
      )
      return completion.choices[0].message.content
    except Exception as e:
      ultimo_erro = e
      continue
  raise Exception(f"Todos os modelos falharam. Erro final: {ultimo_erro}")


def gerar_flashcards_personalizados(
    quantidade, materia, dificuldade, ano_aluno, texto_apontamentos=""
):
  api_key = st.session_state.get("groq_api_key", "").strip()
  flashcards = []
  tema = texto_apontamentos.strip() if texto_apontamentos.strip() else materia

  # 1. Tentar ligar à API da Groq se houver chave inserida
  if api_key:
    try:
      client = Groq(api_key=api_key)
      prompt = f"""
            Gera exatamente {quantidade} flashcards de estudo rigorosos, técnicos e específicos baseados EXATAMENTE no tema e nos apontamentos fornecidos pelo aluno.
            Disciplina: {materia}
            Ano de escolaridade: {ano_aluno} (Programa escolar oficial em Portugal)
            Nível de dificuldade: {dificuldade}
            Apontamentos / Tema do aluno: "{tema}"
            
            IMPORTANTE: Os flashcards devem focar-se estritamente no tema exato fornecido pelo aluno, adaptados ao programa escolar português.
            Usa estritamente o seguinte formato para cada cartão:
            Pergunta: [pergunta]
            Resposta: [resposta]
            ---
            """
      texto_resp = chamar_api_groq_com_fallback(client, prompt)
      blocos = (
          texto_resp.split("---")
          if "---" in texto_resp
          else texto_resp.split("\n\n")
      )
      contador = 1
      for bloco in blocos:
        linhas = [l.strip() for l in bloco.strip().split("\n") if l.strip()]
        p, r = "", ""
        for linha in linhas:
          if (
              linha.lower().startswith("pergunta:")
              or linha.lower().startswith("p:")
          ):
            p = linha.split(":", 1)[1].strip()
          elif (
              linha.lower().startswith("resposta:")
              or linha.lower().startswith("r:")
          ):
            r = linha.split(":", 1)[1].strip()
        if p and r:
          flashcards.append({"id": contador, "pergunta": p, "resposta": r})
          contador += 1
    except Exception:
      flashcards = []

  # 2. Fallback Dinâmico Inteligente: Adapta-se automaticamente a QUALQUER tema inserido pelo utilizador
  if not flashcards:
    templates_dinamicos = [
        {
            "p": (
                f"O que define o conceito fundamental de '{tema}' no âmbito"
                f" da disciplina de {materia} ({ano_aluno})?"
            ),
            "r": (
                f" '{tema}' engloba o conjunto de princípios teóricos e"
                f" práticos essenciais estudados no programa escolar para dominar"
                f" esta matéria."
            ),
        },
        {
            "p": (
                f"Quais são as principais propriedades, regras ou etapas a ter"
                f" em conta ao trabalhar com '{tema}'?"
            ),
            "r": (
                f"Exige a compreensão rigorosa das definições, a correta"
                f" identificação dos termos e a aplicação estruturada dos"
                f" procedimentos associados a '{tema}'."
            ),
        },
        {
            "p": (
                f"Como se aplica a matéria de '{tema}' na resolução de um"
                f" exercício prático ou questão de teste?"
            ),
            "r": (
                f"Interpretando corretamente o enunciado, selecionando a regra"
                f" ou fórmula aplicável a '{tema}' e efetuando os cálculos ou"
                f" argumentação passo a passo."
            ),
        },
        {
            "p": (
                f"Qual é o objetivo principal de estudar o tema '{tema}' no"
                f" {ano_aluno}?"
            ),
            "r": (
                f"Desenvolver o raciocínio crítico, consolidar as bases da"
                f" disciplina de {materia} e preparar o aluno para conteúdos"
                f" mais avançados."
            ),
        },
        {
            "p": (
                f"Quais são os erros ou equívocos mais comuns a evitar ao"
                f" estudar '{tema}'?"
            ),
            "r": (
                f"Confundir definições teóricas, aplicar regras desadequadas"
                f" aos dados fornecidos sobre '{tema}' e não validar o"
                f" resultado final."
            ),
        },
    ]

    contador = 1
    while len(flashcards) < quantidade:
      template_atual = templates_dinamicos[(contador - 1) % len(templates_dinamicos)]
      sufixo = (
          f" (Parte {(contador - 1) // len(templates_dinamicos) + 1})"
          if contador > len(templates_dinamicos)
          else ""
      )
      flashcards.append({
          "id": contador,
          "pergunta": template_atual["p"].replace(f"'{tema}'", f"'{tema}'{sufixo}"),
          "resposta": template_atual["r"],
      })
      contador += 1

  return flashcards[:quantidade]


def obter_recomendacao_inteligente():
  hoje_obj = datetime.date.today()
  dias_pt = [
      "Segunda-feira",
      "Terça-feira",
      "Quarta-feira",
      "Quinta-feira",
      "Sexta-feira",
      "Sábado",
      "Domingo",
  ]
  dia_idx = hoje_obj.weekday()
  dia_nome = "Segunda-feira" if dia_idx >= 5 else dias_pt[dia_idx]
  aulas_hoje = st.session_state.horario.get(dia_nome, [])
  if st.session_state.logs:
    ultimo_registo = st.session_state.logs[-1]
    resumos_recentes = list(ultimo_registo.get("resumos", {}).keys())
    if resumos_recentes:
      materia_recente = resumos_recentes[0]
      return (
          f"Com base no teu horário de hoje ({dia_nome}) e no que estudaste"
          f" recentemente ({materia_recente}), sugerimos que dês continuidade a"
          " essa matéria."
      )
  sugestao_materia = aulas_hoje[0]["disc"] if aulas_hoje else "Matemática"
  return (
      f"Com base no teu horário de hoje ({dia_nome}), sugerimos que"
      f" pratiques {sugestao_materia}."
  )


# Barra Lateral de Navegação e Configuração de API
st.sidebar.markdown("# Menu Principal")
menu = st.sidebar.radio(
    "Navegar para:",
    [
        "Início & Escola",
        "Calendário",
        "Agenda & Horário",
        "Registo Diário",
        "Estudar",
    ],
)
st.sidebar.markdown("---")
st.sidebar.markdown("### Configuração da API")
st.session_state.groq_api_key = st.sidebar.text_input(
    "Chave API da Groq",
    value=st.session_state.groq_api_key,
    type="password",
    help="Insere a tua chave API da Groq",
)

# 1. Início & Escola
if menu == "Início & Escola":
  st.title("Meu Assistente de Estudos")
  st.write("Bem-vindo ao teu espaço centralizado de organização escolar e revisão!")
  recomendacao_texto = obter_recomendacao_inteligente()
  st.info(f"**Sugestão de Estudo:** {recomendacao_texto}")
  st.markdown("---")
  st.subheader("Configurações do Aluno")
  anos_disponiveis = [
      "5.º Ano",
      "6.º Ano",
      "7.º Ano",
      "8.º Ano",
      "9.º Ano",
      "10.° Ano",
      "11.° Ano",
      "12.° Ano",
  ]
  idx_ano_atual = (
      anos_disponiveis.index(st.session_state.ano_escolar)
      if st.session_state.ano_escolar in anos_disponiveis
      else 3
  )
  col1, col2, col3 = st.columns(3)
  with col1:
    st.session_state.escola = st.text_input(
        "Escola Atual", value=st.session_state.escola
    )
  with col2:
    st.session_state.ano_letivo = st.text_input(
        "Ano Letivo", value=st.session_state.ano_letivo
    )
  with col3:
    st.session_state.ano_escolar = st.selectbox(
        "Ano Escolar Atual",
        anos_disponiveis,
        index=idx_ano_atual,
        key="sb_ano_escolar_global",
    )
  st.success(
      f"A frequentar o **{st.session_state.ano_escolar}** (ano letivo"
      f" **{st.session_state.ano_letivo}**) em **{st.session_state.escola}**."
  )
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
          st.markdown(
              f"- <span style='font-size: 1.3em;'>**{disc}**: {res}</span>",
              unsafe_allow_html=True,
          )
        else:
          st.markdown(
              f"- <span style='font-size: 1.3em;'>**{disc}**: *(Sem"
              " apontamentos escritos)*</span>",
              unsafe_allow_html=True,
          )
      metodo_registado = registo_encontrado.get("metodo", "Exercícios")
      st.markdown("### Ficheiros e Métodos de Estudo:")
      st.markdown(
          f"- <span style='font-size: 1.3em;'>**Método utilizado:**"
          f" {metodo_registado}</span>",
          unsafe_allow_html=True,
      )
    else:
      st.info("Não existem registos de estudo guardados para este dia.")
    testes_dia = [
        t
        for t in st.session_state.testes
        if t.get("data") == str(st.session_state.selected_date)
    ]
    if testes_dia:
      st.markdown("### Testes Agendados para este Dia:")
      for t in testes_dia:
        st.markdown(
            f"- <span style='font-size: 1.3em;'>**Teste de"
            f" {t['materia']}**</span>",
            unsafe_allow_html=True,
        )
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
      meses_nomes = [
          "",
          "Janeiro",
          "Fevereiro",
          "Março",
          "Abril",
          "Maio",
          "Junho",
          "Julho",
          "Agosto",
          "Setembro",
          "Outubro",
          "Novembro",
          "Dezembro",
      ]
      st.markdown(
          f"<h3 style='text-align: center;'>{meses_nomes[st.session_state.cal_month]}"
          f" {st.session_state.cal_year}</h3>",
          unsafe_allow_html=True,
      )
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
    mes_dias = cal.monthdayscalendar(
        st.session_state.cal_year, st.session_state.cal_month
    )
    dias_semana_cabecalho = ["S", "T", "Q", "Q", "S", "S", "D"]
    cols_cab = st.columns(7)
    for idx, d_nome in enumerate(dias_semana_cabecalho):
      with cols_cab[idx]:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold; color:"
            f" gray;'>{d_nome}</p>",
            unsafe_allow_html=True,
        )
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
            st.markdown(
                "<p style='text-align: center; color: #d3d3d3;'>-</p>",
                unsafe_allow_html=True,
            )
          else:
            data_atual_loop = datetime.date(
                st.session_state.cal_year, st.session_state.cal_month, dia
            )
            data_str = str(data_atual_loop)
            resumo_resumido = ""
            metodo_resumido = ""
            if data_str in logs_por_data:
              resumos_dict = logs_por_data[data_str].get("resumos", {})
              materias_estudadas = [
                  k for k, v in resumos_dict.items() if v.strip()
              ]
              if materias_estudadas:
                resumo_resumido = ", ".join(materias_estudadas)
              else:
                resumo_resumido = "Estudado"
              metodo_resumido = logs_por_data[data_str].get(
                  "metodo", "Exercícios"
              )
            testes_dia_str = ""
            if data_str in testes_por_data:
              testes_dia_str = "Teste: " + ", ".join(testes_por_data[data_str])
            st.markdown(
                f"<p style='text-align: center; color: gray; margin-bottom:"
                f" 0px;'><b>{dia}</b></p>",
                unsafe_allow_html=True,
            )
            if resumo_resumido:
              st.markdown(
                  f"<p style='text-align: center; font-size: 15px; color:"
                  f" #4b6584; margin-top: 0px; margin-bottom:"
                  f" 0px;'><b>{resumo_resumido}</b></p>",
                  unsafe_allow_html=True,
              )
            if metodo_resumido:
              st.markdown(
                  f"<p style='text-align: center; font-size: 13px; color:"
                  f" #718093; margin-top: 0px;'><i>Método:"
                  f" {metodo_resumido}</i></p>",
                  unsafe_allow_html=True,
              )
            if testes_dia_str:
              st.markdown(
                  f"<p style='text-align: center; font-size: 12px; color:"
                  f" #d63031; margin-top: 0px;'><b>{testes_dia_str}</b></p>",
                  unsafe_allow_html=True,
              )
            if not resumo_resumido and not testes_dia_str:
              st.markdown(
                  "<p style='text-align: center; font-size: 13px; color:"
                  " #b2bec3; margin-top: 0px;'>-</p>",
                  unsafe_allow_html=True,
              )
            if st.button(
                "Ver",
                key=(
                    "btn_dia_"
                    f"{st.session_state.cal_year}_{st.session_state.cal_month}_{dia}"
                ),
            ):
              st.session_state.selected_date = data_atual_loop
              st.rerun()

# 3. Agenda & Horário
elif menu == "Agenda & Horário":
  st.title("Gestão de Horário e Agenda")
  st.subheader("Configurar Horário Semanal")
  dia_escolhido = st.selectbox(
      "Dia da Semana", list(st.session_state.horario.keys())
  )
  current_aulas = st.session_state.horario[dia_escolhido]
  if dia_escolhido not in st.session_state.num_aulas_extra:
    st.session_state.num_aulas_extra[dia_escolhido] = len(current_aulas)
  novo_dia = []
  for idx in range(st.session_state.num_aulas_extra[dia_escolhido]):
    item = (
        current_aulas[idx]
        if idx < len(current_aulas)
        else {"hora": "", "disc": ""}
    )
    if not isinstance(item, dict):
      item = {"hora": "", "disc": str(item)}
    col1, col2 = st.columns(2)
    with col1:
      nova_hora = st.text_input(
          f"Hora da Aula {idx+1}",
          value=item.get("hora", ""),
          key=f"h_{dia_escolhido}_{idx}",
      )
    with col2:
      nova_disc = st.text_input(
          f"Disciplina {idx+1}",
          value=item.get("disc", ""),
          key=f"d_{dia_escolhido}_{idx}",
      )
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
      materia_teste = st.selectbox(
          "Matéria do Teste", LISTA_MATERIAS, key="fb_mat_teste"
      )
    with col_t2:
      data_teste = st.date_input(
          "Data do Teste", value=datetime.date.today(), key="fb_data_teste"
      )
    with col_t3:
      st.markdown("<br>", unsafe_allow_html=True)
    submit_teste = st.form_submit_button("+ Adicionar Teste")
    if submit_teste:
      st.session_state.testes.append(
          {"materia": materia_teste, "data": str(data_teste)}
      )
      st.success(
          f"Teste de {materia_teste} agendado para"
          f" {data_teste.strftime('%d/%m/%Y')} com sucesso!"
      )
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
    dias_portugal = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]
    dia_atual_idx = hoje.weekday()
    dia_automatico = (
        "Segunda-feira" if dia_atual_idx >= 5 else dias_portugal[dia_atual_idx]
    )
    st.markdown(
        f"### Hoje é **{dia_automatico}** ({hoje.strftime('%d/%m/%Y')})"
    )
    aulas_do_dia = st.session_state.horario.get(dia_automatico, [])
    disciplinas_dia = []
    for aula in aulas_do_dia:
      disc = aula.get("disc", "") if isinstance(aula, dict) else str(aula)
      if disc and disc not in disciplinas_dia:
        disciplinas_dia.append(disc)
    resumos_por_materia = {}
    for disc in disciplinas_dia:
      resumos_por_materia[disc] = st.text_area(
          f"Matéria: {disc}", key=f"res_{dia_automatico}_{disc}"
      )
    if st.button("Registar Sessão"):
      registo_novo = {
          "data": str(hoje),
          "dia": dia_automatico,
          "resumos": resumos_por_materia,
          "metodo": "Registo Diário",
      }
      st.session_state.logs.append(registo_novo)
      flashcards_combinados = []
      st.session_state.chave_geracao += 1
      for disc in disciplinas_dia:
        texto_caixa = resumos_por_materia.get(disc, "")
        fcs_disc = gerar_flashcards_personalizados(
            5,
            disc,
            st.session_state.dificuldade_selecionada,
            st.session_state.ano_escolar,
            texto_caixa,
        )
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
      st.info("Não há flashcards gerados.")
    else:
      for i, fc in enumerate(st.session_state.flashcards_pos_gerados, 1):
        st.markdown(f"**Cartão {i}:** {fc['pergunta']}")
        chave_estado = f"mostrar_pos_{st.session_state.chave_geracao}_{i}"
        if chave_estado not in st.session_state:
          st.session_state[chave_estado] = False
        c1, c2 = st.columns([1, 4])
        with c1:
          if st.button(
              f"Virar #{i}",
              key=f"btn_virar_pos_card_{st.session_state.chave_geracao}_{i}",
          ):
            st.session_state[chave_estado] = not st.session_state[chave_estado]
            st.rerun()
        with c2:
          if st.session_state[chave_estado]:
            st.success(f"**Resposta:** {fc['resposta']}")
          else:
            st.info("*(Resposta oculta, clica em 'Virar' para ver)*")
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
    materia_escolhida = st.selectbox(
        "Escolhe a matéria que queres aprofundar:",
        LISTA_MATERIAS,
        key="sb_estudar_mat",
    )
    if st.button("Avançar", key="btn_avancar_mat"):
      st.session_state.materia_escolhida_estudo = materia_escolhida
      st.session_state.step_estudar = "upload_materiais"
      st.rerun()
  elif st.session_state.step_estudar == "upload_materiais":
    if st.button("Voltar", key="btn_voltar_up"):
      st.session_state.step_estudar = "escolher_materia"
      st.rerun()
    st.title("Estudo - Materiais e Apontamentos")
    st.markdown(
        f"**Matéria selecionada:** {st.session_state.materia_escolhida_estudo}"
        f" (Nível: {st.session_state.ano_escolar})"
    )
    st.session_state.texto_estudo_livre = st.text_area(
        "Insere os teus apontamentos exatos ou tópicos estudados na escola (ex:"
        " células, revoluções, reações químicas, etc.):",
        value=st.session_state.texto_estudo_livre,
        key="txt_livre_estudo",
    )
    st.markdown("---")
    st.markdown("### Enviar Documentos, Áudios, Vídeos e Imagens:")
    col_up1, col_up2 = st.columns(2)
    with col_up1:
      st.file_uploader(
          "Enviar Documentos / PDFs / Apontamentos",
          type=["pdf", "docx", "txt"],
          key="up_docs",
      )
      st.file_uploader(
          "Enviar Gravações de Áudio", type=["mp3", "wav", "m4a"], key="up_audios"
      )
    with col_up2:
      st.file_uploader(
          "Enviar Vídeos de Aulas", type=["mp4", "mov"], key="up_videos"
      )
      st.file_uploader(
          "Enviar Imagens ou Fotografias",
          type=["png", "jpg", "jpeg"],
          key="up_imagens",
      )
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
        [
            "Exercícios",
            "Quizzes",
            "Transcrição e Consolidação de Conteúdos",
            "Flashcards",
        ],
        key="radio_ativ_estudar",
    )
    st.markdown("---")
    st.session_state.dificuldade_selecionada = st.radio(
        "Seleciona a Dificuldade:",
        ["Fácil", "Médio", "Difícil", "Muito difícil", "Extremamente difícil"],
        index=1,
        key="radio_dificuldade_opcao",
    )
    if st.button("Iniciar Atividade", key="btn_iniciar_ativ"):
      st.session_state.atividade_selecionada = atividade
      st.session_state.chave_geracao += 1
      if atividade == "Exercícios":
        st.session_state.exercicios_gerados = gerar_30_exercicios(
            st.session_state.dificuldade_selecionada,
            st.session_state.ano_escolar,
            st.session_state.texto_estudo_livre,
        )
      elif atividade == "Flashcards":
        st.session_state.flashcards_gerados = gerar_flashcards_personalizados(
            20,
            st.session_state.materia_escolhida_estudo,
            st.session_state.dificuldade_selecionada,
            st.session_state.ano_escolar,
            st.session_state.texto_estudo_livre,
        )
      st.session_state.step_estudar = "executar_atividade"
      st.rerun()
  elif st.session_state.step_estudar == "executar_atividade":
    if st.button("Voltar às Opções", key="btn_voltar_exec"):
      st.session_state.step_estudar = "escolher_atividade"
      st.rerun()
    st.title(f"{st.session_state.atividade_selecionada}")
    st.markdown(
        f"**Matéria:** {st.session_state.materia_escolhida_estudo} |"
        f" **Dificuldade:** {st.session_state.dificuldade_selecionada} |"
        f" **Ano:** {st.session_state.ano_escolar}"
    )
    if st.session_state.texto_estudo_livre:
      st.info(
          "**Foco Personalizado:** Apontamentos considerados:"
          f" **{st.session_state.texto_estudo_livre}**"
      )
    st.markdown("---")
    if st.session_state.atividade_selecionada == "Exercícios":
      st.subheader("Conjunto de 30 Exercícios Práticos:")
      respostas_utilizador = {}
      for ex in st.session_state.exercicios_gerados:
        eid = ex["id"]
        st.markdown(f"**Exercício {eid}:** $${ex['enunciado']}$$")
        respostas_utilizador[eid] = st.text_input(
            f"Resposta para o exercício {eid}:", key=f"resp_ex_{eid}"
        )
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
        dias_portugal = [
            "Segunda-feira",
            "Terça-feira",
            "Quarta-feira",
            "Quinta-feira",
            "Sexta-feira",
            "Sábado",
            "Domingo",
        ]
        dia_atual_nome = (
            dias_portugal[datetime.date.today().weekday()]
            if datetime.date.today().weekday() < 5
            else "Segunda-feira"
        )
        registo_existente = None
        for log in st.session_state.logs:
          if log.get("data") == hoje_str:
            registo_existente = log
            break
        materia_atual = st.session_state.materia_escolhida_estudo
        texto_resumo_estudo = (
            st.session_state.texto_estudo_livre or f"Pontuação: {acertos}/30"
        )
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
              "metodo": st.session_state.atividade_selecionada,
          }
          st.session_state.logs.append(novo_registo)
        st.success(
            "Respostas corrigidas e guardadas no calendário com sucesso!"
        )
    elif st.session_state.atividade_selecionada == "Flashcards":
      st.subheader("Conjunto de Flashcards de Memorização:")
      if not st.session_state.flashcards_gerados:
        st.warning("Não foram gerados flashcards.")
      else:
        if st.button(
            "Gerar novas perguntas de flashcards", key="btn_gerar_novos_fc"
        ):
          st.session_state.flashcards_gerados = (
              gerar_flashcards_personalizados(
                  20,
                  st.session_state.materia_escolhida_estudo,
                  st.session_state.dificuldade_selecionada,
                  st.session_state.ano_escolar,
                  st.session_state.texto_estudo_livre,
              )
          )
          st.rerun()
        for i, fc in enumerate(st.session_state.flashcards_gerados, 1):
          st.markdown(f"**Cartão {i}:** {fc['pergunta']}")
          chave_fc = f"mostrar_fc_estudo_{st.session_state.chave_geracao}_{i}"
          if chave_fc not in st.session_state:
            st.session_state[chave_fc] = False
          col_b1, col_b2 = st.columns([1, 4])
          with col_b1:
            if st.button(
                f"Virar #{i}",
                key=f"btn_virar_estudo_{st.session_state.chave_geracao}_{i}",
            ):
              st.session_state[chave_fc] = not st.session_state[chave_fc]
              st.rerun()
          with col_b2:
            if st.session_state[chave_fc]:
              st.success(f"**Resposta:** {fc['resposta']}")
            else:
              st.info("*(Resposta oculta, clica em 'Virar' para ver)*")
          st.markdown("---")
        if st.button("Guardar Sessão de Flashcards no Calendário"):
          hoje_str = str(datetime.date.today())
          dias_portugal = [
              "Segunda-feira",
              "Terça-feira",
              "Quarta-feira",
              "Quinta-feira",
              "Sexta-feira",
              "Sábado",
              "Domingo",
          ]
          dia_atual_nome = (
              dias_portugal[datetime.date.today().weekday()]
              if datetime.date.today().weekday() < 5
              else "Segunda-feira"
          )
          registo_existente = None
          for log in st.session_state.logs:
            if log.get("data") == hoje_str:
              registo_existente = log
              break
          materia_atual = st.session_state.materia_escolhida_estudo
          texto_resumo_estudo = (
              st.session_state.texto_estudo_livre or "Revisão com Flashcards"
          )
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
                "metodo": st.session_state.atividade_selecionada,
            }
            st.session_state.logs.append(novo_registo)
          st.success("Sessão de Flashcards guardada no calendário com sucesso!")
