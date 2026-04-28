PROMPT_TEMPLATE = """You are an assistant answering questions based ONLY on the provided context.

Context:
{context}

Question:
{question}

Grounding Rules:
- Only use information from the context
- If the answer is not in the context, say "I don't know"
- Do NOT make up information
- Do NOT mention the context or how the answer was generated

Answer Guidelines:
- Start the answer directly (no introductions)
- Be clear and specific
- Use concise language
- Include relevant details from the context
- Avoid vague or generic statements
- Use bullet points if listing multiple items

Answer:"""


def build_prompt(context: str, question: str) -> str:
    return PROMPT_TEMPLATE.format(context=context, question=question)
