import speech_recognition as sr


def transcrever_audio(audio_file_path: str) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="pt-BR")
            return texto
    except sr.UnknownValueError:
        return "Não foi possível transcrever o áudio."
    except sr.RequestError as e:
        return f"Erro ao solicitar transcrição: {e}"
