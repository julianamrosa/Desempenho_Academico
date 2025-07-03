# Bibliotecas para visualização, manipulação e interatividade
import streamlit as st  # criação do dashboard
import pandas as pd     # manipulação de dados
import datetime         # para exibir data da última atualização
from PIL import Image   # para exibir imagens (ex: logo)
import plotly.express as px  # gráficos interativos
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------
# Leitura dos dados
# ---------------------------------------------
df = pd.read_csv("student_habits.csv")

# ---------------------------------------------
# Configuração da página e layout inicial
# ---------------------------------------------
st.set_page_config(layout="wide")  # deixa a página em largura total
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('logo.png')  # logo larissa e ju

# ---------------------------------------------
# Cabeçalho: logo e título centralizado
# ---------------------------------------------
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image(image, width=150)

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #d9d9d9; font-size: 2rem; margin-top: 1px;'>
        VIDA ACADÊMICA E CONTEXTO EDUCACIONAL (Atividades acadêmicas e fatores socioeconômicos)
    </h1>
    """, unsafe_allow_html=True)

# ---------------------------------------------
# Data da última atualização
# ---------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)  # espaçamento visual

col3, col4, col5 = st.columns([0.1, 0.4, 0.4])

with col5:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.info(f"📅 Última atualização: {box_date}")

# ---------------------------------------------
# Seção: Gráfico de Dispersão - Notas vs Horas de Estudo
# ---------------------------------------------
col6, col7, col8 = st.columns(3)

with col6:
    fig2 = px.scatter(
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

    fig2.update_layout(
        title_font_size=16,
        font=dict(size=14),
        xaxis=dict(dtick=1),  # marca de 1 em 1 hora
        yaxis=dict(range=[df['exam_score'].min() - 5, df['exam_score'].max() + 5])
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------
# Seção: Histograma - Emprego de Meio Período por Gênero
# ---------------------------------------------
with col7:
    fig3 = px.histogram(
        df,
        x="gender",
        color="part_time_job",
        barmode="group",  # barras lado a lado
        text_auto=True,
        title="Emprego de Meio Período x Gênero",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig3.update_layout(
        xaxis_title="Gênero",
        yaxis_title="Contagem",
        title_font_size=16,
        font=dict(size=13)
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------
# Seção: Boxplot - Impacto do Emprego nas Notas
# ---------------------------------------------
with col8:
    fig4 = px.box(
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

    fig4.update_layout(
        xaxis_title="Emprego de Meio Período",
        yaxis_title="Nota",
        title_font_size=16,
        font=dict(size=13),
        showlegend=False
    )

    st.plotly_chart(fig4, use_container_width=True)
