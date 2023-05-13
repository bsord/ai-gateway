from fastapi import APIRouter
from services.text_to_speech import get_audio
from pydantic import BaseModel

router = APIRouter(
    prefix="/test",
    tags=["prompt"],
    responses={404: {"description": "Not found"}},
)

class TextToSpeechInput(BaseModel):
    text: str

@router.post("/text-to-speech")
def text_to_speech(input: TextToSpeechInput):
    print(input.text)
    
    # get completion/response
    audio_file_path = get_audio(text=input.text)
    print(audio_file_path)

    return {"status": "ok"}


