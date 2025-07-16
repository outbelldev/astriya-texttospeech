import data.prompt as prompt
import data.config as config
import os
import json
from datetime import datetime
import logging
#from pydub import AudioSegment

from fastapi import FastAPI, File, UploadFile
from typing import Optional
from fastapi import Form
import uvicorn

from google import genai
from sarvamai import SarvamAI



gemini = genai.Client()
stt_client = SarvamAI(api_subscription_key = os.environ['SARVAM_AI_API'])
app = FastAPI()

database_pdf = gemini.files.upload(file = "data/treeya_items.pdf")
users_in_process = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


def stt(file_path):
    with open(file_path, "rb") as audio_file:
        response = stt_client.speech_to_text.transcribe(
            file = audio_file,
            model = "saarika:v2.5",
            language_code = 'en-IN'
        )
        '''response = stt_client.speech_to_text.translate(
            file = audio_file,
            model = "saaras:v2.5"
        )'''
        return response.transcript

        
def ttt(user_id, audio_path = None, user_text = None):
    user_id_in_process = user_id in users_in_process.keys()
    
    if audio_path:
        user_audio = gemini.files.upload(file = audio_path)
        contents = [user_audio, database_pdf]
    
    if user_text:
        contents = [user_text, database_pdf]
        
    if user_id_in_process:
        print(f"For user: ", user_id, " previous response is in process.", "\n\n")
        contents = [users_in_process[user_id]] +  contents
        
    response = gemini.models.generate_content(
        model = config.ttt.model,
        contents = contents,
        config = config.ttt.config,
    )
    response = json.loads(response.text)
    print("AI:\n", response, "\n\n")
    logger.info(response)
    
    if response['status'] == "in_process":
        print(f"For user: ", user_id, " current response is in process.")
        users_in_process[user_id] = users_in_process.get(user_id, '') + "User: " + response['user_query'] + "\n" + "AI: " + response['data'] + "\n\n"
        
    elif response['status'] == "success":
        if user_id in users_in_process.keys():
            del users_in_process[user_id]
            
    elif response['status'] == 'failure':
        return response
            
    return response
           
           
           
@app.post("/upload-audio/")
async def upload_audio(file: Optional[UploadFile] = File(None),
                       text: Optional[str] = Form(None),
                       user_id: str = Form(...)):

        logger.info('function hit')
    
        if file:
            contents = await file.read()                          #ogg_version = AudioSegment.from_ogg("never_gonna_give_you_up.ogg")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3] 
            file_path = f"data/outputs/{timestamp}.wav"
            
            with open(file_path, "wb") as f:
                f.write(contents)
                
            ttt_response = ttt(user_id = user_id, audio_path = file_path)
            
        elif text:
            ttt_response = ttt(user_id = user_id, user_text = text)
            
        else:
            return json.dumps({'status' : 'failed', 'response': 'Invalid input format. No audio file or text provided.'})
        
        return json.dumps(ttt_response)
    
if __name__ == '__main__':
    uvicorn.run("main:app", host = "localhost", port = 8000)
