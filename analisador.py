import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Analisador de Concorrência Bancária", layout="centered")

st.title("🏦 Analisador de Concorrência Bancária")
st.subheader("Compare propostas e gere um PDF personalizado para o cliente")

# --- Entrada da proposta concorrente ---
st.markdown("## 📄 Proposta do Banco Concorrente")
with st.form("form_concorrente"):
    banco_concorrente = st.text_input("Nome do banco concorrente", value="Banco XPTO")
    valor_emprestimo = st.number_input("Valor do empréstimo (R$)", value=100000.0, step=1000.0)
    prazo_meses = st.number_input("Prazo (meses)", value=36, step=1)
    taxa_juros_anual = st.number_input("Taxa de juros anual (%)", value=18.0)
    cet_total = st.number_input("CET Total (%)", value=22.0)
    submitted_concorrente = st.form_submit_button("Próximo")

if submitted_concorrente:
    # --- Entrada da proposta BB ---
    st.markdown("## 💛 Proposta do Banco do Brasil")
    with st.form("form_bb"):
        taxa_bb_anual = st.number_input("Taxa de juros anual do BB (%)", value=15.5)
        cet_bb = st.number_input("CET Total do BB (%)", value=17.8)
        submitted_ambas = st.form_submit_button("Comparar Propostas")

    if submitted_ambas:
        # Cálculo concorrente
        taxa_concorrente_mensal = taxa_juros_anual / 12 / 100
        parcela_concorrente = valor_emprestimo * (taxa_concorrente_mensal * (1 + taxa_concorrente_mensal)**prazo_meses) / ((1 + taxa_concorrente_mensal)**prazo_meses - 1)
        total_pago_concorrente = parcela_concorrente * prazo_meses

        # Cálculo BB
        taxa_bb_mensal = taxa_bb_anual / 12 / 100
        parcela_bb = valor_emprestimo * (taxa_bb_mensal * (1 + taxa_bb_mensal)**prazo_meses) / ((1 + taxa_bb_mensal)**prazo_meses - 1)
        total_pago_bb = parcela_bb * prazo_meses

        # Exibição
        st.markdown("## 📊 Comparativo de Propostas")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{banco_concorrente}**")
            st.write(f"Parcela: R$ {parcela_concorrente:,.2f}")
            st.write(f"CET: {cet_total:.2f}%")
            st.write(f"Total pago: R$ {total_pago_concorrente:,.2f}")
        with col2:
            st.write("**Banco do Brasil**")
            st.success(f"Parcela: R$ {parcela_bb:,.2f}")
            st.success(f"CET: {cet_bb:.2f}%")
            st.success(f"Total pago: R$ {total_pago_bb:,.2f}")

        economia = total_pago_concorrente - total_pago_bb
        st.markdown(f"### 💰 Economia total com o BB: **R$ {economia:,.2f}**")

        # Sugestões de argumento
        st.markdown("## 🧠 Argumentos Comerciais")
        if cet_bb < cet_total:
            st.info(f"O CET do BB é **{cet_total - cet_bb:.2f}% menor**.")
        if parcela_bb < parcela_concorrente:
            st.info("As parcelas do BB são mais leves, ajudando no fluxo de caixa.")
        st.info("Destaque: confiança de mercado, combo de produtos e canais digitais avançados.")

        # --- Gerar PDF ---
        def gerar_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Analisador de Concorrência Bancária", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt="Resumo da Proposta", ln=True)
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=f"Valor do Empréstimo: R$ {valor_emprestimo:,.2f}", ln=True)
            pdf.cell(200, 10, txt=f"Prazo: {prazo_meses} meses", ln=True)
            pdf.ln(5)

            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt=f"Proposta - {banco_concorrente}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Parcela: R$ {parcela_concorrente:,.2f}", ln=True)
            pdf.cell(200, 10, txt=f"CET: {cet_total:.2f}%", ln=True)
            pdf.cell(200, 10, txt=f"Total Pago: R$ {total_pago_concorrente:,.2f}", ln=True)
            pdf.ln(5)

            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt="Proposta - Banco do Brasil", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Parcela: R$ {parcela_bb:,.2f}", ln=True)
            pdf.cell(200, 10, txt=f"CET: {cet_bb:.2f}%", ln=True)
            pdf.cell(200, 10, txt=f"Total Pago: R$ {total_pago_bb:,.2f}", ln=True)
            pdf.ln(5)

            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt=f"Economia com o BB: R$ {economia:,.2f}", ln=True)

            return pdf

        if st.button("📄 Gerar PDF Comparativo"):
            pdf = gerar_pdf()
            pdf_output = "comparativo_bb_vs_concorrencia.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as file:
                st.download_button("📥 Baixar PDF", file, file_name=pdf_output, mime="application/pdf")
