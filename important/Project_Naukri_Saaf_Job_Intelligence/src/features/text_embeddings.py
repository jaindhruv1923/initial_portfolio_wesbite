"""
Dense Semantic Text Embeddings (Zero-Dependency Latent Semantic Analysis)
========================================================================
Implements a hardened, zero-dependency Semantic Embedding Encoder using
Sublinear TF-IDF + N-gram tokenization and Randomized Singular Value
Decomposition (Randomized SVD / Latent Semantic Analysis).

Eliminates external binary DLL blocks (e.g. PyTorch on Windows 11 Smart
App Control) while providing 128-dimensional dense semantic vectors
for fast pairwise similarity, clustering, and duplicate detection.
"""

import re
import math
from collections import Counter, defaultdict
import numpy as np

class DenseSemanticEncoder:
    """
    Transforms text documents into dense, normalized semantic embeddings
    using BM25/Sublinear TF-IDF + Randomized SVD (LSA).
    """
    def __init__(self, n_components: int = 64, max_features: int = 5000, min_df: int = 3, max_df_ratio: float = 0.85, random_state: int = 42):
        self.n_components = n_components
        self.max_features = max_features
        self.min_df = min_df
        self.max_df_ratio = max_df_ratio
        self.random_state = random_state
        self.vocab = {}
        self.idf_ = None
        self.components_ = None
        self.singular_values_ = None

    def _tokenize(self, text: str) -> list[str]:
        if not isinstance(text, str):
            return []
        text = text.lower()
        # Extract alphabetic words
        words = re.findall(r"\b[a-z]{2,25}\b", text)
        # Generate unigrams and bigrams
        tokens = list(words)
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
        return tokens

    def fit(self, texts: list[str]) -> "DenseSemanticEncoder":
        n_docs = len(texts)
        doc_freq = Counter()
        doc_tokens = []
        
        for text in texts:
            tokens = set(self._tokenize(text))
            doc_tokens.append(tokens)
            for t in tokens:
                doc_freq[t] += 1
                
        # Filter by min_df and max_df
        max_df = int(n_docs * self.max_df_ratio)
        valid_terms = [
            t for t, df in doc_freq.items() 
            if self.min_df <= df <= max_df
        ]
        
        # Sort by frequency and cap at max_features
        valid_terms.sort(key=lambda t: doc_freq[t], reverse=True)
        valid_terms = valid_terms[:self.max_features]
        
        self.vocab = {t: idx for idx, t in enumerate(valid_terms)}
        n_vocab = len(self.vocab)
        
        # Compute smoothed IDF: log(1 + (N + 1) / (DF + 1)) + 1
        self.idf_ = np.zeros(n_vocab)
        for t, idx in self.vocab.items():
            self.idf_[idx] = math.log(1.0 + (n_docs + 1.0) / (doc_freq[t] + 1.0)) + 1.0
            
        # Build Sparse/Dense Term-Doc Matrix
        X_tfidf = self._transform_tfidf(texts)
        
        # Randomized SVD (Halko et al., 2011)
        rng = np.random.RandomState(self.random_state)
        k = min(self.n_components, n_vocab - 1, n_docs - 1)
        p = 10  # oversampling parameter
        
        # Random Gaussian projection matrix
        Omega = rng.randn(n_vocab, k + p)
        # Power iteration for spectral decay
        Y = np.dot(X_tfidf, Omega)
        for _ in range(2):
            Y = np.dot(X_tfidf, np.dot(X_tfidf.T, Y))
            
        Q, _ = np.linalg.qr(Y, mode="reduced")
        B = np.dot(Q.T, X_tfidf)
        
        U_tilde, S, Vt = np.linalg.svd(B, full_matrices=False)
        self.components_ = Vt[:k, :]
        self.singular_values_ = S[:k]
        
        return self

    def _transform_tfidf(self, texts: list[str]) -> np.ndarray:
        n_docs = len(texts)
        n_vocab = len(self.vocab)
        X = np.zeros((n_docs, n_vocab), dtype=np.float32)
        
        for i, text in enumerate(texts):
            tokens = self._tokenize(text)
            if not tokens:
                continue
            tf_counts = Counter(t for t in tokens if t in self.vocab)
            for t, count in tf_counts.items():
                idx = self.vocab[t]
                # Sublinear TF scaling: 1 + log(tf)
                tf_weight = 1.0 + math.log(count)
                X[i, idx] = tf_weight * self.idf_[idx]
                
        # Euclidean L2 normalization per document
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return X / norms

    def transform(self, texts: list[str]) -> np.ndarray:
        """Projects texts into dense normalized k-dimensional semantic space."""
        X_tfidf = self._transform_tfidf(texts)
        dense_embeds = np.dot(X_tfidf, self.components_.T)
        
        # L2 normalize embeddings
        embed_norms = np.linalg.norm(dense_embeds, axis=1, keepdims=True)
        embed_norms[embed_norms == 0] = 1.0
        return dense_embeds / embed_norms

    def fit_transform(self, texts: list[str]) -> np.ndarray:
        self.fit(texts)
        return self.transform(texts)

    @staticmethod
    def cosine_similarity(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """Computes pairwise cosine similarity between normalized embedding matrices."""
        return np.dot(A, B.T)
