from langchain.llms import OpenAI

from langchain.agents import initialize_agent
from langchain.agents import AgentType

from tools.news import GetNewsTool
from tools.video import MakeShortFormVideoTool

def complete_prompt(prompt: str):

    # define the LLM of choice
    llm = OpenAI(temperature=0.0)

    # load tools
    tools = [
        GetNewsTool(),
        MakeShortFormVideoTool()
    ]

    # initialize the agent with our LLM of choice and array of previously defined tools.
    agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    completion_response = agent.run(prompt)

    return completion_response
