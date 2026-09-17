from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from go import run_agent
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    prompt: str

@app.post("/agent")
def agent_endpoint(request: AgentRequest):
    answer = run_agent(request.prompt)
    return {"answer": answer}

@app.get("/")
def read_root():
    return FileResponse("index.html")