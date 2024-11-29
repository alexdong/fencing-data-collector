from datetime import datetime
from pathlib import Path
import sys
import subprocess

from utils import get_char_timeout
from voice_recognition import record_audio, save_wav, transcribe_audio


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "rb") as audio_file:
            transcript = transcribe_audio(audio_file)
            subprocess.run("pbcopy", text=True, input=transcript)
        print(f"\n[INFO] 📝 Transcript:\n✨ {transcript}")
        print("\n[INFO] 📋 Copied to clipboard! 🎉")
        return

    print("[INFO] 🎯 Welcome to Fencing Bout Logger!")
    print(
        "[INFO] Commands: Press `s` to record, press Enter when there is a point scored. Press 'q' to quit."
    )

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
                    print("\n[INFO] 🔄 Press 's' to start or 'q' to quit")


if __name__ == "__main__":
    main()
