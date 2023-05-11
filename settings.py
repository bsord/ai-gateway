import os

global openai_api_key

def init():

    # set openAI key
    global openai_api_key
    openai_api_key = os.environ["OPENAI_API_KEY"]