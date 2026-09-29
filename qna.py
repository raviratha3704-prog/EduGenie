from gemini_client import generate_text


async def answer_question(
    question: str
) -> dict:

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and clearly.

Requirements:

- Give a direct answer first.
- Explain the concept in simple language.
- Use an example when useful.
- Break complicated ideas into smaller parts.
- Do not invent sources or citations.
- If the question is ambiguous, clearly state your assumption.
- Keep the answer appropriate for a student.

Student question:

{question}
""".strip()

    answer = await generate_text(
        prompt,
        temperature=0.3
    )

    return {
        "answer": answer
    }