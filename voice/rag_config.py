#!/usr/bin/env python3
"""
RAG Configuration
Manages retrieval confidence gating and other RAG parameters
"""
import os

# ========== Retrieval Confidence Gating ==========
# Minimum similarity score for top-1 chunk to allow KB context usage.
# If top1_score < THRESHOLD, do not pass retrieved chunks to the model.
# Default is intentionally strict: only trust RAG when confidence is high.
RAG_CONFIDENCE_THRESHOLD = float(os.getenv("RAG_CONFIDENCE_THRESHOLD", "0.6"))

# Number of top chunks to retrieve
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))

# Maximum context length to send to LLM (in characters)
RAG_MAX_CONTEXT_LENGTH = int(os.getenv("RAG_MAX_CONTEXT_LENGTH", "5000"))

# ========== Low-confidence Response ==========
# Returned to the caller when retrieval confidence is below the threshold.
# The caller (or model) should still try to answer from general knowledge.
RAG_NO_ANSWER_MESSAGE = (
    "No relevant information found in the knowledge base for this query."
)

# ========== Chunking Parameters ==========
# Size of each document chunk (in characters)
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "500"))

# Overlap between consecutive chunks (in characters)
CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "100"))

# ========== LLM Contract ==========
# System instructions sent when retrieved context is available
RAG_SYSTEM_INSTRUCTIONS = """\
You are IROI, a lab teaching assistant robot for a Sensor and Circuit course.
Always respond in English regardless of what language the student uses.

Below is relevant context retrieved from the course knowledge base.
Use it as your primary source when it contains the answer.
If the context does not cover the question, you may answer from your own knowledge.
Do not invent lab procedures, wiring steps, or safety rules.
Be concise, clear, and go straight to the answer.

Knowledge Base Context:
{context}
"""

# ========== Logging ==========
# Enable detailed RAG logging
RAG_VERBOSE_LOGGING = os.getenv("RAG_VERBOSE_LOGGING", "true").lower() == "true"
