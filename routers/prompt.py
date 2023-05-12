from fastapi import APIRouter, Depends, HTTPException

import schemas
from services.chat_completion import complete_prompt

router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.CompletionResponse)
def chat_completion(prompt_input: schemas.PromptInput):
    print(prompt_input)
    
    # get completion/response
    completion_response = complete_prompt(prompt=prompt_input.prompt)
    print(completion_response)
    return schemas.CompletionResponse(response = completion_response)
