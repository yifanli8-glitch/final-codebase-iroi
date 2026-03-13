#!/usr/bin/env python3
"""
RAG Retriever with Confidence Gating
Implements vector-based retrieval with similarity scoring and fail-fast mechanism
"""
import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai library not installed")

# Import RAG config
try:
    from rag_config import (
        RAG_CONFIDENCE_THRESHOLD,
        RAG_TOP_K,
        RAG_MAX_CONTEXT_LENGTH,
        RAG_NO_ANSWER_MESSAGE,
        CHUNK_SIZE,
        CHUNK_OVERLAP,
        RAG_VERBOSE_LOGGING
    )
except ImportError:
    # Fallback defaults
    RAG_CONFIDENCE_THRESHOLD = 0.35
    RAG_TOP_K = 3
    RAG_MAX_CONTEXT_LENGTH = 5000
    RAG_NO_ANSWER_MESSAGE = "I can't find this in the lab knowledge base."
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    RAG_VERBOSE_LOGGING = True


class RAGRetriever:
    """Vector-based retrieval with confidence gating"""
    
    def __init__(self, api_key: str = None, docs_dir: str = None):
        """Initialize retriever
        
        Args:
            api_key: OpenAI API key for embeddings
            docs_dir: Directory containing markdown documents
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if OPENAI_AVAILABLE and self.api_key else None
        
        # Document chunks and embeddings
        self.chunks: List[Dict] = []  # [{"text": str, "source": str, "chunk_id": int}]
        self.embeddings: Optional[np.ndarray] = None  # shape: (n_chunks, embedding_dim)
        
        # Load and process documents
        if docs_dir:
            docs_path = Path(docs_dir)
        else:
            docs_path = Path(__file__).parent.parent / "docs"
        
        if docs_path.exists():
            self._load_and_chunk_documents(docs_path)
    
    def _load_and_chunk_documents(self, docs_path: Path):
        """Load markdown files and split into chunks"""
        print(f"📚 [RAG] Loading documents from {docs_path}")
        
        for md_file in docs_path.glob("**/*.md"):
            if md_file.name == "README.md":
                continue  # Skip README files
            
            try:
                content = md_file.read_text(encoding="utf-8")
                file_chunks = self._chunk_text(content, md_file.name)
                self.chunks.extend(file_chunks)
            except Exception as e:
                print(f"⚠️ [RAG] Failed to load {md_file}: {e}")
        
        print(f"✅ [RAG] Loaded {len(self.chunks)} chunks from {len(set(c['source'] for c in self.chunks))} files")
        
        # Generate embeddings
        if self.chunks and self.client:
            self._generate_embeddings()
    
    def _chunk_text(self, text: str, source: str) -> List[Dict]:
        """Split text into overlapping chunks
        
        Args:
            text: Document text
            source: Source filename
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        current_length = 0
        chunk_id = 0
        
        for line in lines:
            line_length = len(line) + 1  # +1 for newline
            
            # If adding this line exceeds chunk size, save current chunk
            if current_length + line_length > CHUNK_SIZE and current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "source": source,
                    "chunk_id": chunk_id
                })
                chunk_id += 1
                
                # Keep overlap
                overlap_chars = 0
                overlap_lines = []
                for i in range(len(current_chunk) - 1, -1, -1):
                    overlap_chars += len(current_chunk[i]) + 1
                    if overlap_chars > CHUNK_OVERLAP:
                        break
                    overlap_lines.insert(0, current_chunk[i])
                
                current_chunk = overlap_lines
                current_length = sum(len(l) + 1 for l in overlap_lines)
            
            current_chunk.append(line)
            current_length += line_length
        
        # Add final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "source": source,
                "chunk_id": chunk_id
            })
        
        return chunks
    
    def _generate_embeddings(self):
        """Generate embeddings for all chunks"""
        if not self.client:
            print("⚠️ [RAG] OpenAI client not available, cannot generate embeddings")
            return
        
        print(f"🔄 [RAG] Generating embeddings for {len(self.chunks)} chunks...")
        start_time = time.time()
        
        try:
            # Batch embed all chunks
            texts = [chunk["text"] for chunk in self.chunks]
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            
            # Convert to numpy array
            embeddings_list = [item.embedding for item in response.data]
            self.embeddings = np.array(embeddings_list)
            
            elapsed = time.time() - start_time
            print(f"✅ [RAG] Generated embeddings in {elapsed:.2f}s (shape: {self.embeddings.shape})")
            
        except Exception as e:
            print(f"❌ [RAG] Failed to generate embeddings: {e}")
            import traceback
            traceback.print_exc()
    
    def retrieve(self, query: str, top_k: int = None) -> Dict:
        """Retrieve relevant chunks with confidence gating
        
        Args:
            query: User query
            top_k: Number of top chunks to retrieve (default: RAG_TOP_K)
            
        Returns:
            Dictionary with:
            - status: "success" or "no_answer"
            - chunks: List of retrieved chunks (if status == "success")
            - scores: List of similarity scores (if status == "success")
            - message: User-facing message (if status == "no_answer")
            - metadata: Logging metadata
        """
        top_k = top_k or RAG_TOP_K
        
        # Log query
        metadata = {
            "query": query,
            "timestamp": time.time(),
            "top_k": top_k,
            "threshold": RAG_CONFIDENCE_THRESHOLD
        }
        
        # Check if embeddings are available
        if self.embeddings is None or len(self.chunks) == 0:
            metadata["decision"] = "fail_fast"
            metadata["reason"] = "no_embeddings"
            if RAG_VERBOSE_LOGGING:
                print(f"❌ [RAG Retrieve] No embeddings available")
                print(f"   Query: {query}")
            return {
                "status": "no_answer",
                "message": RAG_NO_ANSWER_MESSAGE,
                "metadata": metadata
            }
        
        if not self.client:
            metadata["decision"] = "fail_fast"
            metadata["reason"] = "no_client"
            if RAG_VERBOSE_LOGGING:
                print(f"❌ [RAG Retrieve] OpenAI client not available")
            return {
                "status": "no_answer",
                "message": RAG_NO_ANSWER_MESSAGE,
                "metadata": metadata
            }
        
        try:
            # Generate query embedding
            query_response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=[query]
            )
            query_embedding = np.array(query_response.data[0].embedding)
            
            # Calculate cosine similarity
            similarities = self._cosine_similarity(query_embedding, self.embeddings)
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            top_scores = similarities[top_indices]
            top_chunks = [self.chunks[i] for i in top_indices]
            
            # Log retrieval results
            metadata["top1_score"] = float(top_scores[0])
            metadata["top_chunks"] = [
                {"source": chunk["source"], "chunk_id": chunk["chunk_id"], "score": float(score)}
                for chunk, score in zip(top_chunks, top_scores)
            ]
            
            # ========== CONFIDENCE GATING ==========
            if top_scores[0] < RAG_CONFIDENCE_THRESHOLD:
                metadata["decision"] = "low_confidence"
                metadata["reason"] = "below_threshold"
                
                if RAG_VERBOSE_LOGGING:
                    print(f"ℹ️ [RAG] Low confidence ({top_scores[0]:.3f} < {RAG_CONFIDENCE_THRESHOLD})")
                    print(f"   Query: {query}")
                    for i, (chunk, score) in enumerate(zip(top_chunks, top_scores)):
                        print(f"   {i+1}. [{score:.3f}] {chunk['source']} (chunk {chunk['chunk_id']})")
                
                return {
                    "status": "no_answer",
                    "message": RAG_NO_ANSWER_MESSAGE,
                    "metadata": metadata
                }
            
            # ========== PASS: High confidence ==========
            metadata["decision"] = "pass"
            
            if RAG_VERBOSE_LOGGING:
                print(f"✅ [RAG] Match found (top-1 score: {top_scores[0]:.3f})")
                print(f"   Query: {query}")
                for i, (chunk, score) in enumerate(zip(top_chunks, top_scores)):
                    print(f"   {i+1}. [{score:.3f}] {chunk['source']} (chunk {chunk['chunk_id']})")
            
            return {
                "status": "success",
                "chunks": top_chunks,
                "scores": top_scores.tolist(),
                "metadata": metadata
            }
            
        except Exception as e:
            metadata["decision"] = "error"
            metadata["error"] = str(e)
            
            print(f"❌ [RAG Retrieve] Error during retrieval: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "status": "no_answer",
                "message": "Sorry, I encountered an error during retrieval.",
                "metadata": metadata
            }
    
    def _cosine_similarity(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between query and documents
        
        Args:
            query_embedding: Query embedding (1D array)
            doc_embeddings: Document embeddings (2D array, shape: [n_docs, embedding_dim])
            
        Returns:
            Similarity scores (1D array, shape: [n_docs])
        """
        # Normalize
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
        
        # Dot product
        similarities = np.dot(doc_norms, query_norm)
        return similarities
    
    def get_context_for_llm(self, chunks: List[Dict], max_length: int = None) -> str:
        """Format retrieved chunks as context for LLM
        
        Args:
            chunks: Retrieved chunks
            max_length: Maximum context length (default: RAG_MAX_CONTEXT_LENGTH)
            
        Returns:
            Formatted context string
        """
        max_length = max_length or RAG_MAX_CONTEXT_LENGTH
        
        context_parts = []
        current_length = 0
        
        for chunk in chunks:
            chunk_text = f"[Source: {chunk['source']}]\n{chunk['text']}\n"
            chunk_length = len(chunk_text)
            
            if current_length + chunk_length > max_length:
                break
            
            context_parts.append(chunk_text)
            current_length += chunk_length
        
        return "\n---\n\n".join(context_parts)
