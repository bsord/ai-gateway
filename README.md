# ai-gateway
api gateway powered by langchain for accessing various AI tooling

## Getting started

1. Rename .env-sample to .env
2. set openai key in .env file
3. run `docker compose up`
4. using POST method, make a request to localhost:8080/prompt with a json body that includes a 'prompt' field like so:
```
{
    "prompt": "hello world"
}
```