from phi.agent import Agent
from phi.model.google import Gemini
import os
from src.tools.repo_tools import *
from dotenv import load_dotenv
load_dotenv()

repo_crawler = Agent(
    model = Gemini(
        api_key=os.environ['api']
    ),
    name = "repo_crawler",
    tools=[get_file, explore_directory, get_repo_file_structure, get_repo_summary],
    description="you are a senior developer and your job is to help users with finding things in their github repositories",
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


repo_summarizer = Agent(
    model = Gemini(
        api_key=os.environ['api']
    ),
    name = "repo_summarizer",
    tools=[get_file, explore_directory, get_repo_file_structure, save_summary],
    description="you are a senior developer and your job is to generate a detailed summary of the user's github repository",
    instructions=[
        "your mail goal is to generate the summary of the github repositories",
        """
        Your Summary should include the follwing things:
        - Overall file structure of the repository
        - Files and directories at the root level
        - Entry points of the code (e.g., main files)
        - Any important configuration files
        - A genralized summary of the directories and files about thir content
        """,
        "make sure that you go through the readme file of the repository to get a better understanding of the repository",
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