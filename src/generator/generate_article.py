import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def baixa_imagens_licenca_livre(termo_pesquisa, nome_base, index):
    """
    Busca e salva uma imagem com licença livre do Google Imagens.

    Parâmetros:
    - termo_pesquisa (str): termo a ser pesquisado.
    - pasta_destino (str): pasta onde a imagem será salva.

    Retorna:
    - Caminho do arquivo salvo ou None.
    """

    num_imagens = 1
    termo_codificado = urllib.parse.quote(termo_pesquisa)
    url = f"https://www.google.com/search?q={termo_codificado}&tbm=isch&tbs=il:cl"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resposta = requests.get(url, headers=headers)
    if resposta.status_code != 200:
        print("Erro ao realizar a requisição.")
        return None

    soup = BeautifulSoup(resposta.text, 'html.parser')
    tags_imagem = soup.find_all("img")

    urls_imagens = []
    for tag in tags_imagem:
        src = tag.get("src")
        if src and src.startswith("http"):
            urls_imagens.append(src)
        if len(urls_imagens) >= num_imagens:
            break

    if not urls_imagens:
        print("Nenhuma imagem encontrada.")
        return None

    os.makedirs("artigos", exist_ok=True)

    try:
        url_imagem = urls_imagens[0]
        resposta_img = requests.get(url_imagem)
        imagem = Image.open(BytesIO(resposta_img.content))

        img_path = f"artigos/{nome_base}_imagem_{index}.jpg"
        imagem.save(img_path)
        return img_path
    except Exception as e:
        print(f"Erro ao baixar ou salvar a imagem: {e}")
        return None
    
def gerar_artigos():
    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    os.makedirs("artigos", exist_ok=True)
    
    for nome_arquivo in os.listdir("transcricoes"):
        if nome_arquivo.endswith(".txt"):
            caminho_txt = os.path.join("transcricoes", nome_arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]

            with open(caminho_txt, "r", encoding="utf-8") as file:
                texto_base = file.read()

            # Prompt
            prompt = f"""
            
            Imagine que você é um profissional especializado na criação de artigos para blogs e sites, com foco em SEO, experiência do usuário e autoridade no conteúdo. Com base no conteúdo abaixo, escreva um artigo em HTML em português, estruturado conforme as melhores práticas editoriais e de marketing de conteúdo.

            Requisitos Gerais:
            O artigo deve conter entre 1000 e 2000 palavras.

            O texto deve ser original, profundo e informativo, agregando valor real ao leitor.

            Cabeçalho HTML:
            Adicione a tag:

            <meta name="category" content="...">
            Escolha o valor mais apropriado entre: filmes-e-series, jogos, curiosidades, musica, saude, tecnologia, com base no conteúdo.

            Inclua também:

            <meta name="description" content="Resumo atrativo do artigo com até 160 caracteres.">
            <title>Título chamativo do artigo</title>
            Estrutura do Artigo:
            Use títulos e subtítulos claros com <h2>, <h3> e <h4>.

            Organize o conteúdo em listas numeradas ou com marcadores quando necessário.

            Destaque pontos-chave em negrito para melhorar a leitura escaneável.

            Adicione comentários HTML descrevendo as imagens ideais para cada seção, no formato:

            <!-- imagem: descrição da imagem + categoria(filmes-e-series | jogos | curiosidades | musica | saude | tecnologia) -->
            Conteúdo:
            Escreva análises detalhadas sobre os itens ou temas discutidos.

            Explique por que cada ponto merece destaque, com base em critérios claros.

            Sempre que possível, cite fontes confiáveis para embasar suas afirmações.

            Elementos Visuais:
            Sugira o uso de imagens livres de direitos autorais (como Unsplash, Freepik, Pexels).

            Utilize infográficos, gráficos ou vídeos quando relevante (pode ser apenas a sugestão no comentário HTML).

            SEO e Experiência do Usuário:
            Use palavras-chave de forma natural ao longo do texto.

            Escreva uma meta descrição atrativa para aumentar o CTR.

            Mantenha o código e o conteúdo otimizados para carregamento rápido.

            Engajamento e Atualização:
            Inclua links internos fictícios apontando para artigos relacionados (ex: <a href="/artigo-relacionado">Leia também</a>).

            Encerre o artigo com um convite à interação: perguntas, comentários ou compartilhamentos.

            Garanta que o conteúdo tenha relevância duradoura e possa ser atualizado no futuro.

            Não Fazer:
            Não escreva conteúdo superficial ou genérico.

            Não use frases prontas que não entreguem valor real.

            Não gere um artigo curto ou puramente descritivo sem profundidade.

            Texto base:
            \"\"\"{texto_base}\"\"\"
            """

            print(f"📄 Gerando artigo para: {nome_arquivo}")
            response = model.generate_content(prompt)
            time.sleep(40)
            html_com_tags = response.text

            # Busca por comentários de imagens
            imagens = re.findall(r"<!-- imagem: (.*?) -->", html_com_tags)
            html_final = html_com_tags

            for i, descricao in enumerate(imagens):
                img_path = baixa_imagens_licenca_livre(descricao, nome_base, i)
                time.sleep(10)
                if img_path:
                    img_tag = f'<img src="{os.path.basename(img_path[0])}" alt="{descricao}" style="max-width:100%; border-radius:10px; margin: 20px 0;">'
                    html_final = html_final.replace(f"<!-- imagem: {descricao} -->", img_tag, 1)

            # Salva HTML final
            caminho_html = f"artigos/{nome_base}.html"
            with open(caminho_html, "w", encoding="utf-8") as f:
                f.write(html_final)

            print(f"✅ Artigo gerado: {caminho_html}")
            time.sleep(4)
