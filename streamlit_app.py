import streamlit as st
from openai import OpenAI
import PyPDF2

st.set_page_config(page_title="ScanProj CCS", layout="wide")

st.title("🔎 ScanProj CCS")
st.subheader("Análise Inteligente e Estratégica de Projetos")

st.write(
    "Envie os documentos do projeto para gerar uma análise técnica, estratégica, "
    "normativa e alinhada ao PDU do CCS."
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


if st.button("🚀 Gerar análise estratégica"):

    if cadastro is None:
        st.warning("Envie pelo menos o PDF do cadastro do projeto.")
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
Você é um analista técnico e estratégico de projetos do Centro de Ciências da Saúde (CCS/UFSM), atuando com base em princípios de governança pública, planejamento institucional, análise de riscos e apoio à tomada de decisão.

Analise os documentos do projeto considerando aspectos técnicos, normativos, estratégicos e institucionais.

A análise deve funcionar como um filtro estratégico para o CCS, identificando não apenas pendências formais, mas também potencial institucional, relação com o PDU, riscos, inovação, impacto operacional e possíveis encaminhamentos para a Direção.

Apresente a análise estruturada nos seguintes blocos:

---

## 1. Classificação Técnica

Indique:

- tipo de projeto: ensino, pesquisa, extensão, desenvolvimento institucional, prestação de serviço, inovação ou outro;
- coerência entre título, objetivos, metodologia, cronograma, resultados esperados e documentos anexos;
- clareza e consistência geral da proposta.

---

## 2. Pontos de Atenção

Identifique:

- inconsistências;
- fragilidades técnicas;
- lacunas de informação;
- necessidade de conferência documental ou normativa.

Use linguagem cautelosa quando não houver certeza.

---

## 3. Pendências

Indique eventuais pendências:

- documentais;
- formais;
- técnicas;
- de tramitação;
- de complementação pelo proponente.

---

## 4. Potencial de Inovação

Avalie se o projeto apresenta indícios de:

- desenvolvimento de produto, processo, metodologia ou tecnologia;
- software, solução digital ou automação;
- possibilidade de propriedade intelectual;
- parceria com empresas, órgãos públicos ou instituições externas;
- potencial de transferência de tecnologia ou conhecimento;
- aplicação prática com valor institucional ou social.

Classifique o potencial de inovação como:

- Baixo;
- Médio;
- Alto.

Indique se há necessidade de encaminhamento, consulta ou articulação com a PROINOVA.

---

## 5. Alinhamento Estratégico ao PDU

Analise o projeto à luz do Plano de Desenvolvimento da Unidade do CCS.

### 5.1 Eixo estratégico predominante

Classifique em um dos eixos:

- Eixo 1 – Excelência no Ensino e Formação;
- Eixo 2 – Pesquisa e Pós-Graduação;
- Eixo 3 – Impacto Social e Extensão;
- Eixo 4 – Gestão, Governança e Infraestrutura;
- Eixo 5 – Pessoas, Bem-estar e Inclusão.

### 5.2 Objetivo(s) estratégico(s) associado(s)

Indique, quando possível, os objetivos relacionados:

Eixo 1 – Excelência no Ensino e Formação:
- E1O1 – Fortalecer a qualidade dos cursos de graduação;
- E1O2 – Promover a inovação pedagógica e a integração ensino–aprendizagem;
- E1O3 – Qualificar a experiência acadêmica e a permanência estudantil;
- E1O4 – Qualificar a infraestrutura e os recursos de ensino.

Eixo 2 – Pesquisa e Pós-Graduação:
- E2O5 – Fortalecer a pós-graduação e a produção científica;
- E2O6 – Ampliar a captação de recursos e projetos de pesquisa;
- E2O7 – Promover a internacionalização da pesquisa;
- E2O8 – Ampliar a visibilidade e o impacto da produção científica.

Eixo 3 – Impacto Social e Extensão:
- E3O9 – Fortalecer a extensão universitária e a interação com a sociedade;
- E3O10 – Ampliar a integração ensino–serviço–comunidade;
- E3O11 – Consolidar parcerias institucionais estratégicas;
- E3O12 – Ampliar o impacto social das ações do CCS.

Eixo 4 – Gestão, Governança e Infraestrutura:
- E4O13 – Fortalecer a governança e o planejamento institucional do CCS;
- E4O14 – Aprimorar a gestão administrativa e a comunicação institucional;
- E4O15 – Promover transparência e participação na gestão;
- E4O16 – Qualificar a infraestrutura física e tecnológica do Centro.

Eixo 5 – Pessoas, Bem-estar e Inclusão:
- E5O17 – Promover a saúde mental e o bem-estar da comunidade acadêmica;
- E5O18 – Fortalecer políticas de inclusão, diversidade e acessibilidade;
- E5O19 – Qualificar o ambiente institucional e as relações interpessoais.

### 5.3 Grau de alinhamento com o PDU

Classifique como:

- Alto;
- Médio;
- Baixo.

Justifique brevemente.

### 5.4 Classificação estratégica do projeto

Classifique como:

- Operacional: projeto de rotina ou baixo impacto estratégico;
- Relevante: contribui pontualmente para objetivos do CCS;
- Estratégico: impacta diretamente objetivos do PDU;
- Alto impacto institucional: possui potencial estruturante para o Centro.

### 5.5 Contribuições potenciais

Indique se o projeto pode contribuir para:

- indicadores institucionais;
- metas do PDU;
- captação de recursos;
- inovação;
- impacto social;
- fortalecimento de parcerias;
- melhoria de processos;
- redução de riscos institucionais.

---

## 6. Análise de Riscos

Identifique riscos associados ao projeto.

Para cada risco relevante, indique:

- descrição do risco;
- tipo: estratégico, operacional, financeiro, institucional, externo, normativo ou tecnológico;
- probabilidade: baixa, média ou alta;
- impacto: baixo, médio ou alto;
- criticidade: baixa, média, alta ou crítica;
- possível medida de mitigação.

Considere especialmente riscos relacionados a:

- inconsistência documental;
- baixa viabilidade de execução;
- ausência de clareza no plano de trabalho;
- dependência de recursos externos;
- fragilidade de parcerias;
- risco de retrabalho;
- sobrecarga da equipe;
- insegurança normativa;
- riscos à imagem institucional;
- riscos de perda de oportunidade estratégica.

---

## 7. Relação com a Matriz SWOT do CCS

Indique como o projeto se relaciona com a matriz SWOT do CCS.

Considere, quando aplicável:

### Forças
- identidade acadêmica consolidada na área da saúde;
- integração potencial entre ensino, pesquisa, extensão e SUS;
- produção científica relevante;
- capacidade de atuação em áreas estratégicas;
- inserção regional significativa.

### Fraquezas
- infraestrutura heterogênea;
- processos administrativos que demandam padronização;
- monitoramento por indicadores ainda em consolidação;
- risco de baixa adesão institucional às estratégias do PDU;
- sobrecarga de servidores, docentes ou gestores.

### Oportunidades
- avanço da saúde digital;
- ampliação de oportunidades de captação de recursos em PD&I;
- expansão de parcerias com municípios, hospitais e redes do SUS;
- fortalecimento da agenda de governança, riscos e transparência;
- valorização de indicadores de impacto social e qualidade acadêmica.

### Ameaças
- incertezas orçamentárias;
- pressão por resultados sem expansão proporcional de recursos;
- instabilidade de parcerias externas;
- rápida obsolescência tecnológica;
- riscos associados à saúde mental, evasão e engajamento;
- exigências crescentes de transparência e prestação de contas.

---

## 8. Complexidade Operacional e Impacto na Equipe

Avalie:

- grau de complexidade do projeto: baixo, médio ou alto;
- potencial de retrabalho: baixo, médio ou alto;
- grau de clareza das informações: baixo, médio ou alto;
- nível de insegurança normativa ou documental;
- necessidade de acompanhamento mais próximo pelo GAP ou pela Direção.

Indique se o projeto pode gerar sobrecarga, estresse, insegurança operacional ou necessidade de suporte adicional.

---

## 9. Encaminhamento Estratégico

Indique, quando aplicável:

- prosseguimento da tramitação;
- necessidade de complementação;
- devolução para ajuste;
- encaminhamento à comissão competente;
- consulta ou articulação com a PROINOVA;
- acompanhamento prioritário pela Direção;
- integração com ações do PDU;
- tratamento como projeto estratégico do CCS;
- inclusão em painel ou instrumento de monitoramento do PDU.

---

## 10. Despacho Sugerido

Redija um despacho institucional, claro, técnico, respeitoso e objetivo, adequado ao padrão administrativo do CCS.

O despacho deve ser curto, utilizável em processo administrativo e compatível com o encaminhamento sugerido.

---

## Orientações de linguagem

- Use linguagem institucional, objetiva e cautelosa.
- Evite afirmações categóricas quando os documentos não permitirem conclusão segura.
- Utilize expressões como:
  - “aparentemente”;
  - “há indícios de”;
  - “recomenda-se verificar”;
  - “sugere-se”;
  - “salvo melhor juízo da instância competente”.
- Não aprove nem indefira o projeto de forma definitiva.
- A análise deve apoiar a decisão humana, não substituí-la.

Documentos analisados:
{texto}
"""

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um analista técnico institucional especializado em projetos acadêmicos, "
                            "governança pública, planejamento estratégico, gestão de riscos e inovação no setor público."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            st.subheader("📊 Resultado da análise")
            st.write(resposta.choices[0].message.content)
