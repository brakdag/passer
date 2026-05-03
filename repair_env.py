import subprocess
import sys

DEPENDENCIES = [
    "google-genai",
    "rich",
    "prompt_toolkit",
    "yaspin",
    "paho-mqtt",
    "wasmer",
    "Pillow",
    "requests",
    "pydantic",
    "black",
    "pynput",
    "sounddevice",
    "numpy",
    "gTTS",
    "jedi",
    "onnxruntime",
    "opencv-python",
    "pygame",
    "mss",
    "DrissionPage",
]

def repair():
    print("Starting environment repair...")
    for dep in DEPENDENCIES:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {dep}: {e}")
    print("Environment repair complete.")

if __name__ == '__main__':
    repair()