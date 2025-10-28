"""
Data persistence layer for Kaizen learning system.

Handles all JSON file I/O operations for user profiles and schedules.
"""

import json
import os
from pathlib import Path
from typing import Optional
from validators import (
    validate_username,
    validate_language,
    validate_tone_mode,
    validate_date,
    validate_topic_type,
    validate_quiz_score
)

# Constants
DATA_DIR = "data/users"
FILE_EXTENSION = ".json"


def _get_user_file_path(username: str) -> str:
    """
    Get the file path for a user's data file.

    Args:
        username: The username

    Returns:
        Full path to user's JSON file
    """
    return os.path.join(DATA_DIR, f"{username}{FILE_EXTENSION}")


def load_user_data(username: str) -> Optional[dict]:
    """
    Load user data from JSON file.

    Args:
        username: The username to load

    Returns:
        Dictionary with user data if file exists, None otherwise

    Raises:
        ValueError: If JSON is malformed
        PermissionError: If file read permission denied
    """
    file_path = _get_user_file_path(username)

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in user file")
    except PermissionError:
        raise PermissionError(f"Permission denied reading user file: {file_path}")


def save_user_data(username: str, data: dict) -> bool:
    """
    Save user data to JSON file.

    Args:
        username: The username
        data: Dictionary containing user data

    Returns:
        True on success

    Raises:
        ValueError: If username is invalid
        IOError: If write operation fails
    """
    # Validate username
    valid, error = validate_username(username)
    if not valid:
        raise ValueError(f"Invalid username: {error}")

    # Create directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    file_path = _get_user_file_path(username)

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        raise IOError(f"Failed to write user data: {str(e)}")


def create_user(username: str, language: str, tone_mode: str, start_date: str) -> dict:
    """
    Create a new user with profile and empty schedule.

    Args:
        username: User's unique identifier
        language: Programming language being learned
        tone_mode: Notification personality
        start_date: Learning journey start date (YYYY-MM-DD)

    Returns:
        Dictionary with created user data

    Raises:
        ValueError: If any validation fails
    """
    # Validate all inputs
    valid, error = validate_username(username)
    if not valid:
        raise ValueError(error)

    valid, error = validate_language(language)
    if not valid:
        raise ValueError(error)

    valid, error = validate_tone_mode(tone_mode)
    if not valid:
        raise ValueError(error)

    valid, error = validate_date(start_date)
    if not valid:
        raise ValueError(error)

    # Normalize to lowercase
    username = username.lower()
    language = language.lower()
    tone_mode = tone_mode.lower()

    # Create user data structure
    user_data = {
        "profile": {
            "username": username,
            "language": language,
            "tone_mode": tone_mode,
            "start_date": start_date
        },
        "schedule": {}
    }

    # Persist to file
    save_user_data(username, user_data)

    return user_data


def update_schedule(
    username: str,
    day_key: str,
    topic: str,
    topic_type: str,
    quiz_score: Optional[float] = None
) -> bool:
    """
    Update or add a day entry in user's schedule.

    Args:
        username: The username
        day_key: Day identifier (e.g., "day_1", "day_2")
        topic: Topic name
        topic_type: Type of topic (new_topic/review_topic/completion_milestone/rest_day)
        quiz_score: Quiz score (0.0-1.0) or None

    Returns:
        True on success

    Raises:
        ValueError: If user not found or validation fails
    """
    # Load current user data
    user_data = load_user_data(username)
    if user_data is None:
        raise ValueError("User not found")

    # Validate topic_type and quiz_score
    valid, error = validate_topic_type(topic_type)
    if not valid:
        raise ValueError(error)

    valid, error = validate_quiz_score(quiz_score)
    if not valid:
        raise ValueError(error)

    # Add/update day entry
    user_data["schedule"][day_key] = {
        "topic": topic,
        "type": topic_type,
        "quiz_score": quiz_score
    }

    # Save updated data
    save_user_data(username, user_data)

    return True


def get_user_schedule(username: str) -> dict:
    """
    Get user's schedule data.

    Args:
        username: The username

    Returns:
        Dictionary with schedule data, empty dict if user doesn't exist
    """
    user_data = load_user_data(username)
    if user_data is None:
        return {}

    return user_data.get("schedule", {})


def user_exists(username: str) -> bool:
    """
    Check if user file exists.

    Args:
        username: The username to check

    Returns:
        True if user exists, False otherwise
    """
    file_path = _get_user_file_path(username)
    return os.path.exists(file_path)


def get_all_usernames() -> list[str]:
    """
    Get list of all existing usernames.

    Returns:
        List of usernames (without .json extension)
        Empty list if directory doesn't exist or is empty
    """
    if not os.path.exists(DATA_DIR):
        return []

    usernames = []
    try:
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(FILE_EXTENSION):
                # Remove .json extension
                username = filename[:-len(FILE_EXTENSION)]
                usernames.append(username)
    except Exception:
        return []

    return usernames
