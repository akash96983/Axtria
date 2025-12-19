FOLLOW_UP_KEYWORDS = [
    "that",
    "it",
    "those",
    "what about",
    "and",
    "also",
    "for this",
    "for these"
]

def is_follow_up(question: str):
    q = question.lower()
    return any(k in q for k in FOLLOW_UP_KEYWORDS)
