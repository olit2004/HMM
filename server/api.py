import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from preprocess import load_corpus, replace_unk, build_vocab
from train import train_hmm
from viterbi import viterbi

# Global variables for the trained model
hmm_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading corpus and training HMM on startup...")
    corpus = load_corpus('archive/brown.csv')
    processed_corpus = replace_unk(corpus, threshold=1)
    word_to_idx, idx_to_word, tag_to_idx, idx_to_tag = build_vocab(processed_corpus)
    
    pi, A, B = train_hmm(processed_corpus, word_to_idx, tag_to_idx)
    
    hmm_model['pi'] = pi
    hmm_model['A'] = A
    hmm_model['B'] = B
    hmm_model['word_to_idx'] = word_to_idx
    hmm_model['tag_to_idx'] = tag_to_idx
    hmm_model['idx_to_tag'] = idx_to_tag
    print("HMM Model trained successfully!")
    yield
    # Cleanup if needed
    hmm_model.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentenceRequest(BaseModel):
    sentence: str

@app.post("/api/tag")
def tag_sentence(req: SentenceRequest):
    if not hmm_model:
        raise HTTPException(status_code=503, detail="Model is not ready yet.")
    
    words = req.sentence.strip().split()
    if not words:
        return []
    
    predicted_tags = viterbi(
        words, 
        hmm_model['pi'], 
        hmm_model['A'], 
        hmm_model['B'], 
        hmm_model['word_to_idx'], 
        hmm_model['tag_to_idx'], 
        hmm_model['idx_to_tag']
    )
    
    return [{"word": word, "tag": tag} for word, tag in zip(words, predicted_tags)]

client_dir = os.path.join(os.path.dirname(__file__), '..', 'client')
if os.path.exists(client_dir):
    app.mount("/", StaticFiles(directory=client_dir, html=True), name="client")
