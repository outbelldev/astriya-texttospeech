from dataclasses import dataclass

from google.genai import types

import data.prompt as prompt 


@dataclass
class TTT:
    model = "gemini-2.5-flash"
    config = types.GenerateContentConfig(
        temperature = 1,
        thinking_config = types.ThinkingConfig(thinking_budget = 0),
        response_mime_type = "application/json",
        system_instruction = [types.Part.from_text(text = prompt.instruction)]
    )
    
    
    
ttt = TTT()