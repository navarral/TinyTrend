import requests
import time
from datetime import datetime

API_KEY = "29c0f3b3-f189-44e7-af1e-4ac8d16b01a5" 

import requests
from collections import deque

def get_related_words_babelnet(word, lang="IT", max_synsets=5):
    """
    BabelNet has excellent Italian coverage and includes domain-specific terms.
    You'll need a free API key from https://babelnet.org/register
    """
    API_KEY = "29c0f3b3-f189-44e7-af1e-4ac8d16b01a5"
    
    related_words = set()
    
    # Step 1: Get synset IDs for the word
    print(f"Searching for synsets of '{word}'...")
    synset_url = f"https://babelnet.io/v9/getSynsetIds"
    params = {
        'lemma': word,
        'searchLang': lang,
        'key': API_KEY
    }
    
    try:
        response = requests.get(synset_url, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return related_words
            
        synsets = response.json()
        print(f"Found {len(synsets)} synsets")
        
        # Step 2: For each synset, get the full details
        for i, synset_data in enumerate(synsets[:max_synsets]):
            synset_id = synset_data['id']
            print(f"\nProcessing synset {i+1}/{min(len(synsets), max_synsets)}: {synset_id}")
            
            # Get synset details
            detail_url = f"https://babelnet.io/v9/getSynset"
            detail_params = {
                'id': synset_id,
                'targetLang': lang,
                'key': API_KEY
            }
            
            time.sleep(0.5) 
            detail_response = requests.get(detail_url, params=detail_params)
            
            if detail_response.status_code == 200:
                synset_info = detail_response.json()
                
                # Extract senses (synonyms)
                if 'senses' in synset_info:
                    for sense in synset_info['senses']:
                        # print(f"Sense keys: {sense.keys()}")
                        sense_lang = sense.get('properties', {}).get('language', '')
                        if sense_lang == lang:
                            lemma = sense.get('properties', {}).get('simpleLemma')
                            # print(lemma)
                            if lemma:
                                related_words.add(lemma)
                                # print(f"  - {lemma}")
                
                # Get outgoing edges (related concepts)
                edges_url = f"https://babelnet.io/v9/getOutgoingEdges"
                edges_params = {
                    'id': synset_id,
                    'key': API_KEY
                }
                
                time.sleep(0.5)
                edges_response = requests.get(edges_url, params=edges_params)
                
                if edges_response.status_code == 200:
                    edges = edges_response.json()
                    print(f"  Found {len(edges)} edges")
                    # Limit to avoid quota
                    for edge in edges:  
                        target_id = edge.get('target')
                        if target_id:
                            # Get target synset
                            time.sleep(0.5)
                            target_params = {
                                'id': target_id,
                                'targetLang': lang,
                                'key': API_KEY
                            }
                            target_response = requests.get(detail_url, params=target_params)
                            
                            if target_response.status_code == 200:
                                target_info = target_response.json()
                                if 'senses' in target_info:
                                    for sense in target_info['senses'][:3]:
                                        sense_lang = sense.get('properties', {}).get('language', '')
                                        if sense_lang == lang:
                                            lemma = sense.get('properties', {}).get('simpleLemma')
                                            if lemma:
                                                related_words.add(lemma)
                                                # print(f"    -> {lemma}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    return sorted(related_words)

# Example usage
seed_word = "sostanza chimica"
corpus_seed = get_related_words_babelnet(seed_word)
print(f"\nWords related to '{seed_word}' (via BabelNet):\n")
for w in corpus_seed :
    print(" -", w)

print(len(corpus_seed))

# Save to text file
timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
output_file = f"wp2/word_corpus/{seed_word}__BableNet_related_words_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for word in corpus_seed:
        f.write(word + "\n")

print(f"\nSaved {len(corpus_seed)} related words to: {output_file}")
