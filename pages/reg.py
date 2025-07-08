import pandas as pd
import statsmodels.formula.api as smf
import streamlit as st
from PIL import Image   # para exibir imagens (ex: logo)
import numpy as np
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px # gráficos interativos
import plotly.graph_objects as go

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

# ⚙️ Pré-processamento
# Remover linhas com dados faltantes
df_clean = df.dropna()

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

# ---------------------------------------------
# Cabeçalho: título centralizado
# ---------------------------------------------

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #d9d9d9; font-size: 3rem; margin-top: 1px;'>
        Regressão Linear Múltipla
    </h1>
    <h1 style='text-align: center; color: #d9d9d9; font-size: 2.5rem; margin-top: 0.5px;'>
        Modelando as Notas dos Estudantes
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  # espaçamento visual

## Correlações ##

# Calcula matriz de correlação
corr = df.corr(numeric_only=True)
# Cria heatmap interativo
fig = px.imshow(
    corr,
    text_auto='.2f',
    color_continuous_scale='RdBu_r',
    aspect='auto',
    title='Matriz de Correlação para Variáveis Numéricas'
)
# Ajuste de layout opcional
fig.update_layout(
    coloraxis_colorbar=dict(title="Correlação"),
    title_x=0.4
)
# Exibe no Streamlit
st.plotly_chart(fig, use_container_width=True)

#Tabela de correlações das variáveis categóricas
st.markdown(
    "<h3 style='text-align: center; font-size:20px; font-weight:bold;'>Teste de Kruskal-Wallis para Diferença na Média das Notas entre Categorias das Variáveis Qualitativas</h3>",
    unsafe_allow_html=True
)
tabela = pd.DataFrame({
    'Gênero': [0.1501, 0.9277],
    'Trabalho de Meio Período': [0.9201, 0.3374],
    'Qualidade da Dieta': [2.4602, 0.2923],
    'Nível de Educação dos Pais': [2.9912, 0.2241],
    'Qualidade da Internet': [3.2213, 0.1998],
    'Participação Extracurricular': [0.0096, 0.9219]
})
tabela = tabela.set_axis(['Estatística', 'p-valor'], axis=0)
st.table(tabela)

## Regressão ##

# 📌 Definir fórmula da regressão
# Variáveis categóricas serão automaticamente transformadas em dummies pelo patsy/statsmodels
formula = 'exam_score ~ study_hours_per_day + social_media_hours + netflix_hours + attendance_percentage + sleep_hours + exercise_frequency + mental_health_rating'

# 📈 Ajustar o modelo
model = smf.ols(formula=formula, data=df_clean).fit()

# 📊 Métricas de desempenho
y_true = df_clean['exam_score']
y_pred = model.fittedvalues

rmse = np.sqrt(mean_squared_error(y_true, y_pred))

# 📉 Teste de normalidade dos resíduos (Shapiro-Wilk)
shapiro_test = shapiro(model.resid)

# 📏 Teste de homocedasticidade (Breusch-Pagan)
bp_test = het_breuschpagan(model.resid, model.model.exog)

# 📈 Teste de independência dos resíduos (Durbin-Watson)
dw = durbin_watson(model.resid)

# Assume df_clean already exists
# model = smf.ols(formula, data=df_clean).fit()

# Extracting model parameters as a DataFrame
model_summary_df = pd.DataFrame({
    'Coeficiente': model.params,
    'Erro Padrão': model.bse,
    'Estatística T': model.tvalues,
    'p-valor': model.pvalues
})
# Round for nicer display
model_summary_df = model_summary_df.round(4)
model_summary_df = model_summary_df.set_axis(['Intercepto', 'Horas de Estudo', 'Horas nas Redes Sociais',
                                               'Horas na Netflix', 'Frequências nas Aulas',
                                                 'Horas de Sono', 'Frequência de Exercícios Físicos',
                                                   'Escore de Saúde Mental'], axis=0)
#st.subheader("Resumo do Modelo")
st.markdown(
    "<h3 style='text-align: center; font-size:20px; font-weight:bold;'>Resumo do Modelo</h3>",
    unsafe_allow_html=True
)
# Show table
st.dataframe(model_summary_df)

st.markdown(
    "<h3 style='text-align: center; font-size:20px; font-weight:bold;'>Medidas de Qualidade do Modelo</h3>",
    unsafe_allow_html=True
)

qualidade = pd.DataFrame({
    'R2': [ 0.90],
    'REQM': [5.36],
    'Estatística F': [1156],
    'p-valor': [0.00],
    'Normalidade':['❌'],
    'Homocedasticidade':['✅'],
    'Erros Não-Correlacionados':['✅']
})
st.dataframe(qualidade.to_dict(orient="records"))



# st.markdown(
#     "<h3 style='text-align: center; font-size:20px;'>R²: 0.90</h3>",
#     unsafe_allow_html=True
# )
# st.markdown(
#     "<h3 style='text-align: center; font-size:20px;'>REQM: 5.36</h3>",
#     unsafe_allow_html=True
# )
# st.markdown(
#     "<h3 style='text-align: center; font-size:20px;'>F: 1156</h3>",
#     unsafe_allow_html=True
# )
# st.markdown(
#     "<h3 style='text-align: center; font-size:20px;'>p-valor: 0.00</h3>",
#     unsafe_allow_html=True
# )

# 📱 Interface Streamlit
#st.title("🔮 Predição da Nota no Exame")
st.markdown(
    "<h3 style='text-align: center; font-size:25px; font-weight:bold;'>🔮 Predição da Nota no Exame</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; font-size:20px; font-weight:bold;'>Insira os valores abaixo para prever a nota do aluno no exame:</h3>",
    unsafe_allow_html=True
)

#st.markdown("Insira os valores abaixo para prever a nota do aluno no exame:")

# 📥 Inputs lado a lado
col4, col5, col6 = st.columns(3)

with col4:
    study_hours_per_day = st.number_input("Horas de estudo por dia", min_value=0.0, max_value=24.0, value=2.0, step=0.5)
    social_media_hours = st.number_input("Horas em redes sociais por dia", min_value=0.0, max_value=24.0, value=3.0, step=0.5)
    netflix_hours = st.number_input("Horas de Netflix por dia", min_value=0.0, max_value=24.0, value=1.0, step=0.5)

with col5:
    attendance_percentage = st.number_input("Presença (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
    sleep_hours = st.number_input("Horas de sono por dia", min_value=0.0, max_value=24.0, value=7.0, step=0.5)

with col6:
    exercise_frequency = st.number_input("Frequência de exercício/semana", min_value=0, max_value=14, value=3, step=1)
    mental_health_rating = st.number_input("Saúde mental (1 a 10)", min_value=1, max_value=10, value=7, step=1)

# 📊 Botão de previsão
if st.button("Prever Nota"):
    dados_novos = pd.DataFrame({
        'study_hours_per_day': [study_hours_per_day],
        'social_media_hours': [social_media_hours],
        'netflix_hours': [netflix_hours],
        'attendance_percentage': [attendance_percentage],
        'sleep_hours': [sleep_hours],
        'exercise_frequency': [exercise_frequency],
        'mental_health_rating': [mental_health_rating]
    })

    nota_prevista = model.predict(dados_novos)

    st.success(f"🔮 Nota prevista no exame: **{nota_prevista.values[0]:.2f}**")
