from moviepy import VideoFileClip
import os

def extract_audio_from_video(video_path, output_dir="audios"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        filename = os.path.basename(video_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{name_without_ext}.mp3")

        print(f"Extraindo áudio de: {video_path}")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_path)

        print(f"Áudio salvo em: {output_path}")
        return output_path

    except Exception as e:
        print(f"Erro ao extrair áudio de {video_path}: {e}")
        return None

