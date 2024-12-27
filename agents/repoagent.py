from phi.agent import Agent
from phi.model.google import Gemini
import os
from dotenv import load_dotenv
load_dotenv()
from tools.repotools import *

repo_agent = Agent(
    model = Gemini(
        api_key=os.environ['api']
    ),
    tools=[get_file, explore_directory, get_repo_file_structure],
    description="you are an Ai assistant that can help users with their github repositories",
    instructions=[
        "your mail goal is to help users with their github repositories",
        "you can use tools to achieve your goal"
    ],
    markdown=True,
    show_tool_calls=True,
    add_chat_history_to_messages=True,
    add_datetime_to_instructions=True,
    # debug_mode=True,
)
