import wave
import numpy as np
import time

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
    start_time = time.time()
    print("File testo: " + message_file)
    with open(message_file, 'r') as f:
        message = f.read()
    bits = text_to_bits(message)
    print("Testo trasformato in bit")
    with wave.open(audio_file, 'rb') as wav:
        print("File audio: " + audio_file)
        framerate = wav.getframerate()
        nframes = wav.getnframes()
        channels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        audio_format = np.int16 if sampwidth == 2 else np.int8
        print("Creato l'array np.int16")
        audio_data = np.frombuffer(wav.readframes(nframes), dtype=audio_format).copy() 

    if len(bits) > len(audio_data) * 16:  
        raise ValueError("Il messaggio è troppo lungo per essere nascosto nell'audio.")
    
    for i, bit in enumerate(bits):
        audio_data[i] = modify_bit(audio_data[i], bit_position, int(bit))
    print("Audio modificato")
    with wave.open(output_file, 'w') as out_wav:
        out_wav.setparams((channels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))
        out_wav.writeframes(audio_data.tobytes())
    print("Audio salvato con il nome: " + output_file)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Tempo di esecuzione: {elapsed_time} secondi")

audio_file = 'orchestra.wav'  # File audio di input
message_file = 'prova.txt'  # File contenente il messaggio da nascondere
output_file = 'orchestraprova.wav'  # File audio di output
bit_position = 15  # Livello di bit dove inserire il messaggio

hide_message(audio_file, message_file, output_file, bit_position)
