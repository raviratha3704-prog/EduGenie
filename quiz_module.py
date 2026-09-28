import json
import re
from typing import Any

from fastapi import HTTPException

from gemini_client import generate_text


# ---------------------------------------------------------
# Clean Gemini JSON response
# ---------------------------------------------------------

def clean_json_block(
    text: str
) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start = text.find("[")
    end = text.rfind("]")

    if start >= 0 and end > start:

        return text[
            start:end + 1
        ]

    return text


# ---------------------------------------------------------
# Validate quiz
# ---------------------------------------------------------

def _validate_quiz(
    data: Any
) -> list[dict]:

    if not isinstance(data, list):

        raise ValueError(
            "Quiz response must be a JSON list."
        )

    if len(data) != 3:

        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )

    normalized = []

    for index, item in enumerate(
        data,
        start=1
    ):

        if not isinstance(item, dict):

            raise ValueError(
                f"Question {index} is not an object."
            )

        question = str(
            item.get(
                "question",
                ""
            )
        ).strip()

        options = item.get(
            "options"
        )

        answer = str(
            item.get(
                "correct_answer",
                ""
            )
        ).strip()

        if not question:

            raise ValueError(
                f"Question {index} "
                "has no question text."
            )

        if (
            not isinstance(options, list)
            or len(options) != 4
        ):

            raise ValueError(
                f"Question {index} "
                "must have exactly 4 options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if any(
            not option
            for option in options
        ):

            raise ValueError(
                f"Question {index} "
                "contains an empty option."
            )

        if answer not in options:

            raise ValueError(
                f"Question {index}'s "
                "correct_answer must exactly "
                "match one option."
            )

        normalized.append(
            {
                "question": question,
                "options": options,
                "correct_answer": answer,
            }
        )

    return normalized


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

async def generate_quiz(
    text: str,
    topic: str | None = None
) -> dict:

    topic_line = (
        f"Topic: {topic}"
        if topic
        else "Topic: infer it from the passage."
    )

    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational passage below.

Requirements:

- Exactly 3 questions.
- Exactly 4 options per question.
- Exactly one correct answer.
- Distractors should be plausible.
- Questions must be answerable from the passage.
- Do not use information outside the passage.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not use ```json.

Required JSON format:

[
  {{
    "question": "string",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A"
  }}
]

{topic_line}

Passage:

{text}
""".strip()

    raw = await generate_text(
        prompt,
        temperature=0.2
    )

    try:

        data = json.loads(
            clean_json_block(raw)
        )

        quiz = _validate_quiz(data)

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "Gemini generated an invalid "
                f"quiz response: {exc}"
            ),
        ) from exc

    return {
        "quiz": quiz
    }