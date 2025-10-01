# FastAPI app - webhook receiver + online scoring + simple customer endpoint
import os
import datetime
import joblib
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .db import init_db, insert_event, get_customer_events, get_customer_features

app = FastAPI(title="Customer Journey MVP")

MODEL_PATH = os.getenv("MODEL_PATH", "../models/xgb_churn.pkl")

# Lazy load model
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

@app.on_event("startup")
async def startup_event():
    init_db()
    load_model()

@app.post("/webhook/event")
async def webhook_event(payload: EventPayload):
    # Write event to DB
    ts = payload.timestamp or datetime.datetime.utcnow()
    insert_event(payload.customer_id, payload.event_type, payload.properties, ts)
    # TODO: push to Redis/Kafka for online processing
    return {"status": "accepted", "customer_id": payload.customer_id}

@app.post("/score/online")
async def score_online(payload: dict):
    # payload should contain precomputed features in the same order as training
    model = load_model()
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    import pandas as pd
    X = pd.DataFrame([payload["features"]])
    dmatrix = model.DMatrix(X) if hasattr(model, 'DMatrix') else None
    try:
        # handle sklearn-like or xgboost-like
        if hasattr(model, 'predict_proba'):
            prob = float(model.predict_proba(X)[:,1][0])
        else:
            prob = float(model.predict(X)[0])
    except Exception:
        prob = float(model.predict(X)[0])
    return {"churn_prob": prob}

@app.get("/customers/{customer_id}/journey")
async def customer_journey(customer_id: str):
    events = get_customer_events(customer_id)
    return {"customer_id": customer_id, "events": events}

@app.get("/customers/{customer_id}/features")
async def customer_features(customer_id: str):
    feats = get_customer_features(customer_id)
    return {"customer_id": customer_id, "features": feats}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
