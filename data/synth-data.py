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
        customers.append(
            {
                "customer_id": cid,
                "created_at": created.isoformat(),
                "plan": random.choice(["free", "pro", "business"]),
            }
        )
        num_events = np.random.poisson(20)
        last = created
        for j in range(num_events):
            last = last + datetime.timedelta(days=max(1, int(np.random.exponential(10))))
            evt = random.choice(["page_view", "login", "purchase", "support_ticket", "email_open"])
            event = {
                "event_id": str(uuid.uuid4()),
                "customer_id": cid,
                "event_type": evt,
                "timestamp": last.isoformat(),
            }
            if evt == "purchase":
                event["amount"] = round(random.uniform(5, 500), 2)
            elif evt == "support_ticket":
                event["severity"] = random.choice(["low", "medium", "high"])
            elif evt == "email_open":
                event["campaign"] = random.choice(["welcome", "promo", "reengage"])
            events.append(event)

    customers_df = pd.DataFrame(customers)
    events_df = pd.DataFrame(events)

    customers_df.to_csv("features.csv", index=False)
    events_df.to_parquet("events.parquet", index=False)


if __name__ == "__main__":
    gen()
