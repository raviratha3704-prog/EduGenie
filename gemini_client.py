import time
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


def _is_retryable_error(exc: Exception) -> bool:
    """
    Return True for temporary Gemini server/rate-limit errors.
    """

    error_text = str(exc).upper()

    retryable_codes = [
        "503",
        "UNAVAILABLE",
        "500",
        "INTERNAL",
        "502",
        "504",
        "DEADLINE_EXCEEDED",
        "429",
        "RESOURCE_EXHAUSTED",
    ]

    return any(
        code in error_text
        for code in retryable_codes
    )


async def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4
) -> str:

    client = get_client()

    max_retries = 3

    # Retry delays: 2s -> 4s -> 8s
    retry_delays = [2, 4, 8]

    for attempt in range(max_retries + 1):

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

            # If this is a temporary Gemini error,
            # retry the request.
            if (
                _is_retryable_error(exc)
                and attempt < max_retries
            ):

                delay = retry_delays[attempt]

                print(
                    f"Gemini temporary error detected. "
                    f"Retrying in {delay} seconds... "
                    f"(attempt {attempt + 1}/{max_retries})"
                )

                time.sleep(delay)

                continue

            # Final failure
            raise HTTPException(
                status_code=502,
                detail=(
                    f"Gemini request failed after "
                    f"{attempt + 1} attempt(s): {exc}"
                ),
            ) from exc