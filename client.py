import pyaudio
import wave
import requests

azuer_server_url = "https://tstapispeech-dnhxfah2d2fzbnf8.southeastasia-01.azurewebsites.net/upload-audio/"
tunnel_url = "https://9f3180f804e3.ngrok-free.app/upload-audio/"
local_url = 'http://localhost:8000/upload-audio/'

def record_and_send(filename="output.wav", seconds = 3.5, api_url = local_url):
    # Record audio
    chunk = 1024
    fmt = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=fmt, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    print("Recording...")
    frames = [stream.read(chunk) for _ in range(0, int(rate / chunk * seconds))]
    print("Done recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(fmt))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    with open(filename, 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files = files, data = {'user_id' : '001'})
        
    '''s = "green pattani"
    response = requests.post(api_url, data = {'text' : 1, 'user_id' : '001'})
    print("Server response:", response.text)'''

# Example usage:
record_and_send()

