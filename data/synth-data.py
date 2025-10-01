# synthetic data generator: customers + events -> writes events.parquet and a simple features.csv
import pandas as pd
import numpy as np
import uuid
import random
import datetime


def gen(N=2000):
customers = []
events = []
for i in range(N):
cid = f"user_{i}"
created = datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(30, 1000))
customers.append({"customer_id":cid, "created_at": created.isoformat(), "plan": random.choice(["free","pro","business"])})
num_events = np.random.poisson(20)
last = created
for j in range(num_events):
last = last + datetime.timedelta(days=max(1,int(np.random.exponential(10))))
evt = random.choices(["page_view","login","purchase","support_ticket","email_o
