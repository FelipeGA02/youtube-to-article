import requests
from urllib.parse import urlparse, parse_qs

def search_youtube_video_links(api_key, cx_id, query, max_results):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx_id,
        "q": query,
        "num": max_results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        links = [item["link"] for item in data.get("items", []) if "link" in item]
        return links

    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)
        return []

def normalize_youtube_link(link):
    """Extrai o ID do vídeo e retorna um link limpo."""
    parsed_url = urlparse(link)

    if "youtube.com" in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        video_id = query.get("v")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id[0]}"
    elif "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path.strip("/")
        return f"https://www.youtube.com/watch?v={video_id}"
    
    return None