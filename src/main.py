from dotenv import load_dotenv
import os
from downloader.download_video import download_youtube_videos
from downloader.extract_audio import extract_audio_from_video
from downloader.get_trending_videos import search_youtube_video_links
from generator import generate_article
from transcriber.transcribe_audio import transcribe_all_audios

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CX_ID = os.getenv("SEARCH_ENGINE_ID")
QUERY = "top ranking melhores site:youtube.com"
MAX_RESULTS = 5
video_folder = "videos"

if __name__ == "__main__":
    
    #if not API_KEY or not CX_ID:
    #    print("❌ API_KEY ou SEARCH_ENGINE_ID não definidos no .env.")
    #else:
    #    video_links = search_youtube_video_links(API_KEY, CX_ID, QUERY, MAX_RESULTS)
    #    if not video_links:
    #        print("⚠️ Nenhum vídeo encontrado.")
    #    else:
    #        download_youtube_videos(video_links)
            
    #for file in os.listdir(video_folder):
    #    if file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".webm"):
    #        video_path = os.path.join(video_folder, file)
    #        extract_audio_from_video(video_path)
    
    #transcribe_all_audios()
    
    with open("transcriptions/transcricao.txt", "r", encoding="utf-8") as f:
        transcription = f.read()

    title = "Resumo do Vídeo"
    article = generate_article(transcription, title)

    # (opcional) adicionar imagens
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
    article_with_images = generate_article.insert_images_into_article(article, image_urls)

    md, html, pdf = generate_article.export_article(title, article_with_images)

    print(f"Artigo salvo como:\n- Markdown: {md}\n- HTML: {html}\n- PDF: {pdf}")