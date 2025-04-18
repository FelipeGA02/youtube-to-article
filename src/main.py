from dotenv import load_dotenv
import os
from downloader.download_video import download_youtube_videos
from downloader.get_trending_videos import search_youtube_video_links

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CX_ID = os.getenv("SEARCH_ENGINE_ID")
QUERY = "top ranking melhores site:youtube.com"
MAX_RESULTS = 5

if __name__ == "__main__":
    if not API_KEY or not CX_ID:
        print("❌ API_KEY ou SEARCH_ENGINE_ID não definidos no .env.")
    else:
        video_links = search_youtube_video_links(API_KEY, CX_ID, QUERY, MAX_RESULTS)
        if not video_links:
            print("⚠️ Nenhum vídeo encontrado.")
        else:
            download_youtube_videos(video_links)