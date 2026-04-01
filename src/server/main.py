from fastapi import FastAPI
from pydantic import BaseModel
from src.llm.agent import create_agent

app = FastAPI(title="Financial Agent API")

# Initialize Agent
agent = create_agent()

class QueryRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        response = agent.invoke({"input": request.question})
        return {"answer": response["output"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Financial Agent API is running"}