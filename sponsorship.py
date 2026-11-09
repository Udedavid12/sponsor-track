import re

# Positive signals (increase score)
POSITIVE_KEYWORDS = {
    r"visa sponsorship": 50,
    r"sponsor(s|ing)? (a )?visa": 50,
    r"sponsorship available": 50,
    r"we sponsor": 40,
    r"relocation (assistance|package)": 30,
    r"international candidates": 20,
    r"global (company|team)": 10,
    r"multinational": 10,
}

# Negative signals (decrease score)
NEGATIVE_KEYWORDS = {
    r"must be authorized to work": -30,
    r"no visa sponsorship": -100,
    r"cannot sponsor": -100,
    r"security clearance required": -50,
    r"us citizens? only": -100,
    r"must be a (canadian )?citizen": -100,
}

def analyze_sponsorship(description: str) -> dict:
    """
    Analyzes a job description and returns a score and category.
    """
    if not description:
        return {"score": 0, "category": "UNKNOWN", "signals": []}

    text = description.lower()
    score = 0
    matched_signals = []

    # 1. Check for positive signals
    for pattern, points in POSITIVE_KEYWORDS.items():
        if re.search(pattern, text):
            score += points
            matched_signals.append(f"+{points} for '{pattern}'")

    # 2. Check for negative signals
    for pattern, points in NEGATIVE_KEYWORDS.items():
        if re.search(pattern, text):
            score += points  # points are already negative
            matched_signals.append(f"{points} for '{pattern}'")

    # 3. Contextual bonus: Company size / Seniority (Basic heuristic)
    if "senior" in text or "lead" in text or "principal" in text:
        score += 10
        matched_signals.append("+10 for Seniority")
    
    # Cap the score between 0 and 100
    score = max(0, min(score, 100))

    # 4. Categorize
    if score >= 70:
        category = "LIKELY"
    elif score <= 30:
        category = "UNLIKELY"
    else:
        category = "UNKNOWN"

    return {
        "score": score,
        "category": category,
        "signals": matched_signals
    }