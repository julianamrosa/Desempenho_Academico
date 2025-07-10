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
            st.switch_page("pages/app2_1.py")

# ---------------------------------------------
# Cabeçalho: título centralizado
# ---------------------------------------------

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #d9d9d9; font-size: 3rem; margin-top: 1px;'>
        VIDA ACADÊMICA E CONTEXTO EDUCACIONAL
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

    # study_hours_per_day Range Filter
    hours_range = st.slider("Horas de Estudo", int(df['study_hours_per_day'].min()), int(df['study_hours_per_day'].max()), (int(df['study_hours_per_day'].min()), int(df['study_hours_per_day'].max())))

    # attendance_percentage Range Filter
    attendance_range = st.slider("Horas de Estudo", int(df['attendance_percentage'].min()), int(df['attendance_percentage'].max()), (int(df['attendance_percentage'].min()), int(df['attendance_percentage'].max())))

    # Exam score Filter
    score_range = st.slider("Nota na Prova", int(df['exam_score'].min()), int(df['exam_score'].max()), (int(df['exam_score'].min()), int(df['exam_score'].max())))

    # Apply Filters
    df_orig = df.copy()

    df = df[
        (df['study_hours_per_day'] >= hours_range[0]) &
        (df['study_hours_per_day'] <= hours_range[1]) &
        (df['attendance_percentage'] >= attendance_range[0]) &
        (df['attendance_percentage'] <= attendance_range[1]) &
        (df['exam_score'] >= score_range[0]) &
        (df['exam_score'] <= score_range[1])
    ]

# ---------------------------------------------
# Data da última atualização
# ---------------------------------------------
# col_date1, col_date2 = st.columns([0.6, 0.4])

# with col_date2:
#     box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
#     st.info(f"📅 Última atualização: {box_date}")

# ---------------------------------------------
# Seção 1: Distribuição de Horas de Estudo por Dia
# ---------------------------------------------
col4, col5 = st.columns(2)

with col4:
    mean_value = df.study_hours_per_day.mean()
    fig1 = px.histogram(df, x='study_hours_per_day', nbins=8)

    fig1.update_layout(
        title='Distribuição de Horas de Estudo por Dia',
        xaxis_title='Horas de Estudo',
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
    
    fig1.add_shape(
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
    
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.table(df.study_hours_per_day.describe().drop('count').rename({
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Min',
        '25%': 'Q1',
        '50%': 'Mediana',
        '75%': 'Q3',
        'max': 'Max'
    }).to_frame(name='Horas de Estudo'))

# ---------------------------------------------
# Seção 2: Distribuição de Emprego de Meio Período
# ---------------------------------------------
col6, col7 = st.columns(2)

with col6:
    fig2 = px.pie(
        names=df.part_time_job.value_counts().index, 
        values=df.part_time_job.value_counts().values,
        hole=0.4,
        title='Distribuição de Emprego de Meio Período'
    )

    fig2.update_layout(
        title_x=0.25
    )

    st.plotly_chart(fig2, use_container_width=True)

with col7:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    # Criar tabela de estatísticas para variável categórica
    job_stats = df.part_time_job.value_counts().reset_index()
    job_stats.columns = ['Emprego', 'Contagem']
    job_stats['Percentual'] = (job_stats['Contagem'] / len(df) * 100).round(2)
    st.table(job_stats.set_index('Emprego'))

# ---------------------------------------------
# Seção 3: Distribuição de Percentual de Presença
# ---------------------------------------------
col8, col9 = st.columns(2)

with col8:
    mean_value = df.attendance_percentage.mean()
    fig3 = px.histogram(df, x='attendance_percentage', nbins=10)

    fig3.update_layout(
        title='Distribuição de Percentual de Presença',
        xaxis_title='Percentual de Presença (%)',
        yaxis_title='Contagem',
        title_x=0.25,
        annotations=[
            go.layout.Annotation(
                x=mean_value,
                y=1.02,
                xref="x",
                yref="paper",
                text=f"Média: {mean_value:.2f}%",
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
    st.table(df.attendance_percentage.describe().drop('count').rename({
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Min',
        '25%': 'Q1',
        '50%': 'Mediana',
        '75%': 'Q3',
        'max': 'Max'
    }).to_frame(name='Presença (%)'))

# ---------------------------------------------
# Seção 4: Distribuição de Nível de Educação dos Pais
# ---------------------------------------------
col10, col11 = st.columns(2)

with col10:
    fig4 = px.pie(
        names=df.parental_education_level.value_counts().index, 
        values=df.parental_education_level.value_counts().values,
        hole=0.4,
        title='Distribuição de Nível de Educação dos Pais'
    )

    fig4.update_layout(
        title_x=0.25
    )

    st.plotly_chart(fig4, use_container_width=True)

with col11:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    # Criar tabela de estatísticas para variável categórica
    edu_stats = df.parental_education_level.value_counts().reset_index()
    edu_stats.columns = ['Nível de Educação', 'Contagem']
    edu_stats['Percentual'] = (edu_stats['Contagem'] / len(df) * 100).round(2)
    st.table(edu_stats.set_index('Nível de Educação'))

# ---------------------------------------------
# Seção 5: Distribuição de Qualidade da Internet
# ---------------------------------------------
col12, col13 = st.columns(2)

with col12:
    fig5 = px.pie(
        names=df.internet_quality.value_counts().index, 
        values=df.internet_quality.value_counts().values,
        hole=0.4,
        title='Distribuição de Qualidade da Internet'
    )

    fig5.update_layout(
        title_x=0.25
    )

    st.plotly_chart(fig5, use_container_width=True)

with col13:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    # Criar tabela de estatísticas para variável categórica
    internet_stats = df.internet_quality.value_counts().reset_index()
    internet_stats.columns = ['Qualidade da Internet', 'Contagem']
    internet_stats['Percentual'] = (internet_stats['Contagem'] / len(df) * 100).round(2)
    st.table(internet_stats.set_index('Qualidade da Internet'))

# ---------------------------------------------
# Seção 6: Distribuição de Participação Extracurricular
# ---------------------------------------------
col14, col15 = st.columns(2)

with col14:
    fig6 = px.pie(
        names=df.extracurricular_participation.value_counts().index, 
        values=df.extracurricular_participation.value_counts().values,
        hole=0.4,
        title='Distribuição de Participação Extracurricular'
    )

    fig6.update_layout(
        title_x=0.25
    )

    st.plotly_chart(fig6, use_container_width=True)

with col15:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    # Criar tabela de estatísticas para variável categórica
    extra_stats = df.extracurricular_participation.value_counts().reset_index()
    extra_stats.columns = ['Participação Extracurricular', 'Contagem']
    extra_stats['Percentual'] = (extra_stats['Contagem'] / len(df) * 100).round(2)
    st.table(extra_stats.set_index('Participação Extracurricular'))

# ---------------------------------------------
# Seção 7: Distribuição de Notas na Prova
# ---------------------------------------------
col16, col17 = st.columns(2)

with col16:
    mean_value = df.exam_score.mean()
    fig7 = px.histogram(df, x='exam_score', nbins=10)

    fig7.update_layout(
        title='Distribuição de Notas na Prova',
        xaxis_title='Notas',
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
    st.table(df.exam_score.describe().drop('count').rename({
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Min',
        '25%': 'Q1',
        '50%': 'Mediana',
        '75%': 'Q3',
        'max': 'Max'
    }).to_frame(name='Notas'))

# # ---------------------------------------------
# # Seção 8: Distribuição de Idade
# # ---------------------------------------------
# col18, col19 = st.columns(2)

# with col18:
#     mean_value = df.age.mean()
#     fig8 = px.bar(df.age.value_counts().sort_index())

#     fig8.update_layout(
#         title='Distribuição de Idades dos Estudantes',
#         xaxis_title='Idade',
#         yaxis_title='Contagem',
#         title_x=0.25,
#         showlegend=False,
#         annotations=[
#             go.layout.Annotation(
#                 x=mean_value,
#                 y=1.02,
#                 xref="x",
#                 yref="paper",
#                 text=f"Média: {mean_value:.2f}",
#                 showarrow=False,
#                 font=dict(color="White"),
#             )
#         ]
#     )
#     fig8.update_xaxes(tickmode='linear')

#     fig8.add_shape(
#         type="line",
#         x0=mean_value,
#         y0=0,
#         x1=mean_value,
#         y1=1,
#         xref="x",
#         yref="paper",
#         line=dict(
#             color="White",
#             width=2,
#             dash="dash",
#         ),
#         name=f"Mean: {mean_value:.2f}"
#     )

#     st.plotly_chart(fig8, use_container_width=True)

# with col19:
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.table(df.age.describe().drop('count').rename({
#         'mean': 'Média',
#         'std': 'Desvio Padrão',
#         'min': 'Min',
#         '25%': 'Q1',
#         '50%': 'Mediana',
#         '75%': 'Q3',
#         'max': 'Max'
#     }).to_frame(name='Idade'))

# # ---------------------------------------------
# # Seção 9: Distribuição de Gênero
# # ---------------------------------------------
# col20, col21 = st.columns(2)

# with col20:
#     fig9 = px.pie(
#         names=df.gender.value_counts().index, 
#         values=df.gender.value_counts().values,
#         hole=0.4,
#         title='Distribuição de Gênero'
#     )

#     fig9.update_layout(
#         title_x=0.25
#     )

#     st.plotly_chart(fig9, use_container_width=True)

# with col21:
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
    
#     # Criar tabela de estatísticas para variável categórica
#     gender_stats = df.gender.value_counts().reset_index()
#     gender_stats.columns = ['Gênero', 'Contagem']
#     gender_stats['Percentual'] = (gender_stats['Contagem'] / len(df) * 100).round(2)
#     st.table(gender_stats.set_index('Gênero'))