from fastapi import FastAPI
import socket, os, time

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "host": socket.gethostname()}
@app.get("/burn")
def burn():
    x = 0
    for i in range(30_000_000):
        x += i
    return {"result": x}
@app.get("/")
def root():
    return {"message": "lab-devops-2026", "env": os.getenv("ENV", "local"), "time": time.time()}

