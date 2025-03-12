from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram, circuit_drawer
import matplotlib.pyplot as plt

from pydub.utils import which
from pydub import AudioSegment

AudioSegment.converter = which("ffmpeg")

#creating a quantum circut with 3 qubits, and a hamadad gate which puts a qubit into superposition
#and then measures the value which colapses the superposition and returns the value

def get_random_bits(num_bits=3):
    qc = QuantumCircuit(num_bits, num_bits)
    qc.h(range(num_bits))
    qc.measure(range(num_bits), range(num_bits))
    
    backend = Aer.get_backend("aer_simulator")
    qc = transpile(qc, backend)
    job = backend.run(qc, shots=1)
    result = job.result()
    
    counts = result.get_counts()
    bitstring = list(counts.keys())[0]
    
    print(f"Generated Bitstring: {bitstring}")
    display(qc.draw("mpl"))
    
    plot_histogram(counts)
    plt.show()
    
    return bitstring


# Mapping 3-bit strings to notes
bit_to_note = {
    '000': 'C',
    '001': 'D',
    '010': 'E',
    '011': 'F',
    '100': 'G',
    '101': 'A',
    '110': 'B',
    '111': 'C5'
}

def generate_melody(length=8):
    melody = []
    for _ in range(length):
        bits = get_random_bits()
        note = bit_to_note.get(bits)
        melody.append(note)
    return melody

melody = generate_melody()
print("Generated Melody:", melody)

from pydub.generators import Sine
from pydub import AudioSegment
from IPython.display import Audio


# Frequencies of C major notes
note_freq = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
    'C5': 523.25
}

# generation of the audio by mapping the notes got from the quantum computer to actual-
# frequency values for us to convert it into an audio file
def melody_to_audio(melody, duration_ms=500):
    song = AudioSegment.silent(duration=0)
    for note in melody:
        freq = note_freq.get(note, 261.63)
        tone = Sine(freq).to_audio_segment(duration=duration_ms)
        song += tone
    return song
#converting to audio
melody_audio = melody_to_audio(melody)
melody_audio.export("quantum_melody.wav", format="wav")

Audio("quantum_melody.wav")