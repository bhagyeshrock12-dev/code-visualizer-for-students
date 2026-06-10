from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

steps = []

class CodeInput(BaseModel):
    code: str

def trace_func(frame, event, arg):
    if event == "line":
        steps.append({
            "line": frame.f_lineno,
            "variables": dict(frame.f_locals)
        })
    return trace_func

@app.post("/run")
def run_code(data: CodeInput):
    global steps
    steps = []

    try:
        sys.settrace(trace_func)
        exec(data.code)
        sys.settrace(None)

        return {"steps": steps}

    except Exception as e:
        sys.settrace(None)
        return {"error": str(e)}