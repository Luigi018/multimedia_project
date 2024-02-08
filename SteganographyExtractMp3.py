from pydub import AudioSegment
import numpy as np

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

def extract_message_from_mp3(audio_file, bit_length, lsb_position=0):
    audio_segment = AudioSegment.from_mp3(audio_file)
    
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:  
        samples = samples[::2]  
    
    bits = ''.join(str(extract_bit(samples[i], lsb_position)) for i in range(bit_length))
    
    # Converti i bit estratti in testo
    message = bits_to_text(bits)
    return message

audio_file = 'jetengine1000(0).mp3'  # Percorso al tuo file MP3

bit_length = 8000  # Lunghezza messaggio in bit
lsb_position = 0  # Posizione bit estratto

message = extract_message_from_mp3(audio_file, bit_length, lsb_position)
print("Messaggio estratto:", message)
