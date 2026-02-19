from fastapi import FastAPI
import socket, os, time

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "host": socket.gethostname()}

@app.get("/")
def root():
    return {"message": "lab-devops-2026", "env": os.getenv("ENV", "local"), "time": time.time()}

