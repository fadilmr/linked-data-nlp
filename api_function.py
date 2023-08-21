from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query import get_query
from fastapi import Request

app = FastAPI()

class QueryInput(BaseModel):
    query: str

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:5500",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"error":"False", "message":"Welcome to the API"}

@app.post("/execute-query")
def execute_query(query_input: QueryInput):
    try:
        query = query_input.query
        result = get_query(query)
        return {"error":"False", "message":str(result)}
    except Exception as e:
        return {"error":"True", "message":str(e)}
