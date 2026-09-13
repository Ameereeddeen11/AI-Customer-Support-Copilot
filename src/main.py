from fastapi import FastAPI
from pydantic import BaseModel
from rag_query import ask, find_context

app = FastAPI(
    title="Rag Query API",
    description="RAG Query API is for answering customer questions based on the product catalog and FAQs",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    context: list[str]

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Welcome to the RAG Query API"
    }

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    found = find_context(request.question)
    resources = [meta["name"] for _, meta, _ in found]

    answer_text = ask(request.question)

    return QuestionResponse(
        answer=answer_text,
        context=resources
    )