from gemini_client import generate_text


async def get_learning_recommendations(
    topic: str,
    level: str,
    hours_per_week: int
) -> dict:

    prompt = f"""
Create a personalized learning path
for the following topic:

{topic}

Learner level:

{level}

Available study time:

{hours_per_week} hours per week.

Create a practical learning plan.

Include:

1. Overall learning goal

2. Foundation topics

3. Intermediate topics

4. Advanced topics where appropriate

5. Weekly schedule

6. Practice exercises

7. Project ideas

8. Suggested resource TYPES

Examples:

- Official documentation
- Textbooks
- Courses
- Tutorials
- Videos
- Practice websites

Do not invent URLs.

9. Progress assessment

10. Final project suggestion

Make the plan realistic and adaptable.
""".strip()

    recommendations = await generate_text(
        prompt,
        temperature=0.5
    )

    return {
        "recommendations": recommendations
    }