import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

def train_model():
    print("📥 Loading your dataset...")

    # Load YOUR dataset
    df = pd.read_csv("spam_ham_dataset.csv")

    # Keep only needed columns
    df = df[['text', 'label_num']]

    # Rename for clarity
    df.columns = ['text', 'label']

    print("✅ Dataset loaded:", df.shape)

    # -------------------------------
    # TEXT → NUMBERS (Vectorization)
    # -------------------------------
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=10000
    )

    X = vectorizer.fit_transform(df['text'])
    y = df['label']

    # -------------------------------
    # MODEL TRAINING
    # -------------------------------
    model = MultinomialNB(alpha=0.1)
    model.fit(X, y)

    # -------------------------------
    # SAVE MODEL
    # -------------------------------
    joblib.dump(model, "spam_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

    print("🎉 Model trained and saved!")
    print("Files created: spam_model.pkl, vectorizer.pkl")


if __name__ == "__main__":
    train_model()