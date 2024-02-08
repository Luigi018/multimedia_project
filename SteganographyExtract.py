import wave
import numpy as np
import time

def bits_to_text(bits):
    n = int(bits, 2)
    byte_sequence = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    try:
        return byte_sequence.decode('utf-8')
    except UnicodeDecodeError:
        return byte_sequence.decode('utf-8', errors='ignore')

def extract_bit(sample, bit_position):
    if bit_position < 0 or bit_position > 15:
        raise ValueError("Posizione del bit non valida. Deve essere compresa tra 0 e 15.")

    mask = 1 << bit_position
    extracted_bit = (sample & mask) >> bit_position
    return extracted_bit

def extract_message(audio_file, bit_length, lsb_position=0):
    start_time = time.time()

    with wave.open(audio_file, 'rb') as wav:
        print("Apertura file: " + audio_file)
        nframes = wav.getnframes()
        sampwidth = wav.getsampwidth()
        audio_format = np.int16 if sampwidth == 2 else np.int8
        audio_data = np.frombuffer(wav.readframes(nframes), dtype=audio_format)
        print("Creazione array np.int16")
    
    bits = ''.join(str(extract_bit(audio_data[i], lsb_position)) for i in range(bit_length))
    print("Messaggio trovato in bit")
    message = bits_to_text(bits)
    print("Messaggio trasformato in testo")
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Tempo di esecuzione: {elapsed_time} secondi")
    return message

audio_file = 'orchestraprova.wav'  

bit_length = 8000  # Lunghezza file in bit
lsb_position = 15  # Posizione del bit da estrarre

message = extract_message(audio_file, bit_length, lsb_position)
print("Messaggio estratto:", message)
