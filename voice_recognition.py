#!/usr/bin/env python3

import os
import sys
import wave
import pyaudio
import openai
import select
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, BinaryIO
from utils import get_char_timeout

# Initialize OpenAI
assert (
    "OPENAI_API_KEY" in os.environ
), "❌ OPENAI_API_KEY environment variable is not set"

# Audio recording constants optimized for speech
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Optimal for speech recognition
CHUNK = 1024
MAX_DURATION = 780  # 13 minutes (with safety margin)
WARNING_TIME = 30  # Warn when 30 seconds left


def record_audio() -> List[bytes]:
    """Records audio until Enter is pressed. Returns raw audio frames."""
    print("[INFO] 🎤 Recording... (Press Enter to stop)")

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    frames: List[bytes] = []
    start_time = datetime.now()
    warning_shown = False

    while True:
        current_elapsed = int((datetime.now() - start_time).total_seconds())
        remaining = MAX_DURATION - current_elapsed

        # Show warning when 30 seconds left
        if remaining <= WARNING_TIME and not warning_shown:
            print(f"\n[WARN] ⚠️  {WARNING_TIME} seconds left!")
            warning_shown = True

        # Force stop at max duration
        if current_elapsed >= MAX_DURATION:
            print("\n[INFO] ⏰ Maximum recording duration reached")
            break

        sys.stdout.write(
            f"\r⏱️  Recording time: {current_elapsed}s (max {MAX_DURATION}s)   "
        )
        sys.stdout.flush()

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            if input() == "":
                break
        frames.append(stream.read(CHUNK))

    print("\n")  # Move to next line after recording stops
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return frames


def save_wav(frames: List[bytes], output_path: Path) -> None:
    """Saves audio frames to WAV file."""
    print(f"[INFO] 💾 Saving audio to {output_path}")

    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(AUDIO_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))


def transcribe_audio(audio_file: BinaryIO) -> str:
    """Transcribes audio file using OpenAI Whisper API."""
    print("[INFO] 🔄 Transcribing audio...")

    client = openai.OpenAI()
    result = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    assert hasattr(result, "text"), "No transcription text in API response"

    return result.text


if __name__ == "__main__":
    main()
