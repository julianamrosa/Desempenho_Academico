# Bibliotecas para visualização, manipulação e interatividade
import streamlit as st  # criação do dashboard
import pandas as pd     # manipulação de dados
import datetime         # para exibir data da última atualização
from PIL import Image   # para exibir imagens (ex: logo)
import plotly.express as px # gráficos interativos
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


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
st.set_page_config(layout="wide") # deixa a página em largura total
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('logo.png')   # logo larissa e ju

# ---------------------------------------------
# Logo e Seleção de página
# ---------------------------------------------

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.write("")
    st.image(image, width=150)

    # Atualiza no session_state a página atual
    st.session_state.pagina = "Distribuições das Variáveis"

    # Radio para selecionar a página
    opcao = st.radio(
        "Escolha a página:",
        ["Distribuições das Variáveis", "Correlação com as Notas"],
        index=0  # deixa esta selecionada por padrão
    )

    # Faz a navegação só se for diferente da atual
    if opcao != st.session_state.pagina:
        if opcao == "Correlação com as Notas":
            st.switch_page("pages/app1_1.py")

# ---------------------------------------------
# Cabeçalho: título centralizado
# ---------------------------------------------

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #d9d9d9; font-size: 3rem; margin-top: 1px;'>
        CARACTERÍSTICAS PESSOAIS
    </h1>
    <h1 style='text-align: center; color: #d9d9d9; font-size: 2.5rem; margin-top: 0.5px;'>
        Distribuições das Variáveis
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
    age_range = st.slider("Idade", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))

    # Gender Filter (single select)
    gender_filter = st.selectbox("Gênero", options=['All'] + list(df['gender'].unique()))

    # Exam score Filter
    score_range = st.slider("Nota na Prova", int(df['exam_score'].min()), int(df['exam_score'].max()), (int(df['exam_score'].min()), int(df['exam_score'].max())))

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
# Seção 1
# ---------------------------------------------
col4, col5, col6 = st.columns(3)

with col4:
    fig0 = px.pie(
        names=df.gender.value_counts().index, 
        values=df.gender.value_counts().values,
        hole=0.4
        )

    fig0.update_layout(
    title='Contagem de Estudantes por Gênero',
    title_x=0.25
)

    st.plotly_chart(fig0, use_container_width=True)

with col5:
    mean_value=df.age.mean()
    fig2 = px.bar(df.age.value_counts().sort_index())

    fig2.update_layout(
    title='Distribuição de Idades dos Estudantes',
    xaxis_title='Idade',
    yaxis_title='Contagem',
    title_x=0.25,
    showlegend=False,
    annotations=[
        go.layout.Annotation(
            x=mean_value,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"Média: {mean_value:.2f}",
            showarrow=False,
            font=dict(color="White"),
        )
    ]
)
    fig2.update_xaxes(tickmode='linear')

    fig2.add_shape(
    type="line",
    x0=mean_value,
    y0=0,
    x1=mean_value,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="White",
        width=2,
        dash="dash",
    ),
    name=f"Mean: {mean_value:.2f}"
)

    st.plotly_chart(fig2, use_container_width=True)

with col6:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.age.describe().drop('count').rename({
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Min',
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3',
    'max': 'Max'
}).to_frame(name='Idade'))


# ---------------------------------------------
# Seção 2
# ---------------------------------------------
col7, col8, col9 = st.columns(3)

with col7:
    fig1 = px.bar(
        df.diet_quality.value_counts().reindex(["Poor", "Fair", "Good"])
        )

    fig1.update_traces(textposition='outside')
    fig1.update_layout(
    title='Distribuição de Qualidade da Dieta dos Estudantes',
    xaxis_title='Qualidade da Dieta',
    yaxis_title='Frequência',
    title_x=0.25,
    showlegend=False
)

    st.plotly_chart(fig1, use_container_width=True)

with col8:
    mean_value=df.social_media_hours.mean()
    fig3 = px.histogram(df, x='social_media_hours', nbins=10)

    fig3.update_layout(
    title='Distribuição de Horas de Uso de Redes Sociais',
    xaxis_title='Horas em Redes Sociais',
    yaxis_title='Contagem',
    title_x=0.25,
    annotations=[
        go.layout.Annotation(
            x=mean_value,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"Média: {mean_value:.2f}",
            showarrow=False,
            font=dict(color="White"),
        )
    ]
)
    
    fig3.add_shape(
    type="line",
    x0=mean_value,
    y0=0,
    x1=mean_value,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="White",
        width=2,
        dash="dash",
    ),
    name=f"Mean: {mean_value:.2f}"
)

    st.plotly_chart(fig3, use_container_width=True)

with col9:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.social_media_hours.describe().drop('count').rename({
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Min',
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3',
    'max': 'Max'
}).to_frame(name='Horas em Redes Sociais'))

# ---------------------------------------------
# Seção 3
# ---------------------------------------------
col10, col11 = st.columns(2)

with col10:
    mean_value=df.netflix_hours.mean()
    fig4 = px.histogram(df, x='netflix_hours', nbins=6)

    fig4.update_layout(
    title='Distribuição de Horas Assistindo Netflix',
    xaxis_title='Horas na Netflix',
    yaxis_title='Contagem',
    title_x=0.25,
    annotations=[
        go.layout.Annotation(
            x=mean_value,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"Média: {mean_value:.2f}",
            showarrow=False,
            font=dict(color="White"),
        )
    ]
)
    
    fig4.add_shape(
    type="line",
    x0=mean_value,
    y0=0,
    x1=mean_value,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="White",
        width=2,
        dash="dash",
    ),
    name=f"Mean: {mean_value:.2f}"
)
    
    st.plotly_chart(fig4, use_container_width=True)

with col11:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.netflix_hours.describe().drop('count').rename({
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Min',
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3',
    'max': 'Max'
}).to_frame(name='Horas na Netflix'))

# ---------------------------------------------
# Seção 4
# ---------------------------------------------
col12, col13 = st.columns(2)

with col12:
    mean_value=df.sleep_hours.mean()
    fig5 = px.histogram(df, x='sleep_hours', nbins=7)

    fig5.update_layout(
    title='Distribuição de Horas de Sono dos Estudantes',
    xaxis_title='Horas de Sono',
    yaxis_title='Contagem',
    title_x=0.25,
    annotations=[
        go.layout.Annotation(
            x=mean_value,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"Média: {mean_value:.2f}",
            showarrow=False,
            font=dict(color="White"),
        )
    ]
)
    
    fig5.add_shape(
    type="line",
    x0=mean_value,
    y0=0,
    x1=mean_value,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="White",
        width=2,
        dash="dash",
    ),
    name=f"Mean: {mean_value:.2f}"
)
    
    st.plotly_chart(fig5, use_container_width=True)

with col13:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.sleep_hours.describe().drop('count').rename({
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Min',
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3',
    'max': 'Max'
}).to_frame(name='Horas de Sono'))

# ---------------------------------------------
# Seção 5
# ---------------------------------------------
col14, col15 = st.columns(2)

with col14:
    mean_value=df.exercise_frequency.mean()
    fig6 = px.bar(df.exercise_frequency.value_counts().sort_index())

    fig6.update_layout(
    title='Frequência Semanal de Exercicios Fisicos',
    xaxis_title='Exercícios Físicos Semanais',
    yaxis_title='Contagem',
    title_x=0.25,
    showlegend=False,
    annotations=[
        go.layout.Annotation(
            x=mean_value,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"Média: {mean_value:.2f}",
            showarrow=False,
            font=dict(color="White"),
        )
    ]
)
    fig6.update_xaxes(tickmode='linear')

    fig6.add_shape(
    type="line",
    x0=mean_value,
    y0=0,
    x1=mean_value,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="White",
        width=2,
        dash="dash",
    ),
    name=f"Mean: {mean_value:.2f}"
)

    st.plotly_chart(fig6, use_container_width=True)

with col15:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.exercise_frequency.describe().drop('count').rename({
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Min',
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3',
    'max': 'Max'
}).to_frame(name='Exercícios Físicos'))

# ---------------------------------------------
# Seção
# ---------------------------------------------
col16, col17 = st.columns(2)

with col16:
    mean_value=df.mental_health_rating.mean()
    fig7 = px.bar(df.mental_health_rating.value_counts().sort_index())

    fig7.update_layout(
    title='Distribuição de Escores de Saúde Mental dos Estudantes',
    xaxis_title='Escores',
    yaxis_title='Contagem',
    title_x=0.25,
    showlegend=False,
    annotations=[
        go.layout.Annotation(
            x=mean_value,
            y=1.02,
            xref="x",
            yref="paper",
            text=f"Média: {mean_value:.2f}",
            showarrow=False,
            font=dict(color="White"),
        )
    ]
)
    fig7.update_xaxes(tickmode='linear')

    fig7.add_shape(
    type="line",
    x0=mean_value,
    y0=0,
    x1=mean_value,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="White",
        width=2,
        dash="dash",
    ),
    name=f"Mean: {mean_value:.2f}"
)

    st.plotly_chart(fig7, use_container_width=True)

with col17:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.mental_health_rating.describe().drop('count').rename({
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Min',
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3',
    'max': 'Max'
}).to_frame(name='Escore de Saúde Mental'))

