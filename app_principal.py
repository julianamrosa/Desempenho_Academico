import streamlit as st
import base64

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


st.set_page_config(page_title="Página Inicial", layout="wide")

# Função para converter imagem em base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# Pega a imagem convertida
image_base64 = get_base64_image("logo.png")

# CSS customizado
st.markdown(f"""
    <style>
    .logo-img {{
        height: 350px;
    }}
    .title {{
        text-align: center;
        color: #ff3633;
        font-size: 3rem;
        margin-bottom: 1rem;
    }}
    .button-container {{
        display: flex;
        justify-content: center;
        gap: 50px;
        margin-top: 2rem;
    }}
    .button-box {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        max-width: 150px;
    }}
    .round-button {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 120px;
        height: 120px;
        background-color: #bf48d8;
        color: white;
        border-radius: 50%;
        text-decoration: none;
        font-size: 2.5rem;
        transition: 0.3s;
    }}
    .round-button:hover {{
        background-color: #cc1f1a;
        transform: scale(1.05);
    }}
    .button-label {{
        margin-bottom: 0.7rem;
        font-size: 1.6rem;
        color: #fdfefe;
        font-weight: 500;
    }}
    </style>
""", unsafe_allow_html=True)

# Layout de colunas
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown(f"""
        <img src="data:image/jpeg;base64,{image_base64}" class="logo-img">
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h1 class='title'>Fatores Pessoais e Acadêmicos que Influenciam o Desempenho Escolar</h1>", unsafe_allow_html=True)

    # Botões circulares lado a lado com textos acima
    st.markdown("""
        <div class="button-container">
            <div class="button-box">
                <div class="button-label">Características Pessoais</div>
                <a href="/app1" class="round-button">🧍</a>
            </div>
            <div class="button-box">
                <div class="button-label">Vida Acadêmica</div>
                <a href="/app2" class="round-button">🎓</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
