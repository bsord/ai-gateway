from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

def complete_prompt(prompt: str):

    # define the LLM of choice
    llm = OpenAI(temperature=0.0)

    prompt_template = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    completion_response = chain.run("colorful socks")
    
    return completion_response
