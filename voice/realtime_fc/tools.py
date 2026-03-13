"""
Tool definitions and execution for Realtime API function calling.

Two tools:
  - search_knowledge_base : RAG retrieval (embeddings + cosine similarity)
  - analyze_image         : GPT-4o Vision analysis of student-uploaded diagram
"""

import os
from typing import Optional

# ── Tool JSON schemas (sent in session.update) ──────────────────────────

RAG_TOOL = {
    "type": "function",
    "name": "search_knowledge_base",
    "description": (
        "Search the lab course knowledge base for information about sensors, "
        "circuits, power supplies, oscilloscopes, multimeters, wiring, "
        "measurements, and lab procedures. "
        "Call this tool whenever the student asks a technical question."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query derived from the student's question",
            }
        },
        "required": ["query"],
    },
}

IMAGE_TOOL = {
    "type": "function",
    "name": "analyze_image",
    "description": (
        "Analyze a diagram or photo that the student uploaded via the camera. "
        "Call this when the conversation indicates a new image has been uploaded."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "What to look for or verify in the image",
            }
        },
        "required": ["question"],
    },
}

ALL_TOOLS = [RAG_TOOL, IMAGE_TOOL]

# ── Session instructions (no full knowledge-base dump) ──────────────────

# FC_INSTRUCTIONS = """\
# You are IROI, a Sensor and Circuit course teaching assistant robot.
# Always respond in English regardless of the language you hear.

# You help students in a lab environment with questions about sensors, circuits, \
# power supplies, oscilloscopes, multimeters, wiring, and measurements.

# Tools:
# - search_knowledge_base – look up facts from the course knowledge base. \
#   You MUST call this for every question.
# - analyze_image – examine a diagram/photo the student uploaded.

# Rules:
# - Always respond in English.
# - Keep answers short, structured, and spoken-friendly (you are a voice assistant).
# - If search results have no relevant info, say "I don't have that in my knowledge base."
# - If you have no relevant info, say "I don't have that in my knowledge base."
# - If search results have no relevant info, say "I don't have that in my knowledge base."
# - For complex problems, guide step by step (1, 2, 3…).
# - Never invent facts; only use what the tools return.
# - Sound like a patient, friendly lab TA.
# """


FC_INSTRUCTIONS = """\
You are IROI, a lab teaching assistant robot for a Sensor and Circuit course.
Always respond in English regardless of what language the student uses.
You are a voice assistant — keep answers short, structured, and spoken-friendly.

Tools:
- search_knowledge_base – look up facts from the course knowledge base. Call this when the student asks a course-related or technical question.
- analyze_image – examine a diagram or photo the student uploaded.

Answering policy:
- For every new question, call search_knowledge_base with a query based on what the user JUST said. Do not reuse previous search results.
- Derive the search query strictly from the user's latest utterance. Do not let earlier topics influence the query.
- When search results are relevant, use them as your primary source.
- When search results are not relevant, answer from your own knowledge honestly.
- Do not invent lab procedures, wiring steps, or safety rules. If unsure, say so.
- For complex questions, guide step by step (1, 2, 3…).
- If you cannot clearly understand what the user said, ask them to repeat instead of guessing.

Style:
- Be concise and clear, like a friendly lab TA.
- Short sentences. Use structure when helpful.
- Go straight to the answer — no meta-commentary about the knowledge base.
"""

# ── Execution helpers ────────────────────────────────────────────────────


def execute_rag(query: str, rag_retriever) -> str:
    """Run vector retrieval and return formatted context for the model."""
    if not rag_retriever:
        return "Knowledge base is not available."

    result = rag_retriever.retrieve(query)

    if result["status"] == "success":
        context = rag_retriever.get_context_for_llm(result["chunks"])
        return context[:3000]

    metadata = result.get("metadata", {})
    top1_score = metadata.get("top1_score")
    threshold = metadata.get("threshold")
    reason = metadata.get("reason")

    if reason == "below_threshold":
        score_text = (
            f"{top1_score:.3f}" if isinstance(top1_score, (float, int)) else "N/A"
        )
        threshold_text = (
            f"{threshold:.3f}" if isinstance(threshold, (float, int)) else "N/A"
        )
        return (
            "RAG confidence is too low, so do not use any knowledge-base context "
            f"(top-1 score={score_text}, threshold={threshold_text}). "
            "Answer from your own general knowledge."
        )

    return (
        "No relevant information found in the knowledge base. "
        "Answer from your own general knowledge."
    )


def execute_image_analysis(
    question: str,
    image_path: Optional[str],
    api_key: str,
) -> str:
    """Call GPT-4o Vision to analyse the student's uploaded image."""
    if not image_path or not os.path.exists(image_path):
        return (
            "No image has been uploaded yet. "
            "Ask the student to tap the camera icon to upload a photo."
        )

    try:
        import base64

        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a lab teaching assistant. "
                        "Analyze the diagram/image and answer concisely."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=500,
        )
        return resp.choices[0].message.content

    except Exception as e:
        return f"Image analysis failed: {e}"
