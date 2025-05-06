from io import BytesIO
import os
import shutil
import requests
from dotenv import load_dotenv
import urllib.parse
from bs4 import BeautifulSoup

load_dotenv()

HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")

import os
import requests

def gerar_imagem_por_ia_huggingface(prompt, nome_base, token_hf=HUGGINGFACE_KEY):
    """
    Gera uma imagem com base no prompt e salva com nome baseado no artigo.
    Retorna o caminho do arquivo gerado.
    """
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

    headers = {
        "Authorization": f"Bearer {token_hf}"
    }

    payload = {
        "inputs": prompt,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        caminho_arquivo = f"artigos/{nome_base}.png"
        with open(caminho_arquivo, "wb") as f:
            f.write(response.content)
        return caminho_arquivo
    else:
        raise Exception(f"Erro ao gerar imagem: {response.status_code} - {response.text}")


def buscar_imagens_licenca_livre(termo_pesquisa):
    """
    Realiza uma pesquisa no Google Imagens filtrando por imagens com licenças livres de uso.

    Parâmetros:
    - termo_pesquisa: termo a ser pesquisado.

    Retorna:
    - Lista de URLs de imagens.
    """
    num_imagens = 1
    # Codifica o termo de pesquisa para uso em URL
    termo_codificado = urllib.parse.quote(termo_pesquisa)

    # URL de pesquisa no Google Imagens com filtro de licença livre
    url = f"https://www.google.com/search?q={termo_codificado}&tbm=isch&tbs=il:cl"

    # Define os headers para simular um navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Realiza a requisição HTTP
    resposta = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if resposta.status_code != 200:
        print("Erro ao realizar a requisição.")
        return []

    # Analisa o conteúdo HTML da resposta
    soup = BeautifulSoup(resposta.text, 'html.parser')

    # Encontra todas as tags de imagem
    tags_imagem = soup.find_all("img")

    # Extrai os URLs das imagens
    urls_imagens = []
    for tag in tags_imagem:
        src = tag.get("src")
        if src and src.startswith("http"):
            urls_imagens.append(src)
        if len(urls_imagens) >= num_imagens:
            break

    return urls_imagens

def mesclar_imagens(path_ia, urls_livres):
    """
    Salva imagem gerada por IA e as imagens livres em uma pasta com base no nome da imagem IA.
    """
    nome_base = os.path.splitext(os.path.basename(path_ia))[0]
    pasta_destino = os.path.join("imagens", nome_base)
    os.makedirs(pasta_destino, exist_ok=True)

    shutil.copy(path_ia, os.path.join(pasta_destino, "ia.png"))

    for i, url in enumerate(urls_livres):
        try:
            resposta = requests.get(url, timeout=10)
            if resposta.status_code == 200:
                with open(os.path.join(pasta_destino, f"livre_{i}.jpg"), "wb") as f:
                    f.write(resposta.content)
        except:
            print(f"⚠️ Erro ao baixar imagem livre: {url}")

    return os.path.join(pasta_destino, "ia.png") 
    
