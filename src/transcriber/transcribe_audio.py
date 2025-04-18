import os
import whisper

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base") 
        print(f"Transcrevendo: {audio_path}")
        result = model.transcribe(audio_path, fp16=False) 
        return result["text"]
    except Exception as e:
        print(f"Erro ao transcrever {audio_path}: {e}")
        return ""

def transcribe_all_audios(audio_folder="audios", output_folder="transcricoes"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(audio_folder):
        if filename.endswith(".mp3"):
            audio_path = os.path.join(audio_folder, filename)
            texto = transcribe_audio(audio_path)

            if texto:
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_folder, f"{base_name}.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(texto)
                print(f"Transcrição salva em: {output_path}")

