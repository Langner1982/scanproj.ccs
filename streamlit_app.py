import streamlit as st

st.set_page_config(page_title="ScanProj CCS", layout="wide")

st.title("🔎 ScanProj CCS")
st.subheader("Análise Inteligente de Projetos")

st.write("Envie os documentos do projeto para gerar uma análise técnica preliminar.")

st.divider()

# Uploads
st.header("📂 Upload de documentos")

cadastro = st.file_uploader("PDF do cadastro do projeto", type=["pdf"])
tramitacao = st.file_uploader("PDF da tramitação", type=["pdf"])
anexos = st.file_uploader("Anexos (opcional)", accept_multiple_files=True)

st.divider()

# Tipo de análise
st.header("⚙️ Tipo de análise")

modo = st.selectbox(
    "Selecione o tipo de análise",
    [
        "Análise completa",
        "Despacho curto",
        "Foco em inovação",
        "Foco em pendências"
    ]
)

st.divider()

# Botão
if st.button("🚀 Gerar análise"):
    st.subheader("📊 Resultado da análise")

    st.markdown("""
    ### 1. Classificação
    Projeto aparentemente classificado como pesquisa aplicada.

    ### 2. Pontos de atenção
    - Verificar coerência entre objetivo e metodologia
    - Conferir plano de trabalho

    ### 3. Pendências
    - Ausência de detalhamento no plano de trabalho

    ### 4. Potencial de inovação
    Médio (há indícios de aplicação prática)

    ### 5. Encaminhamento
    Recomenda-se solicitar complementação ao proponente.

    ### 6. Despacho sugerido
    Após análise preliminar, sugere-se o retorno ao interessado para complementação do plano de trabalho, a fim de garantir maior clareza na execução do projeto, salvo melhor juízo.
    """)
