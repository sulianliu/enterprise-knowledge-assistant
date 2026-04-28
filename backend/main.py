from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.query import router as query_router
from backend.rag.retrieval import index_documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    index_documents()
    yield


app = FastAPI(title="Enterprise Knowledge Assistant", lifespan=lifespan)
app.include_router(query_router)
