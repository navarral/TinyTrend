
# Run this line only the first time 
# import nltk
# nltk.download('punkt_tab')

# Import nltk tokenizer
from nltk.tokenize import sent_tokenize, word_tokenize

# Import nltk stemmer
from nltk.stem import SnowballStemmer
stemmer_snowball = SnowballStemmer('italian')

# Import italian lemmatiser
import spacy
lemma_spacy = spacy.load("it_core_news_sm")

# Import libraries for code
from collections import Counter
from pathlib import Path
# Path to the folder where this script is located
script_dir = Path(__file__).parent

print("Script directory:", script_dir)

# Path to your folder
text_folder = script_dir / "test_data"

# Empti dictionary
token_dict = {}

for i, file in enumerate(text_folder.glob("*.txt")):
    # if i not in (1,5):
    #    continue
    if i == 1:
        key = file.stem.split("_")[-1]
        # 1. Read text file
        text_run = file.read_text(encoding="utf-8")
        # 2. Tokenise
        word_tokenizer_output = word_tokenize(text_run, language="italian")
        # Keep unique elements (for the future)
        # word_list_unique = list(set(word_list))
        # Limit to first 20 words for display
        word_list = word_tokenizer_output #[:50]

        print(f"\n--- Tokens and Stems for {key} ---")
        print(f"\nStemming {len(word_list)} words\n")

        # Define header and formatting (only Snowball)
        header = ['Word', 'Stem', 'Lemma']
        row_format = '{:<20} : {:<20} : {:<20}'

        # Print header and separator
        print(row_format.format(*header))
        print('-' * 66)

        # Remove words less than 3 characters
        word_list_long = [x for x in word_list if len(x) > 3]

        # 3. Compare stemmatisation and lemmatisation methods
        for word in word_list_long:
            stem = stemmer_snowball.stem(word)
            lemma = lemma_spacy(word)[0].lemma_.lower()  # spaCy lemma
            # print(row_format.format(word, stem, lemma))

        # Print footer line
        # print('-' * 42)
        # print(row_format.format(*header))
            
        # 4. Word counts (stems and lemmas separately)
        stems = [stemmer_snowball.stem(w) for w in word_list_long]
        lemmas = [lemma_spacy(w)[0].lemma_.lower() for w in word_list_long]

        stem_counts = Counter(stems)
        lemma_counts = Counter(lemmas)

        # Stem frequency table (top 10)
        print("\n--- Top 20 Stemmed Word Frequencies ---\n")
        print(f"{'Stem':<20} : {'Count':<5}")
        print('-'*30)
        for stem, count in stem_counts.most_common(10):
            print(f"{stem:<20} : {count:<5}")

        # Lemma frequency table (top 10)
        print("\n--- Top 20 Lemmatized Word Frequencies ---\n")
        print(f"{'Lemma':<20} : {'Count':<5}")
        print('-'*30)
        for lemma, count in lemma_counts.most_common(10):
            print(f"{lemma:<20} : {count:<5}")

print("\nTokenization complete!")


exit()

# Keep unique elements (for the future)
word_list_unique = list(set(word_list))
# Create dictionary: key = last part after "_", value = text content
texts_dict = {}

for file in text_folder.glob("*.txt"):
    # Extract the last part after the last underscore, before .txt
    key = file.stem.split("_")[-1]
    
    # Read file content
    texts_dict[key] = file.read_text(encoding="utf-8")

print(f"Loaded {len(texts_dict)} files")
print("Example keys:", list(texts_dict.keys())[:5])

# Tokenize and store results in another dictionary
tokenized_dict = {}

for key, text_run in texts_dict.items():
    word_tokenizer_output = word_tokenize(text_run, language='italian')
    tokenized_dict[key] = word_tokenizer_output

    print(f"\nOutput data for {key} (via Word Tokenizer):")
    for token in word_tokenizer_output[:10]:  # print only first 30 tokens
        print(f"\t{token}")

print("\nTokenization complete!")
print(f"Tokenized {len(tokenized_dict)} texts.")

word_tokenizer_output = word_tokenize(text_run, language='italian')

print('Output data (via Word Tokenizer):') 
for token in word_tokenizer_output:
     print('\t{}'.format(token))