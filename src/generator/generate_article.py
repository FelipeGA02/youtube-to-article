from transformers import pipeline
import markdown
from weasyprint import HTML
from diffusers import StableDiffusionPipeline
import openai
import os
import requests
from pathlib import Path
from textwrap import wrap

def generate_article(transcription_text: str, title: str = "Artigo Gerado") -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    summary_chunks = summarizer(transcription_text, max_length=300, min_length=100, do_sample=False)
    summary = " ".join([chunk['summary_text'] for chunk in summary_chunks])

    article = f"# {title}\n\n{summary}\n"
    return article

def insert_images_into_article(article: str, image_urls: list) -> str:
    content = article + "\n\n## Imagens Relacionadas:\n"
    for url in image_urls:
        content += f"![Imagem relacionada]({url})\n\n"
    return content

openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar imagem a partir de um prompt
def gerar_imagem(prompt, index):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    image_path = f"imagem_{index}.png"

    # Baixar imagem
    img_data = requests.get(image_url).content
    with open(image_path, 'wb') as f:
        f.write(img_data)

    return image_path

# Função para gerar HTML com imagens e texto
def gerar_html_com_imagens(texto_transcrito, output_path="artigo_gerado.html"):
    partes = wrap(texto_transcrito, width=300)  # divide o texto em blocos
    html = "<html><head><meta charset='UTF-8'><title>Artigo com Imagens</title></head><body>"

    for i, parte in enumerate(partes):
        html += f"<p>{parte}</p>"
        imagem = gerar_imagem(parte, i)
        html += f"<img src='{imagem}' alt='Imagem gerada para parte {i}' style='width: 300px;'><hr>"

    html += "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Artigo gerado com sucesso em {output_path}")

def export_article(title: str, article_markdown: str, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Salvar como Markdown
    md_path = os.path.join(output_dir, f"{title}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(article_markdown)

    # Converter e salvar como HTML
    html_content = markdown.markdown(article_markdown)
    html_path = os.path.join(output_dir, f"{title}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Converter HTML para PDF
    pdf_path = os.path.join(output_dir, f"{title}.pdf")
    HTML(string=html_content).write_pdf(pdf_path)

    return md_path, html_path, pdf_path