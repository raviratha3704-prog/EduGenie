from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="AI-powered learning assistant",
    version="1.0.0",
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# Request models
# ---------------------------------------------------------

class QARequest(BaseModel):
    question: str = Field(..., min_length=1)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"
    weeks: int = Field(default=4, ge=1, le=24)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

@app.post("/qa")
async def qa(request: QARequest):
    try:
        return await answer_question(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to answer the question: {str(exc)}"
        )


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

@app.post("/explain")
async def explain(request: ExplainRequest):
    try:
        return await explain_topic(request.topic)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to explain the topic: {str(exc)}"
        )


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(request: QuizRequest):
    try:
        return await generate_quiz(request.topic)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate the quiz: {str(exc)}"
        )


# ---------------------------------------------------------
# Summarization
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(request: SummaryRequest):
    try:
        return await summarize_text(request.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to summarize the text: {str(exc)}"
        )


# ---------------------------------------------------------
# Learning recommendations
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(request: LearningPathRequest):
    try:
        return await get_learning_recommendations(
            topic=request.topic,
            level=request.level,
            weeks=request.weeks,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate learning path: {str(exc)}"
        )