import csv
import os




#function to read the data set and retuns an array of sentences as tuple of word and tag 
def load_corpus(path):
    sentences = []
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, path)
    
    with open(abs_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if not row or len(row) < 4:
                continue
            
            
            raw_text = row[3]
            
            word_tag_pairs = raw_text.split()
            
            sentence = []
            for pair in word_tag_pairs:
                
                parts = pair.rsplit('/', 1)
                if len(parts) == 2:
                    sentence.append((parts[0], parts[1]))
                else:
                    sentence.append((pair, ''))
            
            sentences.append(sentence)

    return sentences



# function to replace tag of less frequent words with unknown 


def replace_unk(sentences, threshold=1):
    word_counts = {}

    # Count words
    for sentence in sentences:
        for word, tag in sentence:
            word_counts[word] = word_counts.get(word, 0) + 1

    processed = []

    # Replace rare words
    for sentence in sentences:
        new_sentence = []

        for word, tag in sentence:
            if word_counts[word] <= threshold:
                word = "<UNK>"

            new_sentence.append((word, tag))

        processed.append(new_sentence)

    return processed

def build_vocab(sentences):
    vocab = set()
    tags = set()

    for sentence in sentences:
        for word, tag in sentence:
            vocab.add(word)
            tags.add(tag)

    vocab.add("<UNK>")

    word_to_idx = {
        word: i
        for i, word in enumerate(sorted(vocab))
    }

    tag_to_idx = {
        tag: i
        for i, tag in enumerate(sorted(tags))
    }

    idx_to_word = {
        i: word
        for word, i in word_to_idx.items()
    }

    idx_to_tag = {
        i: tag
        for tag, i in tag_to_idx.items()
    }

    return (
        word_to_idx,
        idx_to_word,
        tag_to_idx,
        idx_to_tag
    )

if __name__ == "__main__":
    corpus = load_corpus('archive/brown.csv')
    print(f"Loaded {len(corpus)} sentences.")
    print("First sentence:")
    print(corpus[0])
    
    processed_corpus = replace_unk(corpus, threshold=1)
    print("First sentence after replace_unk:")
    print(processed_corpus[0])
    
    word_to_idx, idx_to_word, tag_to_idx, idx_to_tag = build_vocab(processed_corpus)
    print(f"Vocab size: {len(word_to_idx)}, Tags: {len(tag_to_idx)}")