from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query import get_query, get_individual_details, get_class, get_class_details
from fastapi import Request

app = FastAPI()

class QueryInput(BaseModel):
    query: str
    class_name: str

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
        return {"error":"False", "data":result}
    except Exception as e:
        return {"error":"True", "message":str(e)}

@app.post("/execute-query-individuals-details")
def execute_query_details(query_input: QueryInput):
    try:
        query = query_input.query
        result = get_individual_details(query)
        return {"error":"False", "data":result}
    except Exception as e:
        return {"error":"True", "message":str(e)}

@app.get("/execute-query-class")
def execute_query_class():
    try:
        result = get_class()
        return {"error":"False", "data":result}
    except Exception as e:
        return {"error":"True", "message":str(e)}

@app.get("/execute-query-class-details")
def execute_query_class_details(classname: QueryInput):
    try:
        query = classname.class_name
        result = get_class_details(query)
        return {"error":"False", "data":result}
    except Exception as e:
        return {"error":"True", "message":str(e)}