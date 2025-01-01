from phi.agent import Agent
from src.agents.llms import repo_llm
from src.tools.repo_tools import *

repo_crawler = Agent(
    model =repo_llm,
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
    debug_mode=True,
)


repo_summarizer = Agent(
    model = repo_llm,
    name = "repo_summarizer",
    tools=[get_file, explore_directory, get_repo_file_structure, save_summary],
    description="you are a senior developer and your job is to generate a detailed summary of the user's github repository",
    instructions=[
    "Your main goal is to generate a comprehensive summary of the assigned GitHub repository.",
    """
    Your summary should include:
    - Overall file structure of the repository
    - Files and directories at the root level
    - Entry points of the code (e.g., main files)
    - Important configuration files (e.g., .env, .gitignore, package.json)
    - A generalized description of directories and their contents
    """,
    "Always check the README file for insights about the repository's purpose and key features.",
    "Use the tools provided to explore and analyze the repository files and directories.",
    "If you cannot find specific information, log an error clearly instead of delegating the task elsewhere.",
    "Handle errors gracefully by providing a partial summary and stating what could not be determined.",
    "Return your final summary in a structured Markdown format.",
    "Avoid delegating tasks back to other agents unless explicitly instructed."
    ],
    markdown=True,
    show_tool_calls=True,
    add_chat_history_to_messages=True,
    add_datetime_to_instructions=True,
    debug_mode=True,
)