import streamlit as st
import os
import io
from PIL import Image
import pyzipper

# Configuração da página
st.set_page_config(page_title="Check Extensions", page_icon="🖼️")

st.title("🖼️ Check Extensions")
st.markdown("Converta imagens para JPG e baixe individualmente ou em um pacote ZIP.")


# --- FUNÇÕES DE APOIO ---

def imagem_valida(arquivo_bytes):
    try:
        img = Image.open(arquivo_bytes)
        img.verify()
        return True
    except Exception:
        return False


def processar_imagem_unica(arquivo):
    """Converte uma única imagem e retorna os bytes do JPG."""
    arquivo.seek(0)
    img = Image.open(arquivo)
    img_convertida = img.convert("RGB")
    buffer_img = io.BytesIO()
    img_convertida.save(buffer_img, format="JPEG")
    return buffer_img.getvalue()


def processar_zip(arquivos_carregados, senha=None):
    """Converte múltiplas imagens e retorna os bytes de um arquivo ZIP."""
    buffer_zip = io.BytesIO()
    with pyzipper.AESZipFile(
            buffer_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zipf:
        if senha:
            zipf.setpassword(senha.encode("utf-8"))

        for arquivo in arquivos_carregados:
            if imagem_valida(arquivo):
                arquivo.seek(0)
                img = Image.open(arquivo)
                img_convertida = img.convert("RGB")

                buffer_img = io.BytesIO()
                img_convertida.save(buffer_img, format="JPEG")

                novo_nome = os.path.splitext(arquivo.name)[0] + ".jpg"
                zipf.writestr(novo_nome, buffer_img.getvalue())
    return buffer_zip.getvalue()


# --- INTERFACE ---

arquivos = st.file_uploader(
    "Selecione as imagens",
    type=["jpeg", "png", "bmp", "tiff", "webp", "heic"],
    accept_multiple_files=True
)

if arquivos:
    qtd = len(arquivos)
    st.info(f"📁 {qtd} arquivo(s) selecionado(s).")

    # Configurações na barra lateral
    with st.sidebar:
        st.header("Configurações")

        if qtd > 1:
            st.write("Configurações do ZIP")
            nome_final = st.text_input("Nome do arquivo ZIP", value="imagens_convertidas")
            proteger_senha = st.checkbox("Proteger com senha?")
            senha = st.text_input("Digite a senha", type="password") if proteger_senha else None
        else:
            st.write("Configuração da Imagem")
            nome_original = os.path.splitext(arquivos[0].name)[0]
            nome_final = st.text_input("Nome do arquivo", value=f"{nome_original}_convertida")

    if st.button("🚀 Processar para Download"):
        with st.spinner("Processando..."):
            if qtd == 1:
                # Lógica para arquivo único
                imagem_byte = processar_imagem_unica(arquivos[0])
                st.success("Conversão concluída!")
                st.download_button(
                    label="📥 Baixar Imagem JPG",
                    data=imagem_byte,
                    file_name=f"{nome_final}.jpg",
                    mime="image/jpeg"
                )
            else:
                # Lógica para ZIP
                zip_byte = processar_zip(arquivos, senha)
                st.success("Pacote ZIP pronto!")
                st.download_button(
                    label="📥 Baixar Tudo em ZIP",
                    data=zip_byte,
                    file_name=f"{nome_final}.zip",
                    mime="application/zip"
                )

st.divider()
st.caption(
    "Desenvolvido por [Wendermessias](https://github.com/wendermessias) para verificação e conversão rápida de extensões.")