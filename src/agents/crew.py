from phi.agent import Agent
from phi.model.google import Gemini
import os
from src.agents.repo_agents import *
from dotenv import load_dotenv
load_dotenv()

crew=Agent(
        model = Gemini(
        api_key=os.environ['api']
    ),
    name = "crew",
    team=[repo_summarizer,repo_crawler],
    description="You are a senior developer overseeing a team of agents, ensuring tasks are efficiently delegated and completed related to GitHub repositories.",
    instructions=[
        "You are responsible for collaborating with the agents to help users with their GitHub repositories.",
        "Make sure to provide clear instructions when delegating tasks to ensure each agent understands the goal.",
        "Monitor each agent's progress and ensure the task is completed accurately and on time.",
        "If an agent encounters any errors or needs clarification, either provide assistance or prompt the user for more details.",
        "Ensure effective communication between agents, and intervene when necessary to help complete the user's request.",
        "Keep the workflow smooth by ensuring both agents work in parallel, without unnecessary overlap in their tasks."
    ],
    show_tool_calls=True,
    add_chat_history_to_messages=True,
    add_datetime_to_instructions=True,
    markdown=True
    )