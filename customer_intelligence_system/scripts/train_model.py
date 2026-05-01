
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/Customer-Churn.csv")

print("Columns in dataset:")
print(df.columns)

# ---------------- BASIC CLEANING ----------------

# Drop customerID if exists
if "customerID" in df.columns:
    df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges if exists
if "TotalCharges" in df.columns:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')

# Drop missing values
df.dropna(inplace=True)

# ---------------- TARGET COLUMN ----------------
if df["Churn"].dtype == "object":
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# ---------------- ENCODING ----------------
df = pd.get_dummies(df, drop_first=True)

# ---------------- SPLIT ----------------
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- SAVE ----------------
pickle.dump(model, open("models/churn_model.pkl", "wb"))
pickle.dump(X.columns, open("models/model_columns.pkl", "wb"))

print("✅ Model trained successfully")
print("📁 Files saved in models/")