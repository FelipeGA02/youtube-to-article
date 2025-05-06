from dotenv import load_dotenv
import os
from downloader.download_video import download_youtube_videos
from downloader.extract_audio import extract_audio_from_video
from downloader.get_trending_videos import search_youtube_video_links
from generator import generate_article
from transcriber.transcribe_audio import transcribe_all_audios
from uploader.upload_article import publish_all_articles

if __name__ == "__main__":
    print("🔄 Carregando variáveis de ambiente...")
    load_dotenv()
    
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX_ID = os.getenv("SEARCH_ENGINE_ID")
    QUERY = "top ranking melhores site:youtube.com"
    MAX_RESULTS = 5

    print(f"🔍 Buscando vídeos no YouTube com a query: '{QUERY}'...")
    video_links = search_youtube_video_links(API_KEY, CX_ID, QUERY, MAX_RESULTS)
    
    if not video_links:
        print("⚠️ Nenhum vídeo encontrado.")
    else:
        print(f"📥 {len(video_links)} vídeo(s) encontrado(s). Iniciando o download...")
        download_youtube_videos(video_links)

        print("🎞️ Extraindo áudio dos vídeos baixados...")
        for file in os.listdir("videos"):
            if file.endswith((".mp4", ".mkv", ".webm")):
                video_path = os.path.join("videos", file)
                print(f"🔊 Extraindo áudio de: {file}")
                extract_audio_from_video(video_path)

        print("📝 Transcrevendo todos os áudios...")
        transcribe_all_audios()

        print("📰 Gerando artigos com base nas transcrições...")
        generate_article.gerar_artigos()

        print("🌐 Publicando artigos no site...")
        publish_all_articles()

    print("✅ Processo concluído com sucesso!")
