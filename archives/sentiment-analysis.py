from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        dict: A dictionary containing the label and score of the sentiment.
    """
    result = sentiment_pipeline(text)
    return result[0] if result else None

if __name__ == "__main__":
    sample_text = "I do not hate you. Today was a bad day."
    print(f"Analyzing sentiment for: '{sample_text}'")
    sentiment_result = analyze_sentiment(sample_text)
    print(f"Sentiment: {sentiment_result['label']}, Score: {sentiment_result['score']:.4f}")