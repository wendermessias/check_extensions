import os
import sys
import io
from PIL import Image
from tkinter import Tk, filedialog
import pyzipper  # Biblioteca que permite compactar com senha

# Ajuste de codificação para saída UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Diretórios fixos
PASTA_CONVERTIDAS = "pasta_convertidas"
LOG_FILE = "log.txt"


# Escolher pasta de origem
def escolher_pasta_origem():
    root = Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Selecione a pasta com imagens")
    return pasta


# Verifica se há imagens válidas
def tem_imagens_validas(pasta):
    extensoes = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".heic")
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(extensoes):
            caminho = os.path.join(pasta, arquivo)
            if imagem_valida(caminho):
                return True
    return False


# Verifica se imagem está corrompida
def imagem_valida(caminho):
    try:
        with Image.open(caminho) as img:
            img.verify()
        return True
    except Exception:
        return False


# Compactar com nome e senha opcional
def compactar_zip():
    usar_senha = (
        input("🔐 Deseja proteger o ZIP com uma senha? (s/n): ").strip().lower()
    )
    senha = None

    if usar_senha == "s":
        senha = input("Digite a senha desejada: ").strip()

    nome_zip = input(
        "📦 Digite o nome desejado para o arquivo ZIP (sem extensão): "
    ).strip()
    if not nome_zip:
        nome_zip = "imagens_convertidas"
    nome_zip += ".zip"

    with pyzipper.AESZipFile(
        nome_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zipf:
        if senha:
            zipf.setpassword(senha.encode("utf-8"))
        for arquivo in os.listdir(PASTA_CONVERTIDAS):
            caminho = os.path.join(PASTA_CONVERTIDAS, arquivo)  
            zipf.write(caminho, arcname=arquivo)

    print(f"✅ Arquivo ZIP criado: {nome_zip}")
    if senha:
        print("🔐 Protegido com senha.")
    return nome_zip


# Conversão de imagens
def converter_imagens(pasta_origem):
    os.makedirs(PASTA_CONVERTIDAS, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        for arquivo in os.listdir(pasta_origem):
            caminho = os.path.join(pasta_origem, arquivo)
            if imagem_valida(caminho):
                try:
                    with Image.open(caminho) as img:
                        novo_nome = os.path.splitext(arquivo)[0] + ".jpg"
                        destino = os.path.join(PASTA_CONVERTIDAS, novo_nome)
                        img.convert("RGB").save(destino, "JPEG")
                        log.write(f"✅ Convertido: {arquivo}\n")
                except Exception as e:
                    log.write(f"❌ Erro ao converter {arquivo}: {e}\n")
            else:
                log.write(f"⚠️ Arquivo corrompido: {arquivo}\n")
    print("🖼️ Conversão concluída.")


# Menu interativo
def menu_interativo(pasta_origem):
    nome_zip = None
    while True:
        print("\n📋 Menu de opções:")
        print("• [1] Converter imagens")
        print("• [2] Compactar em ZIP")
        print("• [3] Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            converter_imagens(pasta_origem)
        elif escolha == "2":
            nome_zip = compactar_zip()
        elif escolha == "3":
            print("👋 Encerrando...")
            break
        else:
            print("❌ Opção inválida.")


# Execução principal
if __name__ == "__main__":
    os.makedirs(PASTA_CONVERTIDAS, exist_ok=True)

    pasta_origem = escolher_pasta_origem()
    if pasta_origem and tem_imagens_validas(pasta_origem):
        print(f"📂 Pasta selecionada: {pasta_origem}")
        menu_interativo(pasta_origem)
    else:
        print("⚠️ Nenhuma imagem válida encontrada na pasta selecionada. Encerrando.")