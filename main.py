import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import prompt, test

# init fast api
app = FastAPI()

# default exception handler
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    print(str(exc))

# configure cors
origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt.router) #/prompt/*
app.include_router(test.router) #/prompt/*

# root handler
@app.get("/")
def read_root():
    return {"Status": "Ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)