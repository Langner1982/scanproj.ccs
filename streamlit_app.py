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

def ler_txt(arquivo):
    return arquivo.read().decode("utf-8", errors="ignore")

if st.button("🚀 Gerar análise"):

    if cadastro is None:
        st.warning("Envie pelo menos o PDF do cadastro.")
    else:
        with st.spinner("Analisando documentos..."):

            texto = ""

            if cadastro:
                texto += "\n\n=== CADASTRO DO PROJETO ===\n"
                texto += ler_pdf(cadastro)

            if tramitacao:
                texto += "\n\n=== TRAMITAÇÃO ===\n"
                texto += ler_pdf(tramitacao)

            if anexos:
                for arquivo in anexos:
                    texto += f"\n\n=== ANEXO: {arquivo.name} ===\n"

                    if arquivo.type == "application/pdf":
                        texto += ler_pdf(arquivo)

                    elif arquivo.type == "text/plain":
                        texto += ler_txt(arquivo)

                    else:
                        texto += "[Arquivo anexado, mas leitura automática ainda não disponível para este formato.]"

            prompt = f"""
Você é um analista técnico de projetos do CCS/UFSM.

Analise os documentos abaixo de forma integrada, com linguagem objetiva, institucional e cautelosa.

Considere especialmente:
- coerência entre cadastro, tramitação e anexos;
- compatibilidade entre título, resumo, objetivos, metodologia, cronograma e plano de trabalho;
- existência de pendências documentais;
- clareza quanto ao órgão promotor;
- presença de recurso externo, parceria, prestação de serviço ou captação;
- potencial de inovação, mesmo que o proponente não tenha marcado essa opção;
- eventual necessidade de consulta ou encaminhamento à PROINOVA.

Gere a resposta obrigatoriamente nesta estrutura:

1. Classificação técnica preliminar
2. Síntese do projeto
3. Pontos de atenção
4. Pendências ou inconsistências
5. Potencial de inovação
6. Necessidade de análise pela PROINOVA
7. Encaminhamento sugerido
8. Grau de atenção
9. Despacho sugerido

Use expressões como “aparentemente”, “recomenda-se verificar”, “há indícios de” e “salvo melhor juízo” quando não houver certeza documental.

Documentos analisados:
{texto}
"""

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um analista técnico institucional, especializado em análise preliminar de projetos acadêmicos e administrativos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.subheader("📊 Resultado da análise")
            st.write(resposta.choices[0].message.content)
