
import streamlit as st
import re
import pandas as pd
from collections import Counter

# Correções simples e gírias comuns
substituicoes = {
    r'\bmuito bom\b': 'excelente',
    r'\blegal\b': 'interessante',
    r'\be\b': 'é',
    r'\bmais\b': 'mas',
    r'\bprecisa melhorar\b': 'pode ser aprimorado',
    r'\bmuito interessante\b': 'relevante',
    r'\bom\b': 'adequado',
    r'\bcoisa\b': 'aspecto',
    r'\bnegócio\b': 'situação',
    r'\bmelhorar na parte da linguagem\b': 'refinar a estrutura linguística',
    r'\bnois\b': 'nós',
    r'\bnois vai\b': 'nós vamos',
    r'\bvai para escola\b': 'vamos para a escola',
    r'\bvamo\b': 'vamos',
    r'\bta\b': 'está',
    r'\bpra\b': 'para',
    r'\bnem\b': 'nem mesmo',
    r'\btamo junto\b': 'estamos juntos'
}

# Função de correção e sugestão
def corrigir_texto(texto):
    sugestoes = []
    texto_corrigido = texto

    for padrao, substituto in substituicoes.items():
        ocorrencias = re.findall(padrao, texto_corrigido, re.IGNORECASE)
        for oc in ocorrencias:
            sugestoes.append(f"Sugestão: Substituir '{oc}' por '{substituto}'")
        texto_corrigido = re.sub(padrao, substituto, texto_corrigido, flags=re.IGNORECASE)

    return texto_corrigido, sugestoes

# Estatísticas básicas do texto
def estatisticas_texto(texto):
    palavras = re.findall(r'\b\w+\b', texto.lower())
    frases = re.split(r'[.!?]', texto)
    contagem_palavras = len(palavras)
    contagem_frases = len([f for f in frases if f.strip() != ''])
    repetidas = Counter(palavras)
    mais_repetidas = repetidas.most_common(5)

    return contagem_palavras, contagem_frases, mais_repetidas

# Interface
st.title("🧠 Revisor de Textos com IA + Big Data")
st.write("Insira seu texto para receber correções, sugestões de estilo e estatísticas linguísticas.")

texto_usuario = st.text_area("Digite ou cole seu texto:")

if st.button("Revisar Texto"):
    if texto_usuario.strip():
        texto_corrigido, sugestoes = corrigir_texto(texto_usuario)
        st.subheader("✅ Texto Corrigido")
        st.write(texto_corrigido)

        st.subheader("💡 Sugestões de Melhoria")
        if sugestoes:
            for s in sugestoes:
                st.markdown(f"- {s}")
        else:
            st.write("Nenhuma sugestão encontrada. Ótimo texto!")

        st.subheader("📊 Estatísticas do Texto")
        palavras, frases, repetidas = estatisticas_texto(texto_usuario)
        st.markdown(f"**Palavras:** {palavras}")
        st.markdown(f"**Frases:** {frases}")
        st.markdown("**Palavras mais repetidas:**")
        for palavra, qtd in repetidas:
            st.markdown(f"- {palavra}: {qtd}x")

        # Simulação de Big Data: salva os dados em CSV
        df = pd.DataFrame({
            'Texto Original': [texto_usuario],
            'Texto Corrigido': [texto_corrigido],
            'Sugestoes': ['; '.join(sugestoes)]
        })
        df.to_csv("sugestoes_historico.csv", mode='a', header=False, index=False)

    else:
        st.warning("⚠️ Por favor, insira um texto para revisão.")
