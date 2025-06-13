import requests

url = 'http://127.0.0.1:8000/upload-audio/'
with open('/Users/outbell/Ajay/DeepLearning/GenAI/treeya/2024-12-19-19:29.mp3', 'rb') as file:
    files = {'file' : file, 'filename' : '2024-12-19-18:29.mp3'}
    requests.post(url, files = files)