import os
import datetime
import joblib
import uvicorn
import pandas as pd

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

from .db import init_db, insert_event, get_customer_events, get_customer_features


MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/xgb_churn.pkl")
model = None


def load_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            model = None
    return model


class EventPayload(BaseModel):
    customer_id: str
    event_type: str
    properties: dict = {}
    timestamp: datetime.datetime = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    load_model()
    yield


app = FastAPI(title="Customer Journey MVP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/webhook/event")
async def webhook_event(payload: EventPayload):
    ts = payload.timestamp or datetime.datetime.utcnow()
    insert_event(payload.customer_id, payload.event_type, payload.properties, ts)
    return {"status": "accepted", "customer_id": payload.customer_id}


@app.post("/score/online")
async def score_online(payload: dict):
    model_inst = load_model()
    if model_inst is None:
        raise HTTPException(status_code=503, detail="Model not available")
    X = pd.DataFrame([payload.get("features", {})])
    try:
        if hasattr(model_inst, "predict_proba"):
            prob = float(model_inst.predict_proba(X)[:, 1][0])
        else:
            prob = float(model_inst.predict(X)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
    return {"churn_prob": prob}


@app.get("/customers/{customer_id}/journey")
async def customer_journey(customer_id: str):
    events = get_customer_events(customer_id)
    return {"customer_id": customer_id, "events": events}


@app.get("/customers/{customer_id}/features")
async def customer_features(customer_id: str):
    feats = get_customer_features(customer_id)
    return {"customer_id": customer_id, "features": feats}


@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return {"filename": file.filename, "rows": int(df.shape[0])}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)