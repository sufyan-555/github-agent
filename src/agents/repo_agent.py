from phi.agent import Agent
from phi.model.google import Gemini
import os
from src.tools.repo_tools import *
from dotenv import load_dotenv
load_dotenv()

repo_agent = Agent(
    model = Gemini(
        api_key=os.environ['api']
    ),
    tools=[get_file, explore_directory, get_repo_file_structure],
    description="you are an Ai assistant that can help users with their github repositories",
    instructions=[
        "your mail goal is to help users with their github repositories",
        "If you are unsure about the path of something, try looking into the file structure of the repository and if that doesnot help then ask the user for help",
        "if you encounter an error, try to handle it gracefully, and if not possible then ask the user for help",
        "if you were to find some specifc portions of the code then try to look at most probable places first before asking the user for help",
        "you can use tools to achieve your goal"
    ],
    markdown=True,
    show_tool_calls=True,
    add_chat_history_to_messages=True,
    add_datetime_to_instructions=True,
    # debug_mode=True,
)
