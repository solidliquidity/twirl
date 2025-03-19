import spacy
from transformers import pipeline
from sentence_transformers import SentenceTransformer

def initialize_spacy_model():
    """
    Initialize and return the SpaCy NLP pipeline.
    """
    return spacy.load("en_core_web_sm")

def initialize_huggingface_model():
    """
    Initialize and return the Hugging Face sentiment analysis pipeline.
    """
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
        truncation=True,
        max_length=514
    )

def initialize_finbert_model():
    """
    Initialize and return the Hugging Face FinBERT pipeline for financial sentiment analysis.
    """
    return pipeline(
        "sentiment-analysis",
        model="ProsusAI/finbert",
    )

def initialize_sentence_transformer_model(): 
    model = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(model)
    return model
