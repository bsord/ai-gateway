from langchain.llms import OpenAI

from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from pydantic import BaseModel, Field
from tools.custom_tools import GetNewsTool

def complete_prompt(prompt: str):

    # define the LLM of choice
    llm = OpenAI(temperature=0.0)

    # load tools 
    get_news_tool = GetNewsTool()
    tools = [
        Tool(
            func=get_news_tool,
            name = "get_news",
            description="useful for when you need to answer questions about a subreddit"
        ),
    ]

    # initialize the agent with our LLM of choice and array of previously defined tools.
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    completion_response = agent.run(prompt)

    return completion_response
