import requests
from typing import Optional, Type
from pydantic import Field, BaseModel
from langchain.tools import BaseTool

class GetNewsSchema(BaseModel):
    subreddit: str = Field(description="should be a search query")

class GetNewsTool(BaseTool):
    name = "get_news"
    description = "useful for when you need to get news about a subreddit"
    args_schema: Type[GetNewsSchema] = GetNewsSchema

    def _run(self, subreddit: str) -> str:
        """Use the tool."""
        print('testing')
        result = requests.get("https://api.f5.news/posts/{subreddit}".format(subreddit = subreddit))
        return result.text
    
    async def _arun(self, subreddit: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("get_news does not support async")