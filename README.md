# BigBlogsBrasil

## Estrutura de Pastas

youtube-to-article/
│
├── 📁 src/                        # Código-fonte principal
│   ├── 📁 downloader/            # Scripts para baixar vídeos e áudios do YouTube
│   │   └── download_video.py
│   │
│   ├── 📁 transcriber/           # Scripts de transcrição (ex: Whisper, Vosk)
│   │   └── transcribe_audio.py
│   │
│   ├── 📁 generator/             # Geração de artigos e prompts
│   │   ├── generate_article.py
│   │
│   ├── 📁 uploader/              # Scripts para postar na Hostinger (via FTP, API, CMS)
│   │   └── upload_article.py
│   │
│   └── main.py                   # Orquestração do processo completo
│
├── 📁 artigos/                  # Artigos gerados (HTML, Markdown ou outro formato)
│   └── artigo_001.md
│
├── 📁 audios/                     # Áudios extraídos dos vídeos
│   └── video_001.mp3
│
├── 📁 transcricoes/                    # transcrições baixados
│   └── texto_001.txt
│
├── 📁 videos/                    # Vídeos baixados
│   └── video_001.mp4
│
├── requirements.txt             # Dependências do projeto
├── .env                         # Variáveis de ambiente (API keys, tokens)
└── README.md                    # Documentação do projeto
