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
│   │   └── generate_images.py
│   │
│   ├── 📁 uploader/              # Scripts para postar na Hostinger (via FTP, API, CMS)
│   │   └── upload_article.py
│   │
│   └── main.py                   # Orquestração do processo completo
│
├── 📁 articles/                  # Artigos gerados (HTML, Markdown ou outro formato)
│   └── artigo_001.md
│
├── 📁 images/                    # Imagens geradas por IA
│   └── artigo_001/
│       ├── img1.png
│       └── img2.png
│
├── 📁 audio/                     # Áudios extraídos dos vídeos
│   └── video_001.mp3
│
├── 📁 videos/                    # Vídeos baixados
│   └── video_001.mp4
│
├── 📁 logs/                      # Logs da execução e erros
│   └── execution.log
│
├── 📁 configs/                   # Arquivos de configuração (API keys, etc)
│   └── config.yaml
│
├── requirements.txt             # Dependências do projeto
├── .env                         # Variáveis de ambiente (API keys, tokens)
└── README.md                    # Documentação do projeto
