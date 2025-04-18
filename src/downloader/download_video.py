import yt_dlp

def download_youtube_videos(links, output_path="videos"):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [],
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in links:
            try:
                print(f"Baixando: {url}")
                ydl.download([url])
                print("✔️ Download concluído!\n")
            except Exception as e:
                print(f"Erro ao baixar {url}: {e}")
