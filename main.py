import data.prompt as prompt

import os
import json
from datetime import datetime

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from google import genai
from google.genai import types

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from sarvamai import SarvamAI



TTT_MODEL = "gemini-2.5-flash-preview-05-20"
TTT_CONFIG = types.GenerateContentConfig(
    temperature=0,
    thinking_config = types.ThinkingConfig(
        thinking_budget=0,
    ),
    response_mime_type="application/json",
)
gemini = genai.Client()



deepgram = DeepgramClient()
options = PrerecordedOptions(
        model="nova-3",
        smart_format=True,
    )



client = SarvamAI(api_subscription_key = os.environ['SARVAM_AI_API'])




app = FastAPI()

def sarvam_stt(file_path):
    with open(file_path, "rb") as audio_file:
        response = client.speech_to_text.translate(
            file=audio_file,
            model="saaras:v2"
        )
    
        return response.transcript

def stt(file_path):
    try:
        with open(file_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }
        
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        response = response.to_dict()['results']['channels'][0]['alternatives'][0]['transcript']
        return response

    except Exception as e:
        print(f"Exception: {e}")
        
def ttt(stt_response):
    contents = [types.Content(role="user", parts=[types.Part.from_text(text = prompt.instruction + stt_response)])]
    response = gemini.models.generate_content(
        model = TTT_MODEL,
        contents = contents,
        config = TTT_CONFIG,
    )
    response = json.loads(response.text)
    print(response['response'])
    if type(response['response']) == str:
        return response['response'], 'string'
    
    return response['response'], 'json'
           
           
           
@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
        contents = await file.read() 
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3] 
        file_path = f"data/outputs/{timestamp}.wav"
        with open(file_path, "wb") as f:
            f.write(contents)
            
        stt_response = sarvam_stt(file_path)
        ttt_response, response_type = ttt(stt_response)
        return {'response_type': response_type, 'response': ttt_response}
