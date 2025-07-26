import streamlit as st
import re
from collections import OrderedDict

st.set_page_config(page_title="Generador Poético con Pi", layout="wide")

st.title("📐 Generador Poético con los decimales de π")
st.markdown("Transforma cualquier texto en un poema único utilizando los decimales de π como clave matemática y genera tankas japoneses.")

# Limpia y normaliza el texto
def limpiar_texto(texto):
    palabras = re.findall(r"\b[a-záéíóúüñ]+\b", texto.lower())
    palabras_unicas = list(OrderedDict.fromkeys(palabras))
    return palabras_unicas

# Carga los decimales de pi
@st.cache_data
def cargar_decimales_pi():
    with open("pi_decimals.txt", "r") as f:
        return f.read().strip().replace("\n", "")

def generar_versos(palabras, longitud=7):
    return [palabras[i:i+longitud] for i in range(0, len(palabras), longitud) if len(palabras[i:i+longitud]) == longitud]

def transformar_en_tanka(verso):
    if len(verso) != 7:
        return None
    return f"{verso[0]}\n{verso[1]} {verso[2]}\n{verso[3]}\n{verso[4]} {verso[5]}\n{verso[6]}"

archivo_subido = st.file_uploader("📄 Sube un archivo .txt", type="txt")

if archivo_subido:
    texto = archivo_subido.read().decode("utf-8")
    palabras = limpiar_texto(texto)
    total = len(palabras)
    st.success(f"✔️ El texto contiene {total} palabras únicas.")

    pi = cargar_decimales_pi()
    usados = set()
    resultado = []
    i = 0

    while len(usados) < total and i + 4 <= len(pi):
        bloque = int(pi[i:i+4])
        if 1 <= bloque <= total and bloque not in usados:
            resultado.append(palabras[bloque - 1])
            usados.add(bloque)
        i += 1

    poema = " ".join(resultado)
    st.markdown("### ✨ Poema generado:")
    st.text_area("Poema:", poema, height=200)
    st.download_button("💾 Descargar poema", poema, file_name="poema_pi.txt", mime="text/plain")

    # Generar versos de 7 palabras
    versos = generar_versos(resultado)
    tankas = [transformar_en_tanka(verso) for verso in versos if transformar_en_tanka(verso)]

    if tankas:
        st.markdown("### 🈴 Tankas generados:")
        st.text_area("Tankas:", "\n\n".join(tankas), height=400)
        st.download_button("💾 Descargar tankas", "\n\n".join(tankas), file_name="tankas_pi.txt", mime="text/plain")

else:
    st.info("📥 Sube un archivo .txt para comenzar.")