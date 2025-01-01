from phi.model.google import Gemini
import os
from dotenv import load_dotenv
load_dotenv()

repo_llm =  Gemini(
        id='gemini-1.5-flash',
        api_key=os.environ['api']
    )

coder_llm = Gemini(
        api_key=os.environ['api']
    )
