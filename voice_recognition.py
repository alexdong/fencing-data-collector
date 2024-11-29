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


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "rb") as audio_file:
            transcript = transcribe_audio(audio_file)
            subprocess.run("pbcopy", text=True, input=transcript)
        print(f"\n[INFO] 📝 Transcript:\n✨ {transcript}")
        print("\n[INFO] 📋 Copied to clipboard! 🎉")
        return

    print("[INFO] 🎯 Welcome to Whisper Audio Recorder!")
    print("[INFO] Commands: 's' to start, 'q' to quit, Enter to stop recording")

    while True:
        sys.stdout.write("\r🎮 ")
        sys.stdout.flush()
        cmd = get_char_timeout(3600 * 24 * 7)  # 1 week timeout
        if cmd:
            print(cmd)  # Echo the character back
            match cmd.lower():
                case "q":
                    print("\n[INFO] 👋 Goodbye!")
                    break

                case "s":
                    temp_path = Path(
                        f"/tmp/whisper_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                    )

                    # Record and save audio
                    frames = record_audio()
                    save_wav(frames, temp_path)

                    # Transcribe and copy to clipboard
                    with open(temp_path, "rb") as audio_file:
                        transcript = transcribe_audio(audio_file)
                        subprocess.run("pbcopy", text=True, input=transcript)

                    print(f"\n[INFO] 📝 Transcript:\n✨ {transcript}")
                    print("\n[INFO] 📋 Copied to clipboard! 🎉")
                    print("\n[INFO] 🔄 Press 's' for new recording or 'q' to quit")


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
