# Simple training helper (uses synthetic features CSV) - placeholder
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib


def train_from_csv(path="../data/features.csv", outpath="../models/xgb_churn.pkl"):
df = pd.read_csv(path)
X = df.drop(columns=["customer_id","label"])
y = df["label"]
model = GradientBoostingClassifier()
model.fit(X,y)
joblib.dump(model, outpath)
print("trained ->", outpath)


if __name__ == "__main__":
train_from_csv()
