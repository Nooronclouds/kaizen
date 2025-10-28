"""
Data models for Kaizen adaptive learning system.

Provides UserProfile and Schedule data classes with validation and serialization.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from validators import (
    validate_username,
    validate_language,
    validate_tone_mode,
    validate_date,
    validate_topic_type,
    validate_quiz_score
)


@dataclass
class UserProfile:
    """
    Represents a user's profile and learning preferences.

    Attributes:
        username: Unique identifier (lowercase, 3-20 chars, alphanumeric + underscore)
        language: Programming language being learned (lowercase)
        tone_mode: Notification personality (playful/motivating/soft/genz)
        start_date: Learning journey start date (YYYY-MM-DD format)
    """
    username: str
    language: str
    tone_mode: str
    start_date: str

    def __post_init__(self):
        """Validate all fields after initialization."""
        # Normalize to lowercase
        self.username = self.username.lower()
        self.language = self.language.lower()
        self.tone_mode = self.tone_mode.lower()

        # Validate each field
        valid, error = validate_username(self.username)
        if not valid:
            raise ValueError(f"Invalid username: {error}")

        valid, error = validate_language(self.language)
        if not valid:
            raise ValueError(f"Invalid language: {error}")

        valid, error = validate_tone_mode(self.tone_mode)
        if not valid:
            raise ValueError(f"Invalid tone_mode: {error}")

        valid, error = validate_date(self.start_date)
        if not valid:
            raise ValueError(f"Invalid start_date: {error}")

    def to_dict(self) -> dict:
        """
        Convert UserProfile to dictionary for JSON serialization.

        Returns:
            Dictionary with username, language, tone_mode, start_date
        """
        return {
            "username": self.username,
            "language": self.language,
            "tone_mode": self.tone_mode,
            "start_date": self.start_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        """
        Create UserProfile instance from dictionary.

        Args:
            data: Dictionary with profile fields

        Returns:
            UserProfile instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        required_fields = ["username", "language", "tone_mode", "start_date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return cls(
            username=data["username"],
            language=data["language"],
            tone_mode=data["tone_mode"],
            start_date=data["start_date"]
        )


@dataclass
class DayEntry:
    """
    Represents a single day's learning entry in the schedule.

    Attributes:
        topic: The topic name (e.g., "Variables", "Functions")
        type: Context type (new_topic/review_topic/completion_milestone/rest_day)
        quiz_score: Score between 0.0-1.0, or None if quiz not taken
    """
    topic: str
    type: str
    quiz_score: Optional[float] = None

    def __post_init__(self):
        """Validate fields after initialization."""
        valid, error = validate_topic_type(self.type)
        if not valid:
            raise ValueError(f"Invalid type: {error}")

        valid, error = validate_quiz_score(self.quiz_score)
        if not valid:
            raise ValueError(f"Invalid quiz_score: {error}")

    def to_dict(self) -> dict:
        """
        Convert DayEntry to dictionary for JSON serialization.

        Returns:
            Dictionary with topic, type, quiz_score
        """
        return {
            "topic": self.topic,
            "type": self.type,
            "quiz_score": self.quiz_score
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DayEntry":
        """
        Create DayEntry instance from dictionary.

        Args:
            data: Dictionary with day entry fields

        Returns:
            DayEntry instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        required_fields = ["topic", "type"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return cls(
            topic=data["topic"],
            type=data["type"],
            quiz_score=data.get("quiz_score", None)
        )


@dataclass
class Schedule:
    """
    Represents a user's learning schedule with day-based topics.

    The schedule is a dictionary with day keys ("day_1", "day_2", etc.)
    mapping to DayEntry objects.

    Attributes:
        days: Dictionary of day_key -> DayEntry mappings
    """
    days: Dict[str, DayEntry] = field(default_factory=dict)

    def add_day(self, day_key: str, topic: str, topic_type: str, quiz_score: Optional[float] = None):
        """
        Add or update a day entry in the schedule.

        Args:
            day_key: Key for the day (e.g., "day_1", "day_2")
            topic: Topic name
            topic_type: Type of topic
            quiz_score: Quiz score (0.0-1.0) or None

        Raises:
            ValueError: If topic_type or quiz_score is invalid
        """
        entry = DayEntry(topic=topic, type=topic_type, quiz_score=quiz_score)
        self.days[day_key] = entry

    def get_day(self, day_key: str) -> Optional[DayEntry]:
        """
        Get a day entry from the schedule.

        Args:
            day_key: Key for the day

        Returns:
            DayEntry if exists, None otherwise
        """
        return self.days.get(day_key)

    def to_dict(self) -> dict:
        """
        Convert Schedule to dictionary for JSON serialization.

        Returns:
            Dictionary with day_key -> day_entry_dict mappings
        """
        return {
            day_key: entry.to_dict()
            for day_key, entry in self.days.items()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Schedule":
        """
        Create Schedule instance from dictionary.

        Args:
            data: Dictionary with day_key -> day_entry_dict mappings

        Returns:
            Schedule instance

        Raises:
            ValueError: If day entries are invalid
        """
        schedule = cls()
        for day_key, day_data in data.items():
            entry = DayEntry.from_dict(day_data)
            schedule.days[day_key] = entry
        return schedule
