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
    st.session_state.pagina = "Correlação com as Notas"

    # Radio para selecionar a página
    opcao = st.radio(
        "Escolha a página:",
        ["Distribuições das Variáveis", "Correlação com as Notas"],
        index=1  # esta vem selecionada aqui
    )

    # Faz a navegação só se for diferente da atual
    if opcao != st.session_state.pagina:
        if opcao == "Distribuições das Variáveis":
            st.switch_page("pages/app1.py")

# ---------------------------------------------
# Cabeçalho: título centralizado
# ---------------------------------------------

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #d9d9d9; font-size: 3rem; margin-top: 1px;'>
        CARACTERÍSTICAS PESSOAIS
    </h1>
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
col4, col5 = st.columns(2)

with col4:
    fig0 = px.box(df, y='exam_score', x='gender', 
                  color='gender',
                  color_discrete_map={'Male': '#FF6B6B', 'Female': '#4ECDC4'})

    fig0.update_traces(boxmean=True)

    fig0.update_layout(
        title='Distribuição de Notas por Gênero',
        xaxis_title='Gênero',
        yaxis_title='Notas',
        title_x=0.25,
        showlegend=False
    )

    st.plotly_chart(fig0, use_container_width=True)

with col5:
    fig1 = px.box(df, y='exam_score', x='diet_quality',
                  category_orders={'diet_quality': ['Poor', 'Fair', 'Good']},
                  color='diet_quality',
                  color_discrete_map={'Poor': '#FF6B6B', 'Fair': '#FFA726', 'Good': '#66BB6A'})

    fig1.update_traces(boxmean=True)

    fig1.update_layout(
        title='Distribuição de Notas por Qualidade da Dieta',
        xaxis_title='Qualidade da Dieta',
        yaxis_title='Notas',
        title_x=0.25,
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

df = df.sort_values(by=['age', 'exam_score'])
cores = px.colors.sequential.Plasma  # Mudando para Plasma para cores mais vibrantes

# Normalizar notas para pegar cores proporcionais
min_nota = df['exam_score'].min()
max_nota = df['exam_score'].max()

def get_cor(nota):
    idx = int((nota - min_nota) / (max_nota - min_nota) * (len(cores)-1))
    return cores[idx]

# Criar barras empilhadas
fig = go.Figure()

for _, row in df.iterrows():
    fig.add_trace(go.Bar(
        x=[row['age']],
        y=[1],  # Cada barra representa uma pessoa/notas
        marker_color=get_cor(row['exam_score']),
        name=f"Nota {row['exam_score']}",
        showlegend=False
    ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Idade',
        yaxis_title='Contagem',
        title='Distribuição de Notas por Idade',
        title_x=0.5
    )
    # Scatter invisível para criar colorbar
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            colorscale='Plasma',  # mesma escala usada nas barras
            cmin=min_nota,
            cmax=max_nota,
            colorbar=dict(title='Nota'),
            color=[min_nota, max_nota],  # dois pontos pra gerar o degradê completo
            size=0
        ),
        showlegend=False
    ))

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------
# Seção 2
# ---------------------------------------------
col7, col8, col9 = st.columns(3)

with col7:
    fig3 = px.scatter(df, x="social_media_hours", y="exam_score",
                      color_discrete_sequence=['#9C27B0'])
    
    fig3.update_traces(marker=dict(size=8, line=dict(width=1, color='#7B1FA2')))
    
    fig3.update_layout(
        title='Distribuição de Notas por Horas nas Redes Sociais',
        xaxis_title='Horas nas Redes',
        yaxis_title='Notas',
        title_x=0.25
    )

    st.plotly_chart(fig3, use_container_width=True)

with col8:
    fig4 = px.scatter(df, x="netflix_hours", y="exam_score",
                      color_discrete_sequence=['#FF5722'])
    
    fig4.update_traces(marker=dict(size=8, line=dict(width=1, color='#D84315')))
    
    fig4.update_layout(
        title='Distribuição de Notas por Horas na Netflix',
        xaxis_title='Horas na Netflix',
        yaxis_title='Notas',
        title_x=0.25
    )
    
    st.plotly_chart(fig4, use_container_width=True)

with col9:
    fig5 = px.scatter(df, x="sleep_hours", y="exam_score",
                      color_discrete_sequence=['#2196F3'])
    
    fig5.update_traces(marker=dict(size=8, line=dict(width=1, color='#1976D2')))
    
    fig5.update_layout(
        title='Distribuição de Notas por Horas de Sono',
        xaxis_title='Horas de Sono',
        yaxis_title='Notas',
        title_x=0.25
    )
    
    st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------
# Seção 3
# ---------------------------------------------
col10, col11 = st.columns(2)

with col10:
    # Criar escala de cores para exercícios (0-7 dias)
    exercise_colors = ['#FF6B6B', '#FF8A65', '#FFA726', '#FFB74D', '#AED581', '#81C784', '#66BB6A', '#4CAF50']
    
    fig6 = px.box(df, y='exam_score', x='exercise_frequency',
                  color='exercise_frequency',
                  color_discrete_sequence=exercise_colors)

    fig6.update_traces(boxmean=True)

    fig6.update_layout(
        title='Distribuição de Notas por Frequência Semanal de Exercício Físico',
        xaxis_title='Exercícios Físicos',
        yaxis_title='Notas',
        title_x=0.25,
        showlegend=False
    )

    st.plotly_chart(fig6, use_container_width=True)

with col11:
    # Criar escala de cores para saúde mental (1-10)
    mental_colors = ['#D32F2F', '#F44336', '#FF5722', '#FF7043', '#FFA726', '#FFB74D', '#FFCC02', '#8BC34A', '#4CAF50', '#2E7D32']
    
    fig7 = px.box(df, y='exam_score', x='mental_health_rating',
                  color='mental_health_rating',
                  color_discrete_sequence=mental_colors)

    fig7.update_traces(boxmean=True)

    fig7.update_layout(
        title='Distribuição de Notas por Escore de Saúde Mental',
        xaxis_title='Escores de Saúde Mental',
        yaxis_title='Notas',
        title_x=0.25,
        showlegend=False,
        xaxis=dict(
        tickmode='linear',  # força os ticks a seguirem um espaçamento fixo
        dtick=1             # espaçamento entre ticks (1 significa mostrar todos)
    )
    )
    
    st.plotly_chart(fig7, use_container_width=True)

fig8 = px.scatter(
    df,
    x="social_media_hours",
    y="netflix_hours",
    color="gender",
    size="mental_health_rating",
    color_discrete_map={'Male': '#FF6B6B', 'Female': '#4ECDC4'}
)

fig8.update_traces(marker=dict(line=dict(width=1, color='white')))

fig8.update_layout(
    title='Horas nas Redes Sociais e na Netflix, por Gênero e Saúde Mental',
    xaxis_title='Horas nas Redes Sociais',
    yaxis_title='Horas na Netflix',
    legend_title="Gênero",
    title_x=0.3
)

st.plotly_chart(fig8, use_container_width=True)