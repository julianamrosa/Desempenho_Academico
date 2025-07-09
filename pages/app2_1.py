# Bibliotecas para visualização, manipulação e interatividade
import streamlit as st  # criação do dashboard
import pandas as pd     # manipulação de dados
import datetime         # para exibir data da última atualização
from PIL import Image   # para exibir imagens (ex: logo)
import plotly.express as px  # gráficos interativos
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# Leitura dos dados
# ---------------------------------------------
df = pd.read_csv("student_habits.csv")

# ---------------------------------------------
# Configuração da página e layout inicial
# ---------------------------------------------
# st.set_page_config(layout="wide") # deixa a página em largura total
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('logo.png')   # logo larissa e ju

# ---------------------------------------------
# Logo e Seleção de página
# ---------------------------------------------

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.write("")
    st.image(image, width=150)

    # Atualiza no session_state a página atual
    st.session_state.pagina = "Correlação com as Notas"

    # Radio para selecionar a página
    opcao = st.radio(
        "Escolha a página:",
        ["Distribuições das Variáveis", "Correlação com as Notas"],
        index=1  # deixa esta selecionada por padrão
    )

    # Faz a navegação só se for diferente da atual
    if opcao != st.session_state.pagina:
        if opcao == "Distribuições das Variáveis":
            st.switch_page("app2.py")

# ---------------------------------------------
# Cabeçalho: título centralizado
# ---------------------------------------------

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #d9d9d9; font-size: 2rem; margin-top: 1px;'>
        VIDA ACADÊMICA E CONTEXTO EDUCACIONAL
    </h1>
    <h2 style='text-align: center; color: #d9d9d9; font-size: 1.5rem; margin-top: 0.5px;'>
        (Atividades acadêmicas e fatores socioeconômicos)
    </h2>
    <h1 style='text-align: center; color: #d9d9d9; font-size: 2.5rem; margin-top: 0.5px;'>
        Correlação com as Notas
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  # espaçamento visual

# ---------------------------------------------
# Filtros
# ---------------------------------------------

with col3:
    st.write("")
    # Sidebar Filters
    st.header("Filtros")

    # Age Range Filter
    age_range = st.slider("Idade", int(df['age'].min()), int(
        df['age'].max()), (int(df['age'].min()), int(df['age'].max())))

    # Gender Filter (single select)
    gender_filter = st.selectbox(
        "Gênero", options=['All'] + list(df['gender'].unique()))

    # Exam score Filter
    score_range = st.slider("Nota na Prova", int(df['exam_score'].min()), int(
        df['exam_score'].max()), (int(df['exam_score'].min()), int(df['exam_score'].max())))

    # Apply Filters
    df_orig = df.copy()

    if gender_filter != 'All':
        df = df[df['gender'] == gender_filter]

    df = df[
        (df['age'] >= age_range[0]) &
        (df['age'] <= age_range[1]) &
        (df['exam_score'] >= score_range[0]) &
        (df['exam_score'] <= score_range[1])
    ]

# ---------------------------------------------
# Data da última atualização
# ---------------------------------------------
col_date1, col_date2 = st.columns([0.6, 0.4])

with col_date2:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.info(f"📅 Última atualização: {box_date}")

# ---------------------------------------------
# Seção 1: Gráfico de Dispersão - Notas vs Horas de Estudo
# ---------------------------------------------
st.markdown("### Gráfico de Dispersão: Notas x Horas de Estudo")

fig1 = px.scatter(
    df,
    x="study_hours_per_day",
    y="exam_score",
    trendline="ols",  # regressão linear
    labels={
        "study_hours_per_day": "Horas de Estudo por Dia",
        "exam_score": "Nota"
    },
    title="Dispersão: Notas x Horas de Estudo",
    template="plotly_white",
    color_discrete_sequence=["#FF69B4"]
)

fig1.update_layout(
    title_font_size=16,
    font=dict(size=14),
    xaxis=dict(dtick=1),  # marca de 1 em 1 hora
    yaxis=dict(range=[df['exam_score'].min() - 5, df['exam_score'].max() + 5])
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------
# Seção 2: Boxplot - Emprego de Meio Período x Notas
# ---------------------------------------------
st.markdown("### Boxplot: Notas x Emprego de Meio Período")

fig2 = px.box(
    df,
    x="part_time_job",
    y="exam_score",
    color="part_time_job",
    title="Notas x Emprego de Meio Período",
    labels={
        "part_time_job": "Tem Emprego de Meio Período?",
        "exam_score": "Nota"
    },
    color_discrete_sequence=["#41DDEB", "#E5E99A"]
)

fig2.update_layout(
    xaxis_title="Emprego de Meio Período",
    yaxis_title="Nota",
    title_font_size=16,
    font=dict(size=13),
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------
# Seção 3: Gráfico de Dispersão - Notas vs Percentual de Presença
# ---------------------------------------------
st.markdown("### Gráfico de Dispersão: Notas x Percentual de Presença")

fig3 = px.scatter(
    df,
    x="attendance_percentage",
    y="exam_score",
    trendline="ols",
    labels={
        "attendance_percentage": "Percentual de Presença (%)",
        "exam_score": "Nota"
    },
    title="Dispersão: Notas x Percentual de Presença",
    template="plotly_white",
    color_discrete_sequence=["#00CC96"]
)

fig3.update_layout(
    title_font_size=16,
    font=dict(size=14),
    yaxis=dict(range=[df['exam_score'].min() - 5, df['exam_score'].max() + 5])
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------
# Seção 4: Boxplot - Nível de Educação dos Pais x Notas
# ---------------------------------------------
st.markdown("### Boxplot: Notas x Nível de Educação dos Pais")

fig4 = px.box(
    df,
    x="parental_education_level",
    y="exam_score",
    color="parental_education_level",
    title="Notas x Nível de Educação dos Pais",
    labels={
        "parental_education_level": "Nível de Educação dos Pais",
        "exam_score": "Nota"
    },
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig4.update_layout(
    xaxis_title="Nível de Educação dos Pais",
    yaxis_title="Nota",
    title_font_size=16,
    font=dict(size=13),
    showlegend=False
)

fig4.update_xaxes(tickangle=45)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------
# Seção 5: Boxplot - Qualidade da Internet x Notas
# ---------------------------------------------
st.markdown("### Boxplot: Notas x Qualidade da Internet")

fig5 = px.box(
    df,
    x="internet_quality",
    y="exam_score",
    color="internet_quality",
    title="Notas x Qualidade da Internet",
    labels={
        "internet_quality": "Qualidade da Internet",
        "exam_score": "Nota"
    },
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig5.update_layout(
    xaxis_title="Qualidade da Internet",
    yaxis_title="Nota",
    title_font_size=16,
    font=dict(size=13),
    showlegend=False
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------
# Seção 6: Boxplot - Participação Extracurricular x Notas
# ---------------------------------------------
st.markdown("### Boxplot: Notas x Participação Extracurricular")

fig6 = px.box(
    df,
    x="extracurricular_participation",
    y="exam_score",
    color="extracurricular_participation",
    title="Notas x Participação Extracurricular",
    labels={
        "extracurricular_participation": "Participação Extracurricular",
        "exam_score": "Nota"
    },
    color_discrete_sequence=["#FF6B6B", "#4ECDC4"]
)

fig6.update_layout(
    xaxis_title="Participação Extracurricular",
    yaxis_title="Nota",
    title_font_size=16,
    font=dict(size=13),
    showlegend=False
)

st.plotly_chart(fig6, use_container_width=True)

# ---------------------------------------------
# Seção 7: Histograma - Emprego de Meio Período por Gênero
# ---------------------------------------------
st.markdown("### Emprego de Meio Período x Gênero")

fig7 = px.histogram(
    df,
    x="gender",
    color="part_time_job",
    barmode="group",  # barras lado a lado
    text_auto=True,
    title="Emprego de Meio Período x Gênero"
)

fig7.update_layout(
    xaxis_title="Gênero",
    yaxis_title="Quantidade de Estudantes",
    title_font_size=16,
    font=dict(size=13)
)

st.plotly_chart(fig7, use_container_width=True)
