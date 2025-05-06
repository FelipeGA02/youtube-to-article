import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
import time

from generator.image_generator import buscar_imagens_licenca_livre, gerar_imagem_por_ia_huggingface, mesclar_imagens

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

os.makedirs("artigos", exist_ok=True)

def gerar_query_visual(descricao, contexto):
    prompt_query = f"""
    Você é um especialista em busca de imagens para ilustrar artigos. Com base na descrição abaixo, no contexto geral do artigo e na categoria, gere uma *query* concisa, específica e visualmente expressiva para ser usada na API do Unsplash.

    Descrição: "{descricao}"
    Contexto do artigo: "{contexto}"
    Categoria: "(filmes-e-series | jogos | curiosidades | musica | saude | tecnologia)"
    """
    response = model.generate_content(prompt_query)
    time.sleep(30)
    return response.text.strip().replace('"', '')

def gerar_artigos():
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
            html_com_tags = response.text

            # Busca por comentários de imagens
            imagens = re.findall(r"<!-- imagem: (.*?) -->", html_com_tags)
            html_final = html_com_tags

            for i, descricao in enumerate(imagens):
                query_visual = gerar_query_visual(descricao, texto_base)
                path_ia = gerar_imagem_por_ia_huggingface(query_visual, f"{nome_base}_{i}")
                time.sleep(10)
                imagens_livres = buscar_imagens_licenca_livre(descricao)
                time.sleep(10)
                img_path = mesclar_imagens(path_ia, imagens_livres)
                time.sleep(2)
                if img_path:
                    img_tag = f'<img src="{os.path.basename(img_path)}" alt="{descricao}" style="max-width:100%; border-radius:10px; margin: 20px 0;">'
                    html_final = html_final.replace(f"<!-- imagem: {descricao} -->", img_tag, 1)

            # Salva HTML final
            caminho_html = f"artigos/{nome_base}.html"
            with open(caminho_html, "w", encoding="utf-8") as f:
                f.write(html_final)

            print(f"✅ Artigo gerado: {caminho_html}")
            time.sleep(4)
