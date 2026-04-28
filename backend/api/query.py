from fastapi import APIRouter
from pydantic import BaseModel

from backend.rag.embedding import generate_answer
from backend.rag.prompt import build_prompt
from backend.rag.retrieval import retrieve_chunks


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    chunks = retrieve_chunks(request.question)
    if not chunks:
        return QueryResponse(answer="I don't know", sources=[])

    context = "\n\n".join(chunk["content"] for chunk in chunks)
    prompt = build_prompt(context=context, question=request.question)
    answer = generate_answer(prompt)
    sources = sorted({chunk["source"] for chunk in chunks})

    return QueryResponse(answer=answer, sources=sources)
