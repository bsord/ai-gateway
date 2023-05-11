import openai

def complete_prompt(prompt: str):

    # define messages object to send to openAI
    messages_to_openai = [
        {"role": "system", "content": "you are a helpful ai assistant"}
    ]
    messages_to_openai.append(
        {"role": "user", "content": prompt} 
    )

    completion_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_to_openai,
        temperature=0.0
    )

    return completion_response
