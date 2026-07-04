# main.py — FastAPI application entry point: creates the app instance, registers routers, configures CORS middleware, and startup/shutdown events
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Tramet backend is running"}