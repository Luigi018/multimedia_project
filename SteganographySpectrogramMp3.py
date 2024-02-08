import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from pydub import AudioSegment

def calculate_spectrogram_mp3(audio_file, title):
    audio_segment = AudioSegment.from_mp3(audio_file)
    
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:  
        samples = samples[::2] 
    
    framerate = audio_segment.frame_rate

    f, t, Sxx = spectrogram(samples, fs=framerate)

    plt.figure()
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='auto')
    plt.title(title)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequenza (Hz)')
    plt.colorbar(label='Potenza (dB)')
    plt.show()

audio_file_mp3 = 'jetengine500000(0).mp3' 

calculate_spectrogram_mp3(audio_file_mp3, 'Spettrogramma - Audio MP3')
