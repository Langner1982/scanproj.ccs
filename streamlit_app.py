import streamlit as st
from openai import OpenAI
import PyPDF2

st.set_page_config(page_title="ScanProj CCS", layout="wide")

st.title("🔎 ScanProj CCS")
st.subheader("Análise Inteligente de Projetos")

st.write("Envie os documentos do projeto para gerar uma análise técnica preliminar.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.divider()

st.header("📂 Upload de documentos")

cadastro = st.file_uploader("PDF do cadastro do projeto", type=["pdf"])
tramitacao = st.file_uploader("PDF da tramitação", type=["pdf"])
anexos = st.file_uploader(
    "Anexos gerais do projeto",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)
st.divider()

def ler_pdf(arquivo):
    texto = ""
    reader = PyPDF2.PdfReader(arquivo)
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto

if st.button("🚀 Gerar análise"):

    if cadastro is None:
        st.warning("Envie o PDF do cadastro")
    else:
        with st.spinner("Analisando..."):

            texto = ler_pdf(cadastro)

            prompt = f"""
            Você é um analista técnico de projetos do CCS/UFSM.

            Analise o projeto abaixo e gere:

            1. Classificação
            2. Pontos de atenção
            3. Pendências
            4. Potencial de inovação
            5. Encaminhamento
            6. Despacho sugerido

            Texto:
            {texto}
            """

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um analista técnico institucional."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.subheader("📊 Resultado")
            st.write(resposta.choices[0].message.content)
