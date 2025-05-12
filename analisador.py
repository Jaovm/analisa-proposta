import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Analisador de Concorrência Bancária", layout="centered")
st.title("🏦 Analisador de Concorrência Bancária")

# Inicializa estado
if "etapa" not in st.session_state:
    st.session_state.etapa = "concorrente"

st.markdown("### Compare propostas e gere um PDF para o cliente")

# --- Etapa 1: Concorrente ---
if st.session_state.etapa == "concorrente":
    with st.form("form_concorrente", clear_on_submit=True):
        st.subheader("📄 Proposta do Banco Concorrente")
        banco_concorrente = st.text_input("Nome do banco concorrente", value="Banco XPTO")
        valor_emprestimo = st.number_input("Valor do empréstimo (R$)", value=100000.0, step=1000.0, key="valor_emprestimo")
        prazo_meses = st.number_input("Prazo (meses)", value=36, step=1, key="prazo")
        taxa_juros_anual = st.number_input("Taxa de juros anual (%)", value=18.0, key="juros_concorrente")
        cet_total = st.number_input("CET Total (%)", value=22.0, key="cet_concorrente")
        submitted_concorrente = st.form_submit_button("Enviar proposta do concorrente")

    if submitted_concorrente:
        st.session_state.update({
            "banco_concorrente": banco_concorrente,
            "valor_emprestimo": valor_emprestimo,
            "prazo": prazo_meses,
            "taxa_juros_anual": taxa_juros_anual,
            "cet_total": cet_total,
            "etapa": "bb"
        })
        st.experimental_rerun()

# --- Etapa 2: Banco do Brasil ---
elif st.session_state.etapa == "bb":
    with st.form("form_bb", clear_on_submit=True):
        st.subheader("💛 Proposta do Banco do Brasil")
        taxa_bb_anual = st.number_input("Taxa de juros anual do BB (%)", value=15.5, key="juros_bb")
        cet_bb = st.number_input("CET Total do BB (%)", value=17.8, key="cet_bb")
        submitted_bb = st.form_submit_button("Enviar proposta do BB")

    if submitted_bb:
        st.session_state.update({
            "taxa_bb_anual": taxa_bb_anual,
            "cet_bb": cet_bb,
            "etapa": "resultado"
        })
        st.experimental_rerun()

# --- Etapa 3: Resultado e PDF ---
elif st.session_state.etapa == "resultado":
    # Dados
    banco_concorrente = st.session_state.banco_concorrente
    valor_emprestimo = st.session_state.valor_emprestimo
    prazo = st.session_state.prazo
    juros_concorrente = st.session_state.taxa_juros_anual
    cet_concorrente = st.session_state.cet_total
    juros_bb = st.session_state.taxa_bb_anual
    cet_bb = st.session_state.cet_bb

    # Cálculo de parcelas
    taxa_concorrente_mensal = juros_concorrente / 12 / 100
    parcela_concorrente = valor_emprestimo * (taxa_concorrente_mensal * (1 + taxa_concorrente_mensal)**prazo) / ((1 + taxa_concorrente_mensal)**prazo - 1)
    total_concorrente = parcela_concorrente * prazo

    taxa_bb_mensal = juros_bb / 12 / 100
    parcela_bb = valor_emprestimo * (taxa_bb_mensal * (1 + taxa_bb_mensal)**prazo) / ((1 + taxa_bb_mensal)**prazo - 1)
    total_bb = parcela_bb * prazo
    economia = total_concorrente - total_bb

    st.subheader("📊 Comparativo de Propostas")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{banco_concorrente}**")
        st.write(f"Parcela: R$ {parcela_concorrente:,.2f}")
        st.write(f"CET: {cet_concorrente:.2f}%")
        st.write(f"Total pago: R$ {total_concorrente:,.2f}")
    with col2:
        st.write("**Banco do Brasil**")
        st.success(f"Parcela: R$ {parcela_bb:,.2f}")
        st.success(f"CET: {cet_bb:.2f}%")
        st.success(f"Total pago: R$ {total_bb:,.2f}")

    st.markdown(f"### 💰 Economia com o BB: **R$ {economia:,.2f}**")

    st.subheader("🧠 Argumentos Comerciais")
    if cet_bb < cet_concorrente:
        st.info(f"O CET do BB é **{cet_concorrente - cet_bb:.2f}% menor**.")
    if parcela_bb < parcela_concorrente:
        st.info("As parcelas do BB são mais leves, ajudando no fluxo de caixa.")
    st.info("Confiança, solidez e pacote completo de soluções para empresas e PF.")

    # Função PDF
    def gerar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Analisador de Concorrência Bancária", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Resumo da Proposta", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Valor: R$ {valor_emprestimo:,.2f}", ln=True)
        pdf.cell(200, 10, f"Prazo: {prazo} meses", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Proposta - {banco_concorrente}", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Parcela: R$ {parcela_concorrente:,.2f}", ln=True)
        pdf.cell(200, 10, f"CET: {cet_concorrente:.2f}%", ln=True)
        pdf.cell(200, 10, f"Total Pago: R$ {total_concorrente:,.2f}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Proposta - Banco do Brasil", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Parcela: R$ {parcela_bb:,.2f}", ln=True)
        pdf.cell(200, 10, f"CET: {cet_bb:.2f}%", ln=True)
        pdf.cell(200, 10, f"Total Pago: R$ {total_bb:,.2f}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Economia com o BB: R$ {economia:,.2f}", ln=True)

        return pdf

    if st.button("📄 Gerar PDF Comparativo"):
        pdf = gerar_pdf()
        pdf_output = "comparativo_bb_vs_concorrencia.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as file:
            st.download_button("📥 Baixar PDF", file, file_name=pdf_output, mime="application/pdf")
