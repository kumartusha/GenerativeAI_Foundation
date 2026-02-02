import openai
import sounddevice as sd
import numpy as np
import tempfile
import wave
import os

# Load API key from environment
# openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # replace with your actual key
# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# if openai.api_key is None:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

fs = 16000
chunk_duration = 5  # seconds

print("🎤 Speak now (Ctrl+C to stop)")

def save_wav(filename, audio_data, fs=16000):
    audio_data = np.asarray(audio_data, dtype=np.int16)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())

try:
    while True:
        # Record audio
        audio_chunk = sd.rec(int(chunk_duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        # Save properly as WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            save_wav(f.name, audio_chunk, fs)
            temp_filename = f.name

        # Send to Whisper API
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=open(temp_filename, "rb")
        )

        print("📝", transcript.text)

        # Delete temp file
        os.remove(temp_filename)

except KeyboardInterrupt:
    print("\n🛑 Stopped")