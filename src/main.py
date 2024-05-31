import catboost as cb
from fastapi import FastAPI

from src.routers.api import api_router
from src.config import MODEL_PATH, THRESHOLD
from src.services.model import ClfModel


def create_app() -> FastAPI:
    app = FastAPI()
    set_routers(app)
    load_model(app)
    return app


def set_routers(app: FastAPI) -> None:
    app.include_router(api_router)


def load_model(app: FastAPI) -> None:
    _model = cb.CatBoostClassifier()
    _model.load_model(MODEL_PATH)

    model = ClfModel(_model, THRESHOLD)

    app.state.model = model


app = create_app()
