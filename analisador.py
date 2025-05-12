import streamlit as st

st.set_page_config(page_title="Analisador de Concorrência Bancária", layout="centered")

st.title("🏦 Analisador de Concorrência Bancária")
st.subheader("Compare uma proposta de crédito com as condições do Banco do Brasil")

st.markdown("### 📄 Proposta da Concorrência")
with st.form("concorrencia"):
    banco_concorrente = st.text_input("Nome do Banco Concorrente", value="Banco XPTO")
    valor_emprestimo = st.number_input("Valor do empréstimo (R$)", value=100000.0, step=1000.0)
    prazo_meses = st.number_input("Prazo (meses)", value=36, step=1)
    taxa_juros_anual = st.number_input("Taxa de juros anual (%)", value=18.0, step=0.1)
    cet_total = st.number_input("CET Total (%)", value=22.0, step=0.1)
    submitted = st.form_submit_button("Analisar Proposta")

if submitted:
    st.markdown("### 🧮 Simulando Proposta do Banco do Brasil")

    # Simulação BB (você pode usar dados reais ou fixos aqui)
    taxa_bb_anual = 15.5
    cet_bb = 17.8
    taxa_bb_mensal = taxa_bb_anual / 12 / 100
    parcela_bb = valor_emprestimo * (taxa_bb_mensal * (1 + taxa_bb_mensal)**prazo_meses) / ((1 + taxa_bb_mensal)**prazo_meses - 1)
    total_pago_bb = parcela_bb * prazo_meses

    # Concorrente
    taxa_concorrente_mensal = taxa_juros_anual / 12 / 100
    parcela_concorrente = valor_emprestimo * (taxa_concorrente_mensal * (1 + taxa_concorrente_mensal)**prazo_meses) / ((1 + taxa_concorrente_mensal)**prazo_meses - 1)
    total_pago_concorrente = parcela_concorrente * prazo_meses

    st.write(f"**Banco Concorrente:** {banco_concorrente}")
    st.write(f"📌 Parcela: R$ {parcela_concorrente:,.2f}")
    st.write(f"📌 CET: {cet_total:.2f}%")
    st.write("---")
    st.write("**Banco do Brasil (Simulado):**")
    st.success(f"📌 Parcela: R$ {parcela_bb:,.2f}")
    st.success(f"📌 CET: {cet_bb:.2f}%")

    # Comparação
    st.markdown("### 📊 Comparativo")
    st.write(f"💸 Economia total com o BB: R$ {(total_pago_concorrente - total_pago_bb):,.2f}")
    st.write("---")

    # Argumentos de Venda
    st.markdown("### 🧠 Sugestão de Argumentos de Venda")
    if cet_bb < cet_total:
        st.info(f"O CET do BB é **{(cet_total - cet_bb):.2f}% menor**. Mostre que o custo total é mais vantajoso, mesmo com parcelas próximas.")
    if parcela_bb < parcela_concorrente:
        st.info("As parcelas do BB são mais leves, ajudando no fluxo de caixa da empresa.")
    st.info("Lembre o cliente sobre diferenciais do BB: confiança de mercado, canais digitais, possibilidade de combo com seguros ou investimentos.")
