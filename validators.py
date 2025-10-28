"""
Input validation functions for Kaizen learning system.

All validators return tuples: (is_valid: bool, error_message: str | None)
"""

from datetime import datetime
import re


def validate_username(username: str) -> tuple[bool, str | None]:
    """
    Validate username input.

    Rules:
    - Not empty
    - 3-20 characters
    - Only alphanumeric and underscores allowed
    - Converted to lowercase

    Args:
        username: The username to validate

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not username or not isinstance(username, str):
        return (False, "Username cannot be empty")

    if len(username) < 3 or len(username) > 20:
        return (False, "Username must be 3-20 characters")

    # Only alphanumeric and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return (False, "Username can only contain letters, numbers, and underscores")

    return (True, None)


def validate_tone_mode(tone_mode: str) -> tuple[bool, str | None]:
    """
    Validate tone mode input.

    Rules:
    - Must be one of: playful, motivating, soft, genz
    - Case-insensitive comparison

    Args:
        tone_mode: The tone mode to validate

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    valid_modes = ["playful", "motivating", "soft", "genz"]

    if not tone_mode or not isinstance(tone_mode, str):
        return (False, "Tone mode cannot be empty")

    if tone_mode.lower() not in valid_modes:
        return (False, f"Tone mode must be one of: {', '.join(valid_modes)}")

    return (True, None)


def validate_date(date_str: str) -> tuple[bool, str | None]:
    """
    Validate date string in ISO 8601 format.

    Rules:
    - Format: YYYY-MM-DD
    - Must be a valid calendar date

    Args:
        date_str: The date string to validate

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not date_str or not isinstance(date_str, str):
        return (False, "Date cannot be empty")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return (True, None)
    except ValueError:
        return (False, "Date must be in YYYY-MM-DD format")


def validate_quiz_score(score: float | None) -> tuple[bool, str | None]:
    """
    Validate quiz score.

    Rules:
    - None is allowed (quiz not taken)
    - If not None, must be float between 0.0 and 1.0 (inclusive)

    Args:
        score: The quiz score to validate

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if score is None:
        return (True, None)

    if not isinstance(score, (int, float)):
        return (False, "Quiz score must be a number or None")

    if score < 0.0 or score > 1.0:
        return (False, "Quiz score must be between 0.0 and 1.0")

    return (True, None)


def validate_topic_type(topic_type: str) -> tuple[bool, str | None]:
    """
    Validate topic type.

    Rules:
    - Must be one of: new_topic, review_topic, completion_milestone, rest_day

    Args:
        topic_type: The topic type to validate

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    valid_types = ["new_topic", "review_topic", "completion_milestone", "rest_day"]

    if not topic_type or not isinstance(topic_type, str):
        return (False, "Topic type cannot be empty")

    if topic_type not in valid_types:
        return (False, f"Topic type must be one of: {', '.join(valid_types)}")

    return (True, None)


def validate_language(language: str) -> tuple[bool, str | None]:
    """
    Validate programming language name.

    Rules:
    - Not empty
    - Minimum 2 characters
    - Converted to lowercase

    Args:
        language: The language name to validate

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not language or not isinstance(language, str):
        return (False, "Language cannot be empty")

    if len(language) < 2:
        return (False, "Language name must be at least 2 characters")

    return (True, None)
