import os
import random
import base64
import requests
import logging
import unicodedata
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import Optional

# Setup de logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

# Carregando variáveis do ambiente
load_dotenv()

# Constantes de configuração
WORDPRESS_URL: str = os.getenv("WORDPRESS_URL", "").strip()
USERNAME: str = os.getenv("WORDPRESS_USERNAME", "").strip()
APPLICATION_PASSWORD: str = os.getenv("WORDPRESS_APP_PASSWORD", "").strip()
AUTORES: list[int] = list(map(int, os.getenv("AUTORES", "1").split(",")))
DEFAULT_CATEGORY_ID: int = int(os.getenv("CATEGORIA_ID", "1"))
ARTIGOS_DIR: str = "artigos"

# Headers para autenticação
basic_token = base64.b64encode(f"{USERNAME}:{APPLICATION_PASSWORD}".encode()).decode("utf-8")
HEADERS_POST = {
    "Authorization": f"Basic {basic_token}",
    "Content-Type": "application/json"
}
HEADERS_MEDIA = {
    "Authorization": f"Basic {basic_token}"
}


def sanitize_filename(name: str) -> str:
    """Remove acentuação e caracteres especiais de um nome de arquivo."""
    return unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")


def upload_image(image_path: str) -> str:
    """Faz o upload de uma imagem para o WordPress e retorna sua URL."""
    if not os.path.exists(image_path):
        print(f"Arquivo não encontrado: {image_path}")
        return ""

    filename = sanitize_filename(os.path.basename(image_path))
    headers = HEADERS_MEDIA.copy()
    headers["Content-Disposition"] = f'attachment; filename="{filename}"'

    try:
        print(f"Preparando o upload da imagem: {image_path}")
        with open(image_path, "rb") as img_file:
            response = requests.post(
                f"{WORDPRESS_URL}/wp-json/wp/v2/media",  # Certifique-se da URL correta aqui!
                headers=headers,
                files={"file": (filename, img_file, "image/jpeg")}
            )

        if response.status_code in (200, 201):
            try:
                response_json = response.json()

                # Use "source_url" diretamente
                uploaded_url = response_json.get("source_url")

                if uploaded_url:
                    print(f"Imagem {image_path} carregada com sucesso. URL: {uploaded_url}")
                    return uploaded_url
                else:
                    print("Erro: 'source_url' não encontrado na resposta.")
            except Exception as e:
                print(f"Erro ao processar a resposta JSON: {e}")
        else:
            print(f"Erro ao carregar a imagem: {image_path}, status code: {response.status_code}")
            print("Resposta do servidor:", response.text)

    except Exception as e:
        print(f"Falha ao carregar a imagem {image_path}: {e}")

    return ""


def get_category_id(raw_slug: Optional[str]) -> int:
    """Obtém o ID da categoria com base em seu slug ou nome."""
    if not raw_slug:
        return DEFAULT_CATEGORY_ID

    slug = sanitize_filename(raw_slug).lower().strip().replace(" ", "-")

    # 1ª tentativa: buscar por slug
    try:
        resp = requests.get(
            f"{WORDPRESS_URL}/wp-json/wp/v2/categories",
            headers=HEADERS_POST,
            params={"slug": slug}
        )
        if resp.ok and resp.json():
            cat_id = resp.json()[0]["id"]
            logging.info(f"Categoria encontrada por slug '{slug}': ID {cat_id}")
            return cat_id
    except Exception as e:
        logging.error(f"Erro ao buscar categoria por slug: {e}")

    # 2ª tentativa: buscar por nome
    try:
        resp = requests.get(
            f"{WORDPRESS_URL}/wp-json/wp/v2/categories",
            headers=HEADERS_POST,
            params={"search": slug}
        )
        if resp.ok:
            for cat in resp.json():
                if cat.get("name", "").lower() == raw_slug.lower().strip():
                    logging.info(f"Categoria encontrada por nome '{raw_slug}': ID {cat['id']}")
                    return cat["id"]
    except Exception as e:
        logging.error(f"Erro ao buscar categoria por nome: {e}")

    logging.warning(f"Categoria '{raw_slug}' não encontrada. Usando fallback: {DEFAULT_CATEGORY_ID}")
    return DEFAULT_CATEGORY_ID


def process_html_file(file_path: str) -> tuple[str, str, int]:
    """Lê e processa o HTML retornando título, conteúdo HTML e categoria."""
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    title = soup.title.string if soup.title else "Sem título"
    meta_cat = soup.find("meta", {"name": "category"})
    slug = meta_cat["content"] if meta_cat and meta_cat.get("content") else None
    category_id = get_category_id(slug)

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not src.startswith("http"):
            local_path = os.path.join(os.path.dirname(file_path), src)
            uploaded_url = upload_image(local_path)
            if uploaded_url:
                img["src"] = uploaded_url

    return title, str(soup), category_id


def publish_article(file_path: str) -> None:
    """Publica um único artigo no WordPress."""
    title, content, category_id = process_html_file(file_path)

    payload = {
        "title": title,
        "content": content,
        "status": "publish",
        "author": random.choice(AUTORES),
        "categories": [category_id],
    }

    try:
        response = requests.post(
            f"{WORDPRESS_URL}/wp-json/wp/v2/posts",
            headers=HEADERS_POST,
            json=payload
        )
        logging.info(f"Publicado '{title}' → Status: {response.status_code}")
        logging.debug(f"Resposta: {response.text}")
    except Exception as e:
        logging.error(f"Erro ao publicar artigo '{title}': {e}")


def publish_all_articles(directory: str = ARTIGOS_DIR) -> None:
    """Publica todos os arquivos HTML encontrados no diretório especificado."""
    if not os.path.isdir(directory):
        logging.error(f"Diretório não encontrado: {directory}")
        return

    html_files = [f for f in os.listdir(directory) if f.lower().endswith(".html")]
    if not html_files:
        logging.info("Nenhum arquivo HTML encontrado.")
        return

    for filename in html_files:
        full_path = os.path.join(directory, filename)
        logging.info(f"Publicando: {filename}")
        publish_article(full_path)
