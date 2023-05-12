from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

def complete_prompt(prompt: str):

    # define the LLM of choice
    llm = OpenAI(temperature=0.0)

    # load tools 
    tools = load_tools(["llm-math"], llm=llm)

    # initialize the agent with our LLM of choice and array of previously defined tools.
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    completion_response = agent.run(" What is the result of 42 raised to the .023 power?")

    return completion_response
