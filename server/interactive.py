import sys
from preprocess import load_corpus, replace_unk, build_vocab
from train import train_hmm
from viterbi import viterbi

def interactive_loop(pi, A, B, word_to_idx, tag_to_idx, idx_to_tag):
    print("\n" + "="*50)
    print("HMM POS Tagger Interactive Mode")
    print("Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")
    
    while True:
        try:
            sentence_str = input("Enter a sentence: ").strip()
            if sentence_str.lower() in ['exit', 'quit']:
                break
                
            if not sentence_str:
                continue
                
            # Split the sentence into words
            words = sentence_str.split()
            
            # Predict the tags using Viterbi
            predicted_tags = viterbi(words, pi, A, B, word_to_idx, tag_to_idx, idx_to_tag)
            
            # Display results formatted nicely
            print("\nPredicted POS tags:")
            for word, tag in zip(words, predicted_tags):
                print(f"{word:15} -> {tag}")
            print("-" * 30 + "\n")
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

def main():
    print("Loading corpus and training HMM (this may take a few seconds)...")
    
    # We use the whole dataset to train for the best interactive results
    corpus = load_corpus('archive/brown.csv')
    processed_corpus = replace_unk(corpus, threshold=1)
    word_to_idx, idx_to_word, tag_to_idx, idx_to_tag = build_vocab(processed_corpus)
    
    pi, A, B = train_hmm(processed_corpus, word_to_idx, tag_to_idx)
    
    print("Model trained successfully!")
    interactive_loop(pi, A, B, word_to_idx, tag_to_idx, idx_to_tag)

if __name__ == "__main__":
    main()
