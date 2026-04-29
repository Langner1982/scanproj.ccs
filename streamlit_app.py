import streamlit as st
from openai import OpenAI
import PyPDF2

st.set_page_config(page_title="ScanProj CCS", layout="wide")

# CSS para diminuir títulos
st.markdown("""
<style>
h1 {font-size: 28px !important;}
h2 {font-size: 22px !important;}
h3 {font-size: 18px !important;}
</style>
""", unsafe_allow_html=True)

st.title("🔎 ScanProj CCS")
st.subheader("Análise Inteligente de Projetos")

st.write(
    "Envie os documentos do projeto para gerar uma análise técnica e institucional."
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.divider()

st.header("📂 Upload de documentos")

cadastro = st.file_uploader("PDF do cadastro do projeto", type=["pdf"])
tramitacao = st.file_uploader("PDF da tramitação", type=["pdf"])
anexos = st.file_uploader(
    "Anexos gerais do projeto",
    type=["pdf", "txt"],
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
        st.warning("Envie pelo menos o PDF do cadastro do projeto.")
    else:
        with st.spinner("Analisando..."):

            texto = ""

            if cadastro:
                texto += "\n\n=== CADASTRO ===\n"
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

            prompt = f"""
Você é um analista técnico de projetos do CCS/UFSM.

Realize uma análise objetiva, clara e útil para apoio à decisão, evitando textos longos.

---

1. Classificação Técnica

- Tipo de projeto
- Coerência geral (objetivos, metodologia, cronograma)
- Clareza e consistência

---

2. Pontos de Atenção

Apresente SOMENTE se houver problemas relevantes.

---

3. Pendências

Apresente SOMENTE se houver pendências claras.

---

4. Potencial de Inovação

Classifique:
- Baixo
- Médio
- Alto

Indique se há necessidade de interação com a PROINOVA.

---

5. Alinhamento Estratégico ao PDU

5.1 Eixo:
- Ensino e Formação
- Pesquisa e Pós-Graduação
- Extensão e Impacto Social
- Gestão e Governança
- Pessoas e Bem-estar

5.2 Objetivo relacionado (se possível)

5.3 Grau de alinhamento:
- Alto
- Médio
- Baixo

Justifique brevemente.

---

6. Análise de Riscos

Para cada risco relevante:

- Tipo (estratégico, operacional, financeiro, institucional, externo)
- Probabilidade (baixa, média, alta)
- Impacto (baixo, médio, alto)
- Criticidade (baixa, média, alta, crítica)

Se não houver riscos relevantes, informe de forma breve.

---

7. SWOT (quando aplicável)

Indique apenas pontos relevantes.

---

8. Encaminhamento

Sugira encaminhamento de forma objetiva.

---

9. Despacho

Redija diretamente o despacho (sem título), de forma curta e institucional.

---

Seja direto, evite redundâncias e priorize utilidade prática.

Texto do projeto:
{texto}
"""

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Analista técnico institucional com foco em clareza, objetividade e apoio à decisão."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            st.subheader("📊 Resultado")
            st.write(resposta.choices[0].message.content)
