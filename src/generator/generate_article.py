import os
import re
import requests
import google.generativeai as genai
from dotenv import load_dotenv

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")

# Cria pastas se não existirem
os.makedirs("artigos", exist_ok=True)
 
# Função para gerar imagem usando a API gratuita do Unsplash
def gerar_imagem_gratis_unsplash(query, index, nome_base):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url).json()

    # Em caso de erro
    if "urls" not in response:
        print(f"⚠️ Erro ao buscar imagem: {response}")
        return ""

    image_url = response["urls"]["regular"]
    img_path = f"artigos/{nome_base}_imagem_{index}.jpg"
    img_data = requests.get(image_url).content
    with open(img_path, "wb") as handler:
        handler.write(img_data)

    return img_path

def gerar_artigos():
    for nome_arquivo in os.listdir("transcricoes"):
        if nome_arquivo.endswith(".txt"):
            caminho_txt = os.path.join("transcricoes", nome_arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]

            with open(caminho_txt, "r", encoding="utf-8") as file:
                texto_base = file.read()

            # Prompt
            prompt = f"""
            
            Com base no conteúdo abaixo, escreva um artigo em HTML em português, que inclua uma meta tag podendo ter o content de: filmes-e-series, jogos, curiosidades, musica, saude, tecnologia. Escolha o que fazer maior sentido para o conteúdo. Exemplo:
            <head>
                <meta name="category" content="tecnologia">
                <title>Exemplo de Artigo</title>
            </head>
            Para gerar o artigo foque nos seguites tópicos:
            
            ### 1. **Conteúdo Original e Profundo**

            - Escreva **análises detalhadas** para cada item do ranking, explicando por que ele ocupa aquela posição.
            - Inclua **fontes confiáveis** para embasar suas escolhas.

            ### 2. **Formato Estruturado e Escaneável**

            - Use **títulos e subtítulos claros (H2, H3, H4)** para facilitar a leitura.
            - Adicione **listas numeradas ou com marcadores** para organização.
            - Destaque **pontos-chave em negrito** para facilitar a leitura rápida.

            ### 3. **Mídia Visual de Qualidade**

            - Inclua **imagens originais** ou com licença de uso (Unsplash, Pexels, Freepik).
            - Adicione **infográficos ou tabelas** para tornar os dados mais atraentes.
            - Se possível, **incorpore vídeos** (próprios ou de fontes confiáveis).

            ### 4. **SEO e Experiência do Usuário**

            - Escreva **títulos chamativos e descritivos**.
            - Utilize palavras-chave de forma natural.
            - Crie **meta descrições** atrativas para cada artigo.
            - Melhore o tempo de carregamento do site.

            ### 5. **Engajamento e Autoridade**

            - Adicione **links internos** para outros artigos relevantes do seu blog.
            - Incentive comentários e interações.
            - Atualize rankings periodicamente para manter a relevância.

            ### 6. **Evite Conteúdo de Baixo Valor**

            - Evite textos superficiais ou automáticos.
            - Não crie artigos apenas para gerar cliques sem entregar valor real.
            
            Para cada seção, adicione um comentário HTML com uma descrição da imagem ideal para acompanhar essa parte, no formato:
            <!-- imagem: descrição da imagem -->

            Texto:
            \"\"\"{texto_base}\"\"\"
            """

            print(f"📄 Gerando artigo para: {nome_arquivo}")
            response = model.generate_content(prompt)
            html_com_tags = response.text

            # Busca por comentários de imagens
            imagens = re.findall(r"<!-- imagem: (.*?) -->", html_com_tags)
            html_final = html_com_tags

            for i, descricao in enumerate(imagens):
                img_path = gerar_imagem_gratis_unsplash(descricao, i, nome_base)
                if img_path:
                    img_tag = f'<img src="{os.path.basename(img_path)}" alt="{descricao}" style="max-width:100%; border-radius:10px; margin: 20px 0;">'
                    html_final = html_final.replace(f"<!-- imagem: {descricao} -->", img_tag, 1)

            # Salva HTML final
            caminho_html = f"artigos/{nome_base}.html"
            with open(caminho_html, "w", encoding="utf-8") as f:
                f.write(html_final)

            print(f"✅ Artigo gerado: {caminho_html}")
