# pyrefly: ignore [missing-import]
import numpy as np

def viterbi(sentence,
            pi,
            A,
            B,
            word_to_idx,
            tag_to_idx,
            idx_to_tag):

    num_tags = len(tag_to_idx)
    T = len(sentence)

    log_pi = np.log(pi)
    log_A = np.log(A)
    log_B = np.log(B)

    V = np.zeros((num_tags, T))

    BP = np.zeros((num_tags, T), dtype=int)

   
    words = []

    for word in sentence:
        if word not in word_to_idx:
            word = "<UNK>"

        words.append(word_to_idx[word])

   

    first_word = words[0]

    for i in range(num_tags):
        V[i, 0] = log_pi[i] + log_B[i, first_word]


    for t in range(1, T):

        for i in range(num_tags):

            best_score = -np.inf
            best_prev = 0

            for j in range(num_tags):

                score = (
                    V[j, t - 1]
                    + log_A[j, i]
                    + log_B[i, words[t]]
                )

                if score > best_score:
                    best_score = score
                    best_prev = j

            V[i, t] = best_score
            BP[i, t] = best_prev



    best_last_tag = np.argmax(V[:, -1])

    best_path = [best_last_tag]

    for t in range(T - 1, 0, -1):

        best_last_tag = BP[best_last_tag, t]

        best_path.append(best_last_tag)

    best_path.reverse()

    predicted_tags = [
        idx_to_tag[tag_idx]
        for tag_idx in best_path
    ]

    return predicted_tags

if __name__ == "__main__":
    from preprocess import load_corpus, replace_unk, build_vocab
    from train import train_hmm
    
    print("Loading and preprocessing data...")
    corpus = load_corpus('archive/brown.csv')
    processed_corpus = replace_unk(corpus, threshold=1)
    word_to_idx, idx_to_word, tag_to_idx, idx_to_tag = build_vocab(processed_corpus)
    
    print("Training HMM...")
    pi, A, B = train_hmm(processed_corpus, word_to_idx, tag_to_idx)
    
    sentence = ["The", "dog", "runs"]
    print(f"\nRunning Viterbi on sentence: {sentence}")
    tags = viterbi(sentence, pi, A, B, word_to_idx, tag_to_idx, idx_to_tag)
    print(f"Predicted tags: {tags}")
