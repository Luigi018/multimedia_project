import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

def calculate_spectrogram(audio_file, title):
    with wave.open(audio_file, 'rb') as wav:
        framerate = wav.getframerate()
        audio_data = wav.readframes(-1)
        audio_data = np.frombuffer(audio_data, dtype=np.int16)

    f, t, Sxx = spectrogram(audio_data, fs=framerate)

    plt.figure()
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='auto')
    plt.title(title)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequenza (Hz)')
    plt.colorbar(label='Potenza (dB)')
    plt.show()

audio_file1 = 'orchestra.wav'

calculate_spectrogram(audio_file1, 'Spettrogramma - Audio 1')

