import pandas as pd
from predict import predict_news  # import your existing function

TEST_FILE = "data/manual_test.csv"

def evaluate_model():
    df = pd.read_csv(TEST_FILE)

    correct = 0
    total = len(df)

    for _, row in df.iterrows():
        text = row["text"]
        true_label = row["label"]  # 0 or 1

        pred_label_str = predict_news(text)
        pred_label = 0 if pred_label_str == "FAKE" else 1

        if pred_label == true_label:
            correct += 1

    accuracy = correct / total if total > 0 else 0
    print(f"Model Accuracy: {accuracy:.4f} ({correct}/{total})")

if __name__ == "__main__":
    evaluate_model()
