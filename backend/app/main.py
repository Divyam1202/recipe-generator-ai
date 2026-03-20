from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .model_loader import load_model

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    print("Starting FastAPI server...")
    load_model()


app.include_router(router)