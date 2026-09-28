from gemini_client import generate_text


async def summarize_text(
    text: str
) -> dict:

    prompt = f"""
Summarize the educational passage below
for quick revision.

Requirements:

- Keep the important facts.
- Keep important relationships between ideas.
- Remove repetition.
- Use simple language.
- Prefer a short heading followed by bullet points.
- Do not introduce information that is not
  present in the passage.

Passage:

{text}
""".strip()

    summary = await generate_text(
        prompt,
        temperature=0.25
    )

    return {
        "summary": summary
    }