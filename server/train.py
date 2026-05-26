# pyrefly: ignore [missing-import]
import numpy as np
from preprocess import load_corpus, replace_unk, build_vocab

def train_hmm(sentences, word_to_idx, tag_to_idx):

    num_tags = len(tag_to_idx)
    vocab_size = len(word_to_idx)

    pi = np.zeros(num_tags)

    A = np.zeros((num_tags, num_tags))

    B = np.zeros((num_tags, vocab_size))

    # Counting
    for sentence in sentences:

        first_tag = sentence[0][1]
        pi[tag_to_idx[first_tag]] += 1

        for i, (word, tag) in enumerate(sentence):

            tag_idx = tag_to_idx[tag]
            word_idx = word_to_idx[word]

            B[tag_idx, word_idx] += 1

            if i > 0:
                prev_tag = sentence[i - 1][1]

                prev_idx = tag_to_idx[prev_tag]

                A[prev_idx, tag_idx] += 1

    # Laplace smoothing
    pi += 1
    A += 1
    B += 1

    # Normalize
    pi = pi / pi.sum()

    A = A / A.sum(axis=1, keepdims=True)

    B = B / B.sum(axis=1, keepdims=True)

    return pi, A, B

if __name__ == "__main__":
    print("Loading and preprocessing data...")
    corpus = load_corpus('archive/brown.csv')
    processed_corpus = replace_unk(corpus, threshold=1)
    word_to_idx, idx_to_word, tag_to_idx, idx_to_tag = build_vocab(processed_corpus)
    
    print("Training HMM...")
    pi, A, B = train_hmm(processed_corpus, word_to_idx, tag_to_idx)
    
    print("Training complete.")
    print(f"Number of tags: {len(tag_to_idx)}")
    print(f"Vocabulary size: {len(word_to_idx)}")
    print("pi shape:", pi.shape)
    print("A shape:", A.shape)
    print("B shape:", B.shape)
    print(f"Sample pi sum: {pi.sum():.4f}")
    print(f"Sample A row sum: {A[0].sum():.4f}")
    print(f"Sample B row sum: {B[0].sum():.4f}")
