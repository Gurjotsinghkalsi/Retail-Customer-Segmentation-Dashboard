# ml_model/churn_train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib

# Load churn-labeled data
df = pd.read_csv("../data/churn_labeled_customers.csv")

# Features and target
X = df[["total_revenue", "total_invoices", "avg_basket_size", "unique_products"]]
y = df["is_churned"]

# Apply SMOTE to balance classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
print("📊 Classification Report (SMOTE):\n")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, "../data/churn_model.pkl")
joblib.dump(scaler, "../data/churn_scaler.pkl")
print("✅ Model and scaler saved to '../data/'")