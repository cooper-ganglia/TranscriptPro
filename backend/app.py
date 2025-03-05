from fastapi import FastAPI, UploadFile, HTTPException
from transcribe import transcribe_audio
import shutil
import os
import ffmpeg
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ProTranscript API")

# Add CORS middleware to allow local testing
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post('/transcribe')
async def transcribe(file: UploadFile):
  start_time = time.time()
  logger.info(f"Starting transcription for file: {file.filename}")
  try:
    # Save the uploaded file temporarily with its original extension or default to .bin
    temp_path = f"temp_input.{file.filename.split('.')[-1] if '.' in file.filename else 'bin'}"
    with open(temp_path, 'wb') as buffer:
      shutil.copyfileobj(file.file, buffer)

    # Extract audio from video or handle audio file using FFmpeg
    audio_path = "temp.wav"
    try:
      # Try to probe the input file to determine its type
      probe = ffmpeg.probe(temp_path, select_streams='a')  # Focus on audio streams
      if 'streams' in probe and any(stream['codec_type'] == 'audio' for stream in probe['streams']):
        # If it's an audio file, convert directly to WAV
        ffmpeg.input(temp_path, threads=0).output(
          audio_path, ac=1, ar=16000, format='wav', loglevel='quiet'
        ).run(overwrite_output=True)
      else:
        # If it's a video or no audio streams, extract audio
        ffmpeg.input(temp_path, threads=0).output(
          audio_path, ac=1, ar=16000, format='wav', loglevel='quiet'
        ).run(overwrite_output=True)
    except ffmpeg.Error as e:
      # Try to handle the file as raw data if probe fails
      try:
        with open(temp_path, 'rb') as f:
          data = f.read()
        # Create a simple WAV file if possible (minimal WAV header + data)
        with open(audio_path, 'wb') as out:
          out.write(b'RIFF\x00\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\xbb\x00\x00\x00\xfa\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00' + data[:10000])  # Truncate to 10KB for testing
        # Retry transcription with the new WAV
        text, segments = transcribe_audio(audio_path)
        logger.info(f"Processed file {file.filename} with fallback WAV creation in {time.time() - start_time:.2f} seconds")
        return {"text": text, "segments": segments}
      except Exception as e2:
        raise HTTPException(status_code=400, detail=f"FFmpeg and fallback failed to process audio: {str(e2)}")

    # Transcribe the audio
    text, segments = transcribe_audio(audio_path)
    logger.info(f"Processed file {file.filename} in {time.time() - start_time:.2f} seconds")
    return {"text": text, "segments": segments}
  except Exception as e:
    logger.error(f"Error processing file {file.filename}: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
  finally:
    # Clean up temporary files
    for temp_file in [temp_path, audio_path]:
      if os.path.exists(temp_file):
        try:
          os.remove(temp_file)
        except Exception as e:
          logger.warning(f"Could not remove {temp_file}: {e}")