from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.anthropic import Anthropic

from tools.games import find_games_tool, get_game_details_tool

load_dotenv()


llm = Anthropic(
    model="claude-haiku-4-5",
)


agent = FunctionAgent(
    tools=[
        find_games_tool,
        get_game_details_tool,
    ],
    llm=llm,
    system_prompt=(
        "You are MeepleMind, a board game assistant. "
        "Use the available tools to answer questions about board games. "
        "Only make claims based on information returned by the tools. "
        "Never add general knowledge about board games. "
        "If a tool returns status='no_match', respond only with the message "
        "provided by the tool. Do not explain why, do not speculate, "
        "and do not suggest alternatives unless they were returned by a tool. "
        "Be precise with numerical values returned by tools. "
        "Do not reinterpret or approximate them. "
        "For example, if a game takes 20 minutes, say 20 minutes, not under 20 minutes."
    ),
)