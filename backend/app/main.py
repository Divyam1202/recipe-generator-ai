import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model_loader import load_model
from .routes import router

logger = logging.getLogger(__name__)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    print("Starting FastAPI server...")
    try:
        load_model()
    except Exception as exc:
        logger.warning("Model preloading skipped during startup: %s", exc)


app.include_router(router)
