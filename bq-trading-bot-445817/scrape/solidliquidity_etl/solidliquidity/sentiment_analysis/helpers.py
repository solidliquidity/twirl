def batch_analyze_sentiment(comments, nlp, sentiment_model):
    """
    Perform sentiment analysis for a batch of comments.

    Args:
        comments (list): List of comment strings.
        nlp: SpaCy NLP pipeline.
        sentiment_model: Hugging Face sentiment analysis pipeline.

    Returns:
        list: A list of dictionaries with extracted stocks and sentiment.
    """
    results = []
    for comment in comments:
        result = extract_stocks_and_sentiment(comment, nlp, sentiment_model)
        results.append(result)
    return results
