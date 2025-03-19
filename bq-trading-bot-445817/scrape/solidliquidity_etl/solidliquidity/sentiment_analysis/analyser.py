from .models import initialize_spacy_model, initialize_huggingface_model, initialize_finbert_model
import numpy as np

def extract_stocks_and_sentiment(comment, nlp, sentiment_model):
    """
    Extract stock mentions and their sentiment from a comment.

    Args:
        comment (str): The text of the comment.
        nlp: SpaCy NLP pipeline for Named Entity Recognition.
        sentiment_model: Hugging Face sentiment analysis pipeline.

    Returns:
        dict: A dictionary with extracted stocks and their sentiment.

    Example Output:
        {
            "Stocks": ["AAPL", "TSLA"],
            "Sentiment": "LABEL_2",
            "Score": 0.92
        }
    """
    # Extract stock mentions using SpaCy's NER
    doc = nlp(comment)
    stocks = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]]

    # Perform sentiment analysis using Hugging Face
    sentiment = sentiment_model(comment)[0]

    return {
        "Stocks": stocks,
        "Sentiment": sentiment["label"],
        "Score": sentiment["score"]
    }


def analyse_financial_headline(headline, sentiment_model):
    """
    Analyse the sentiment of a financial headline using FinBERT.

    Args:
        headline (str): The text of the headline.
        sentiment_model: Hugging Face sentiment analysis pipeline.

    Returns:
        dict: A dictionary containing the sentiment label and score.

    Example Output:
        {"Sentiment": "positive", "Score": 0.85}
    """
    result = sentiment_model(headline)[0]
    return {"Sentiment": result["label"], "Score": np.round(result["score"], 2)}
