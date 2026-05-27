import random
from preprocess import load_corpus, replace_unk, build_vocab
from train import train_hmm
from viterbi import viterbi

def evaluate(test_sentences, pi, A, B, word_to_idx, tag_to_idx, idx_to_tag):
    correct = 0
    total = 0
    
    for i, sentence in enumerate(test_sentences):
        words = [word for word, tag in sentence]
        true_tags = [tag for word, tag in sentence]
        
        
        if not words:
            continue
            
        predicted_tags = viterbi(words, pi, A, B, word_to_idx, tag_to_idx, idx_to_tag)
        
        for true_tag, pred_tag in zip(true_tags, predicted_tags):
            if true_tag == pred_tag:
                correct += 1
            total += 1
            
        if (i + 1) % 100 == 0:
            print(f"Evaluated {i + 1} sentences...")
            
    accuracy = correct / total if total > 0 else 0
    return accuracy

def main():
    print("Loading corpus...")
    corpus = load_corpus('archive/brown.csv')
    
    # Shuffle for a random split
    random.seed(42)
    random.shuffle(corpus)
    
    split_idx = int(len(corpus) * 0.8)
    train_corpus = corpus[:split_idx]
    test_corpus = corpus[split_idx:]
    
    print(f"Train size: {len(train_corpus)} sentences")
    print(f"Test size: {len(test_corpus)} sentences")
    
    print("Preprocessing training set...")
    processed_train = replace_unk(train_corpus, threshold=1)
    word_to_idx, idx_to_word, tag_to_idx, idx_to_tag = build_vocab(processed_train)
    
    print("Training HMM...")
    pi, A, B = train_hmm(processed_train, word_to_idx, tag_to_idx)
    
    print("Evaluating on a subset of test set...")
    # Evaluate on a subset of the test set so it finishes in a reasonable time
    subset_test = test_corpus[:500] 
    accuracy = evaluate(subset_test, pi, A, B, word_to_idx, tag_to_idx, idx_to_tag)
    
    print(f"Accuracy on {len(subset_test)} test sentences: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()
