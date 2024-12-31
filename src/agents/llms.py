from phi.model.google import Gemini
import os
from dotenv import load_dotenv
load_dotenv()

repo_llm =  Gemini(
        id='gemini-1.5-flash',
        api_key=os.environ['api']
    )

coder_llm = Gemini(
        id='gemini-2.0-flash-thinking-exp-1219',
        api_key=os.environ['api']
    )
