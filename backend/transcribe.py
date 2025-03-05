import whisper
from config import WHISPER_MODEL

def transcribe_audio(file_path):
  try:
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(file_path, fp16=False)  # Force FP32 for CPU
    return result['text'], result['segments']
  except Exception as e:
    raise Exception(f"Transcription failed: {str(e)}")