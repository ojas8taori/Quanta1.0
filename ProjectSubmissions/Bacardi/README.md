# Quantum Music Generator 🎵⚛️

A project that generates random musical melodies using quantum computing principles! Built with Qiskit for quantum circuit simulation and pydub for audio synthesis.


## Features ✨
- **Quantum Randomness**: Uses quantum superposition to generate true random bits
- **Visualization**: Real-time quantum circuit diagrams and measurement histograms
- **Audio Synthesis**: Converts quantum states to musical notes (C major scale)
- **Portable**: Generates standard WAV files for easy sharing

## Requirements 📋
- Python 3.8+
- Qiskit
- Matplotlib
- Pydub
- IPython
- FFmpeg

## How It Works 🔮
1. Creates 3-qubit quantum circuit with Hadamard gates

2. Measures qubits to get random bitstring (000-111)

3. Maps bit patterns to musical notes (C, D, E, F, G, A, B, C5)

4. Synthesizes melody using pure sine waves

5. Exports to WAV format


## Installation ⚙️
```bash
git clone https://github.com/samanvithkashyap/quantum-music-generator
cd quantum-music-generator
pip install -r requirements.txt
sudo apt-get install ffmpeg  # For Linux/macOS

