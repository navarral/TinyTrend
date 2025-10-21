import math
from collections import Counter
import numpy as np
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pathlib import Path
import re
from pprint import pprint
import pandas as pd
from tqdm import tqdm

# Import italian lemmatiser
lemma_spacy = spacy.load("it_core_news_sm")
from nltk.stem import SnowballStemmer
stemmer_snowball = SnowballStemmer('italian')
# stop_words_it = set(stopwords.words("italian"))

def clean_and_lemmatize(text):
    """Lemmatize Italian text and remove stopwords and short tokens."""
    # 1. Tokenise
    # doc_words = word_tokenize(text, language="italian")
    # 2. Lemmatisation
    # doc_words_lemma = [lemma_spacy(x)[0].lemma_.lower() for x in doc_words]

    doc = lemma_spacy(text)
    doc_words_lemma = [token.lemma_.lower() for token in doc]
    # doc_words_lemma = [stemmer_snowball.stem(w) for w in doc_words]
    # 3. Remove any token that contains whitespace (spaces, tabs, newlines)
    doc_words_no_space = [x for x in doc_words_lemma if not re.search(r'\s', x)]
    # 4. Remove words with non-alphabetic characters or too short
    doc_words_clean = [x for x in doc_words_no_space if x.isalpha() and len(x) > 3]
    # 5. Unique words
    doc_words_unique = sorted(set(doc_words_clean ))
    return doc_words_unique

# --- Load documents ---
script_dir = Path(__file__).parent
text_folder = script_dir / "test_data"

docs_tokens = []
doc_names = []

text_policies = list(text_folder.glob("*.txt"))

for file in tqdm(text_policies, desc="Processing documents"):
    text = file.read_text(encoding="utf-8")
    tokens = clean_and_lemmatize(text)
    docs_tokens.append(tokens)
    doc_names.append(file.stem)

print(f"Loaded and tokenized {len(docs_tokens)} documents")

# --- Build vocabulary ---
vocab = sorted(set(token for doc in docs_tokens for token in doc))
vocab_index = {word: i for i, word in enumerate(vocab)}

# --- Compute term frequencies (TF) ---
tf = np.zeros((len(docs_tokens), len(vocab)))
for i, tokens in enumerate(docs_tokens):
    counts = Counter(tokens)
    total = sum(counts.values())
    for word, count in counts.items():
        j = vocab_index[word]
        tf[i, j] = count / total  # normalized term frequency

# --- Compute inverse document frequency (IDF) ---
df = np.sum(tf > 0, axis=0)
idf = np.log((1 + len(docs_tokens)) / (1 + df)) + 1  # smoothed IDF

# --- Compute TF-IDF ---
tfidf = tf * idf

rows = []

# 1. Flatten all TF-IDF scores into a single array
all_scores = np.concatenate(tfidf)

# 2. Round scores to 6 decimals
# all_scores_rounded = np.round(all_scores, 6)

# 3. Compute global 90th percentile threshold
# global_threshold = round(np.percentile(all_scores_rounded, 90), 6)

all_scores_nonzero = all_scores[all_scores > 0]
global_threshold = round(np.percentile(all_scores_nonzero, 90), 6)

print(f"Global 90th percentile TF-IDF threshold: {global_threshold}")

# 4. Filter TF-IDF terms per document using the global threshold
for i, doc_name in enumerate(doc_names):
    row = np.round(tfidf[i], 6)  # round each document's row
    for idx, score in enumerate(row):
        if score >= global_threshold:
            rows.append({
                "document": doc_name,
                "term": vocab[idx],
                "tfidf": score
            })

# 3. Save as TSV
df_tfidf_top = pd.DataFrame(rows)
output_filename = script_dir / "output_data/df_policies_tfidf.tsv"
df_tfidf_top.to_csv(output_filename , sep="\t", index=False, encoding="utf-8")

print(f"Saved {len(df_tfidf_top)} TF-IDF terms (top 10%) across {len(doc_names)} documents")


