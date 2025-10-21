from rdflib import Graph, Namespace, RDFS, URIRef
from datetime import datetime
from pathlib import Path

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from datetime import datetime
import nltk

# Ensure NLTK data is available
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


from deep_translator import GoogleTranslator

# === Load ontology ===
# Path to the folder where this script is located
script_dir = Path(__file__).parent

print("Script directory:", script_dir)

# Path to ontology file
owl_file = script_dir / "disdriv.owl" 
g = Graph()
g.parse(owl_file, format="xml")

# === Define common namespaces ===
OBO = Namespace("http://purl.obolibrary.org/obo/")
OBOINOWL = Namespace("http://www.geneontology.org/formats/oboInOwl#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

# === Collect all text values ===
all_text = set()

# 1. Labels
for _, _, label in g.triples((None, RDFS.label, None)):
    all_text.add(str(label))

# 2. Annotated targets
for _, _, annotated in g.triples((None, OWL.annotatedTarget, None)):
    all_text.add(str(annotated))

# --- Combine all text entries into one string ---
combined_text = " ".join(all_text)

# --- Tokenize (English) ---
tokens = word_tokenize(combined_text, language="english")

# --- Lowercase all tokens ---
tokens = [t.lower() for t in tokens]

# --- Remove stopwords ---
stop_words = set(stopwords.words("english"))
tokens = [t for t in tokens if t not in stop_words]

# --- Keep only alphabetic words and length > 3 ---
tokens = [t for t in tokens if t.isalpha() and len(t) > 3]

# --- Lemmatize tokens ---
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(t) for t in tokens]

# --- Remove duplicates and sort ---
unique_words = sorted(set(lemmatized_tokens))

print(f"English vocabulary size before translation: {len(unique_words)}")

# --- Translate to Italian ---
translator = GoogleTranslator(source="en", target="it")

italian_words = []
for word in unique_words:
    try:
        translated = translator.translate(word)
        italian_words.append(translated.lower())
    except Exception as e:
        print(f"⚠️ Could not translate '{word}': {e}")

# --- Unique Italian words ---
unique_italian = sorted(set(italian_words))

# === Save to file ===
timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
output_file = f"wp2/word_corpus/DISDRIV_words_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for line in unique_italian :
        f.write(line + "\n")

print(f"Extracted {len(unique_italian)} unique text entries from ontology.")
print(f"Saved to: {output_file}")