🖼️ Check Extensions & Converter

Este projeto é uma ferramenta web interativa desenvolvida em Python utilizando Streamlit. Ela permite que usuários realizem o upload de múltiplas imagens, verifiquem sua integridade, convertam-nas automaticamente para o formato JPG e as baixem de forma otimizada.

O grande diferencial é a lógica inteligente de download: se você converter apenas uma imagem, recebe o arquivo direto; se forem várias, o sistema gera um pacote ZIP que pode ser protegido por senha.

✨ Funcionalidades

Upload Múltiplo: Suporte para diversos formatos (PNG, WEBP, BMP, TIFF, HEIC, etc.).

Conversão Inteligente: Transforma qualquer formato de imagem válido em JPG (RGB) de alta compatibilidade.

Validação de Arquivos: Verifica se as imagens não estão corrompidas antes de processar.

Segurança (ZIP): Opção de compactar múltiplas imagens em um arquivo .zip com criptografia AES-256 via senha.

Interface Adaptativa:

1 imagem = Download direto do .jpg.

2+ imagens = Download de pacote .zip.

🚀 Tecnologias Utilizadas

Python - Linguagem base.

Streamlit - Framework para a interface web.

Pillow (PIL) - Processamento e conversão de imagens.

Pyzipper - Compactação de arquivos com criptografia avançada.