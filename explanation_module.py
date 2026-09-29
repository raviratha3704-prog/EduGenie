"""
EduGenie - Explanation Module

Provides simple topic explanations.
"""

def explain_topic(topic: str, level: str = "beginner") -> str:
    """
    Generate an explanation for a topic.

    Args:
        topic: Topic the student wants explained.
        level: Student level, e.g. beginner, intermediate, advanced.

    Returns:
        A text explanation.
    """

    topic = topic.strip()

    if not topic:
        return "Please provide a topic to explain."

    level = level.strip().lower() if level else "beginner"

    explanations = {
        "beginner": (
            f"{topic} is an important concept. "
            f"At a beginner level, you can understand {topic} "
            f"by focusing on its basic definition, purpose, and simple examples."
        ),
        "intermediate": (
            f"{topic} can be understood by studying its main concepts, "
            f"how those concepts are connected, and how {topic} "
            f"is applied in practical situations."
        ),
        "advanced": (
            f"{topic} can be studied in depth by examining its underlying "
            f"principles, technical details, practical applications, "
            f"limitations, and advanced use cases."
        ),
    }

    return explanations.get(
        level,
        explanations["beginner"]
    )


# Backward-compatible function names
def generate_explanation(topic: str, answer: str = "") -> str:
    """
    Compatibility wrapper for code that uses generate_explanation().
    """

    explanation = explain_topic(topic)

    if answer:
        return f"{explanation}\n\nAnswer:\n{answer}"

    return explanation


def explain_answer(topic: str, answer: str = "") -> str:
    """
    Compatibility wrapper for code that uses explain_answer().
    """

    return generate_explanation(topic, answer)


def ask_explanation(topic: str) -> str:
    """
    Compatibility wrapper for code that uses ask_explanation().
    """

    return explain_topic(topic)