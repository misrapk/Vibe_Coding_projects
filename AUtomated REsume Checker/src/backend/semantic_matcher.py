import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Tuple

class SemanticMatcher:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        self.resume_index = faiss.IndexFlatIP(self.dimension)
        self.job_index = faiss.IndexFlatIP(self.dimension)
        
        # Metadata storage (maps FAISS index to object ID)
        self.resume_ids = [] 
        self.job_ids = []    

    def _get_embedding(self, text: str) -> np.ndarray:
        if not text.strip():
            return np.zeros((1, self.dimension), dtype=np.float32)
        
        embedding = self.model.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(embedding)
        return embedding.astype(np.float32)

    def rebuild_index(self, type: str, data_list: List[Dict[str, Any]]):
        """Rebuilds the FAISS index from a list of items with 'id' and 'embedding'."""
        if type == "resume":
            self.resume_index = faiss.IndexFlatIP(self.dimension)
            self.resume_ids = []
            if not data_list: return
            
            embeddings = []
            for item in data_list:
                if item.get("embedding"):
                    emb = np.frombuffer(item["embedding"], dtype=np.float32).reshape(1, -1)
                    embeddings.append(emb)
                    self.resume_ids.append(item["id"])
            
            if embeddings:
                self.resume_index.add(np.vstack(embeddings))
                
        elif type == "job":
            self.job_index = faiss.IndexFlatIP(self.dimension)
            self.job_ids = []
            if not data_list: return
            
            embeddings = []
            for item in data_list:
                if item.get("embedding"):
                    emb = np.frombuffer(item["embedding"], dtype=np.float32).reshape(1, -1)
                    embeddings.append(emb)
                    self.job_ids.append(item["id"])
            
            if embeddings:
                self.job_index.add(np.vstack(embeddings))

    def get_text_embedding(self, text: str) -> np.ndarray:
        return self._get_embedding(text)

    def search_resumes(self, job_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.resume_index.ntotal == 0:
            return []
            
        embedding = self._get_embedding(job_text)
        scores, indices = self.resume_index.search(embedding, min(top_k, self.resume_index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or idx >= len(self.resume_ids): continue
            results.append({
                "id": self.resume_ids[idx],
                "similarity_score": round(float(score) * 100, 2)
            })
        return results

    def calculate_match_score(self, resume_text: str, job_text: str) -> float:
        res_emb = self._get_embedding(resume_text)
        job_emb = self._get_embedding(job_text)
        score = np.dot(res_emb, job_emb.T)[0][0]
        return round(float(score) * 100, 2)
