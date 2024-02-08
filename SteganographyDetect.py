import wave
import numpy as np

def load_audio(file_path):
    audio = wave.open(file_path, 'rb')
    frames = audio.readframes(-1)
    signal = np.frombuffer(frames, dtype=np.int16)
    return audio, signal

def detect_audio_steganography(file_path):
    print("Audio usato: " + file_path)
    audio, signal = load_audio(file_path)
    diff = np.diff(signal)
    threshold = np.max(np.abs(diff)) / 2
    print("Calcolo il threshold medio ", threshold)
    suspicious_samples = np.sum(np.abs(diff) > threshold)
    print("Calcolo il numero di campioni sospetti pari a ", suspicious_samples)
    detection_threshold = 0.035 
    print("Calcolo usando la soglia scelta dal programmatore:",detection_threshold * len(signal))
    if suspicious_samples > detection_threshold * len(signal):
        print("Sospetta presenza di steganografia nell'audio.")
    else:
        print("Nessuna steganografia rilevata nell'audio.")

    audio.close()

if __name__ == "__main__":
    audio_file = "jetengine1000(12).wav"
    detect_audio_steganography(audio_file)
