import wave
import numpy as np
from pydub import AudioSegment

def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def modify_bit(audio_data, bit_position, bit):
    if bit_position < 0 or bit_position > 15:
        raise ValueError("Posizione del bit non valida. Deve essere compresa tra 0 e 15.")
    mask = 1 << bit_position
    if bit == 0:
        audio_data &= ~mask
    elif bit == 1:
        audio_data |= mask
    else:
        raise ValueError("Il bit deve essere 0 o 1.")
    return audio_data

def hide_message(audio_file, message_file, output_file, bit_position=0):
    with open(message_file, 'r') as f:
        message = f.read()
    bits = text_to_bits(message)
    
    with wave.open(audio_file, 'rb') as wav:
        framerate = wav.getframerate()
        nframes = wav.getnframes()
        channels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        audio_format = np.int16 if sampwidth == 2 else np.int8
        audio_data = np.frombuffer(wav.readframes(nframes), dtype=audio_format).copy()
        
    if len(bits) > len(audio_data) * 16:
        raise ValueError("Il messaggio è troppo lungo per essere nascosto nell'audio.")
    
    for i, bit in enumerate(bits):
        audio_data[i] = modify_bit(audio_data[i], bit_position, int(bit))
    
    with wave.open(output_file, 'w') as out_wav:
        out_wav.setparams((channels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))
        out_wav.writeframes(audio_data.tobytes())

    compress_audio(output_file, output_file.replace('.wav', '.mp3'))

def compress_audio(input_file, output_file):
    sound = AudioSegment.from_wav(input_file)
    sound.export(output_file, format="mp3", bitrate="128k")

audio_file = 'orchestra.wav'
message_file = '500000.txt'
output_file = 'jetengine500000(0).wav'
bit_position = 0

hide_message(audio_file, message_file, output_file, bit_position)
