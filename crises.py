import re
from typing import List

CRISES_KEYWORDS: List[str] = [
    "suicides", "suicide", "anxiety", "mental health crisis",
    "self-harm", "substance abuse", "kill myself", "want to die",
    "worthless", "can't go on", "ending it all", "no reason to live"
]

SAFETY_MESSAGE = (
    "💡 It sounds like you're going through a really tough time. "
    "You're not alone, and there are people who want to help you. "
    "Please consider reaching out to a mental health professional or contacting a helpline:\n\n"
    "**India:** 9152987821 (iCall), 1800-599-0019 (Vandrevala Foundation)\n"
    "**USA:** 988 (Suicide & Crisis Lifeline)\n"
    "**UK:** 116 123 (Samaritans)\n\n"
    "You matter. 💙"
)

def contains_crisis_keywords(text: str) -> bool:
    text_clean = re.sub(r"[^\w\s]", "", text.lower())
    return any(re.search(rf"\b{re.escape(keyword)}\b", text_clean) for keyword in CRISES_KEYWORDS)
