import requests
from datetime import datetime

def get_related_words_conceptnet(word, lang="it", relation="RelatedTo", limit=20):
    """
    Query ConceptNet for related words in a given language.
    """

    # If limit = 0 → remove it from the query
    if limit == 0:
        url = f"https://api.conceptnet.io/query?node=/c/{lang}/{word}&rel=/r/{relation}"
    else:
        url = f"https://api.conceptnet.io/query?node=/c/{lang}/{word}&rel=/r/{relation}&limit={limit}"

    print(url)
    response = requests.get(url).json()

    related_words = set()
    for edge in response.get('edges', []):
        start = edge['start']['term']
        end = edge['end']['term']
        # Keep only Italian words
        if start.startswith(f"/c/{lang}/") and end.startswith(f"/c/{lang}/"):
            start_word = start.split('/')[-1].replace('_', ' ')
            end_word = end.split('/')[-1].replace('_', ' ')
            # Add the opposite node to the list (the “other side” of the edge)
            if start_word == word:
                related_words.add(end_word)
            else:
                related_words.add(start_word)

    return sorted(related_words)

# Example usage
seed_word = "chimico"
corpus_seed = get_related_words_conceptnet(word=seed_word, lang="it", relation="IsA", limit=400)
print(f"Words related to '{seed_word}' (via ConceptNet):", len(corpus_seed))
#for w in related:
#    print(" -", w)

exit()
# Save to text file
timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
output_file = f"wp2/word_corpus/{seed_word}_related_words_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for word in related:
        f.write(word + "\n")

print(f"\nSaved {len(related)} related words to: {output_file}")

