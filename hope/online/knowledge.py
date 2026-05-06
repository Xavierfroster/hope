import wikipedia

def get_wikipedia_summary(query):
    """Fetches a summary from Wikipedia."""
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except Exception:
        return None
