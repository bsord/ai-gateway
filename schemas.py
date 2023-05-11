from pydantic import Json, BaseModel

class PromptInput(BaseModel):
    prompt: str

class CompletionResponse(BaseModel):
    response: str