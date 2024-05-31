import io

import pandas as pd
import matplotlib.pyplot as plt
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse

from src.services.preprocess import preprocess_data

api_router = APIRouter()


@api_router.post("/predict")
def predict(request: Request, file: UploadFile = File(...)):
    model = request.app.state.model

    df = pd.read_csv(file.file)
    file.file.close()

    df, ids = preprocess_data(df)
    preds = model.predict_proba(df)
    df_probas = pd.Series(preds, index=ids).reset_index()
    df_probas.columns = ["client_id", "score"]
    df_probas.to_csv("probas.csv", index=False)


    labels = (preds >= model.threshold).astype(int)
    df_response = pd.Series(labels, index=ids).reset_index()
    df_response.columns = ["client_id", "pred"]
    df_response.to_csv("preds.csv", index=False)
    return "OK"


@api_router.get("/importances")
def get_importances(request: Request):
    model = request.app.state.model
    importances = pd.Series(
        model.model.get_feature_importance(),
        index=model.model.feature_names_,
    )
    response = importances.sort_values(ascending=False).head(5).to_dict()
    return response


@api_router.get("/scores")
def get_scores_distr():
    df = pd.read_csv("probas.csv")
    fig, ax = plt.subplots()
    plt.hist(df["score"])
    plt.title("Score distribution")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@api_router.get("/download_preds")
def get_scores_distr():
    return FileResponse("preds.csv", media_type="text/csv")


@api_router.get("/")
async def main():
    content = """
    <body>
    <form action="/predict" method="POST" enctype="multipart/form-data">
        <label for="file">Upload a file for prediction:</label>
        <input type="file" id="file" name="file"><br />
        <button>Upload</button>
    </form>

    <form action="/download_preds" method="GET" enctype="multipart/form-data">
        <button>Download predictions</button>
    </form>

    <form action="/importances" method="GET" enctype="multipart/form-data">
        <button>Get importances</button>
    </form>

    <form action="/scores" method="GET" enctype="multipart/form-data">
        <button>Get scores distribution</button>
    </form>
    </body>
    """
    return HTMLResponse(content=content)
