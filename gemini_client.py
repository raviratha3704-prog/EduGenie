from functools import lru_cache

from fastapi import HTTPException
from google import genai

from config import settings


@lru_cache(maxsize=1)
def get_client():

    if not settings.gemini_api_key:

        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured. "
                "Please add it to your .env file."
            ),
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


async def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4
) -> str:

    client = get_client()

    try:

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={
                "temperature": temperature
            },
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Gemini request failed: {exc}",
        ) from exc