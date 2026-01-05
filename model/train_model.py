import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

# Paths to CSV files
base_path = "C:/Users/soumy/fake-news-detector/data"
files = {
    "politifact_real.csv": 1,
    "politifact_fake.csv": 0,
    "gossipcop_real.csv": 1,
    "gossipcop_fake.csv": 0
}

all_data = []

# Load and label data
for file_name, label in files.items():
    file_path = os.path.join(base_path, file_name)
    df = pd.read_csv(file_path)
    if "title" in df.columns:
        df = df[["title"]]
        df["label"] = label
        all_data.append(df)

# Combine everything
df_full = pd.concat(all_data).dropna().reset_index(drop=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(df_full["title"], df_full["label"], test_size=0.2, random_state=42)

# TF-IDF
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(class_weight='balanced', n_estimators=100)

model.fit(X_train_vec, y_train)

# Evaluation
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "model/fake_news_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model and vectorizer saved!")
