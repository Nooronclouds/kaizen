"""
Adaptive learning scheduler that uses ML to dynamically adjust learning paths.

Combines curriculum, user history, and ML predictions to create personalized schedules.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List
import data_manager
from curriculum import get_curriculum, get_topic_by_name, Topic
from ml_model import AdaptiveLearningModel


class AdaptiveScheduler:
    """
    Main scheduler that manages adaptive learning paths using ML predictions.

    Features:
    - Initializes schedules from curriculum
    - Tracks user progress and performance
    - Uses ML model to decide next actions
    - Adapts schedule based on predictions (proceed/review/accelerate)
    """

    def __init__(self, model_path: str = "data/adaptive_model.pkl"):
        """
        Initialize the adaptive scheduler.

        Args:
            model_path: Path to trained ML model
        """
        self.ml_model = AdaptiveLearningModel(model_path=model_path)
        try:
            self.ml_model.load()
        except FileNotFoundError:
            print(f"Warning: ML model not found at {model_path}. Train the model first.")

    def initialize_schedule(self, username: str, language: str, start_date: str) -> bool:
        """
        Initialize a new learning schedule for a user.

        Creates user profile and generates initial schedule from curriculum.

        Args:
            username: User's unique identifier
            language: Programming language to learn
            start_date: Start date in YYYY-MM-DD format

        Returns:
            True if successful

        Raises:
            ValueError: If user creation or curriculum loading fails
        """
        # Create user with default tone_mode
        user_data = data_manager.create_user(username, language, "playful", start_date)

        # Get curriculum for the language
        curriculum = get_curriculum(language)

        # Add first topic to schedule
        first_topic = curriculum[0]
        data_manager.update_schedule(
            username=username,
            day_key="day_1",
            topic=first_topic.name,
            topic_type="new_topic",
            quiz_score=None  # No quiz taken yet
        )

        print(f"Schedule initialized for {username}")
        print(f"Language: {language}")
        print(f"Start date: {start_date}")
        print(f"First topic: {first_topic.name}")

        return True

    def process_quiz_result(
        self,
        username: str,
        current_day_key: str,
        quiz_score: float
    ) -> Dict:
        """
        Process a quiz result and adapt the schedule using ML predictions.

        Args:
            username: User's identifier
            current_day_key: Current day (e.g., "day_5")
            quiz_score: Quiz score (0.0-1.0)

        Returns:
            Dictionary with:
            - action: "proceed", "schedule_review", or "accelerate"
            - next_day_key: Next day identifier
            - next_topic: Next topic name
            - next_type: Next topic type (new_topic/review_topic)
            - probabilities: ML model prediction probabilities

        Raises:
            ValueError: If user doesn't exist or quiz_score invalid
        """
        # Update current day's quiz score
        user_data = data_manager.load_user_data(username)
        if not user_data:
            raise ValueError(f"User {username} not found")

        current_day_data = user_data["schedule"].get(current_day_key)
        if not current_day_data:
            raise ValueError(f"Day {current_day_key} not found in schedule")

        # Update quiz score
        data_manager.update_schedule(
            username=username,
            day_key=current_day_key,
            topic=current_day_data["topic"],
            topic_type=current_day_data["type"],
            quiz_score=quiz_score
        )

        # Extract features for ML prediction
        features = self._extract_features(username, current_day_key)

        # Get ML prediction
        action = self.ml_model.predict(**features)
        probabilities = self.ml_model.predict_proba(**features)

        # Adapt schedule based on action
        next_schedule = self._adapt_schedule(username, current_day_key, action)

        result = {
            "action": action,
            "next_day_key": next_schedule["day_key"],
            "next_topic": next_schedule["topic"],
            "next_type": next_schedule["type"],
            "probabilities": probabilities
        }

        return result

    def _extract_features(self, username: str, current_day_key: str) -> Dict:
        """
        Extract ML model features from user history.

        Features:
        - quiz_score: Latest quiz score
        - topic_difficulty: Current topic difficulty
        - days_since_scheduled: Days spent on current topic
        - user_pace: Overall learning pace

        Args:
            username: User's identifier
            current_day_key: Current day

        Returns:
            Dictionary with feature values
        """
        user_data = data_manager.load_user_data(username)
        schedule = user_data["schedule"]
        current_day_data = schedule[current_day_key]
        language = user_data["profile"]["language"]

        # Feature 1: quiz_score
        quiz_score = current_day_data["quiz_score"]

        # Feature 2: topic_difficulty
        try:
            topic = get_topic_by_name(language, current_day_data["topic"])
            topic_difficulty = topic.difficulty
        except ValueError:
            # Topic not in curriculum, use default
            topic_difficulty = 0.5

        # Feature 3: days_since_scheduled
        # Count how many days this topic has been scheduled (including reviews)
        topic_name = current_day_data["topic"]
        days_since_scheduled = 0
        for day_key, day_data in schedule.items():
            if day_data["topic"] == topic_name:
                days_since_scheduled += 1

        # Feature 4: user_pace
        # Calculate as average quiz score across all completed quizzes
        completed_scores = [
            day_data["quiz_score"]
            for day_data in schedule.values()
            if day_data["quiz_score"] is not None
        ]
        if completed_scores:
            user_pace = sum(completed_scores) / len(completed_scores)
        else:
            user_pace = 0.5  # Default for first quiz

        return {
            "quiz_score": quiz_score,
            "topic_difficulty": topic_difficulty,
            "days_since_scheduled": days_since_scheduled,
            "user_pace": user_pace
        }

    def _adapt_schedule(self, username: str, current_day_key: str, action: str) -> Dict:
        """
        Adapt the schedule based on ML prediction action.

        Actions:
        - proceed: Add next topic from curriculum
        - schedule_review: Schedule current topic again for review
        - accelerate: Skip 1-2 topics ahead

        Args:
            username: User's identifier
            current_day_key: Current day
            action: ML predicted action

        Returns:
            Dictionary with next day info (day_key, topic, type)
        """
        user_data = data_manager.load_user_data(username)
        schedule = user_data["schedule"]
        current_day_data = schedule[current_day_key]
        language = user_data["profile"]["language"]
        curriculum = get_curriculum(language)

        # Get next day number
        current_day_num = int(current_day_key.split("_")[1])
        next_day_num = current_day_num + 1
        next_day_key = f"day_{next_day_num}"

        if action == "schedule_review":
            # Schedule same topic again for review
            next_topic = current_day_data["topic"]
            next_type = "review_topic"

        elif action == "proceed":
            # Move to next topic in curriculum
            current_topic_name = current_day_data["topic"]
            next_topic = self._get_next_topic_in_curriculum(curriculum, current_topic_name)
            next_type = "new_topic"

        elif action == "accelerate":
            # Skip ahead (skip 1 topic)
            current_topic_name = current_day_data["topic"]
            next_topic = self._get_next_topic_in_curriculum(curriculum, current_topic_name, skip=1)
            next_type = "new_topic"

        else:
            raise ValueError(f"Unknown action: {action}")

        # Add to schedule
        data_manager.update_schedule(
            username=username,
            day_key=next_day_key,
            topic=next_topic,
            topic_type=next_type,
            quiz_score=None
        )

        return {
            "day_key": next_day_key,
            "topic": next_topic,
            "type": next_type
        }

    def _get_next_topic_in_curriculum(self, curriculum: List[Topic], current_topic: str, skip: int = 0) -> str:
        """
        Get the next topic in curriculum, optionally skipping some topics.

        Args:
            curriculum: List of Topic objects
            current_topic: Current topic name
            skip: Number of topics to skip (0 = next topic, 1 = skip one, etc.)

        Returns:
            Next topic name
        """
        # Find current topic index
        current_index = None
        for i, topic in enumerate(curriculum):
            if topic.name.lower() == current_topic.lower():
                current_index = i
                break

        if current_index is None:
            # Topic not found, return first topic
            return curriculum[0].name

        # Calculate next index
        next_index = current_index + 1 + skip

        # Check if we've reached the end
        if next_index >= len(curriculum):
            # Return completion milestone
            return "Course Completion Review"

        return curriculum[next_index].name

    def get_current_topic(self, username: str) -> Optional[Dict]:
        """
        Get the current topic the user should be working on.

        Returns the latest day entry in the schedule.

        Args:
            username: User's identifier

        Returns:
            Dictionary with current day info (day_key, topic, type, quiz_score)
            or None if no schedule exists
        """
        schedule = data_manager.get_user_schedule(username)

        if not schedule:
            return None

        # Get the latest day
        day_keys = sorted(schedule.keys(), key=lambda k: int(k.split("_")[1]))
        latest_day_key = day_keys[-1]
        current_day_data = schedule[latest_day_key]

        return {
            "day_key": latest_day_key,
            "topic": current_day_data["topic"],
            "type": current_day_data["type"],
            "quiz_score": current_day_data["quiz_score"]
        }

    def get_progress_summary(self, username: str) -> Dict:
        """
        Get a summary of user's learning progress.

        Args:
            username: User's identifier

        Returns:
            Dictionary with progress statistics
        """
        user_data = data_manager.load_user_data(username)
        if not user_data:
            raise ValueError(f"User {username} not found")

        schedule = user_data["schedule"]
        language = user_data["profile"]["language"]
        curriculum = get_curriculum(language)

        # Calculate statistics
        total_days = len(schedule)
        completed_quizzes = sum(1 for day_data in schedule.values() if day_data["quiz_score"] is not None)
        pending_quizzes = total_days - completed_quizzes

        completed_scores = [
            day_data["quiz_score"]
            for day_data in schedule.values()
            if day_data["quiz_score"] is not None
        ]
        avg_score = sum(completed_scores) / len(completed_scores) if completed_scores else 0.0

        unique_topics = len(set(day_data["topic"] for day_data in schedule.values()))
        review_days = sum(1 for day_data in schedule.values() if day_data["type"] == "review_topic")

        return {
            "total_days": total_days,
            "completed_quizzes": completed_quizzes,
            "pending_quizzes": pending_quizzes,
            "average_score": avg_score,
            "unique_topics_covered": unique_topics,
            "total_topics_in_curriculum": len(curriculum),
            "review_days": review_days
        }


if __name__ == "__main__":
    print("="*60)
    print("Adaptive Scheduler Demo")
    print("="*60 + "\n")

    # Initialize scheduler
    scheduler = AdaptiveScheduler()

    # Create demo user
    demo_username = "demo_adaptive_user"

    # Check if user already exists
    if data_manager.user_exists(demo_username):
        print(f"User {demo_username} already exists. Loading existing data...\n")
    else:
        print("Initializing new schedule...")
        scheduler.initialize_schedule(demo_username, "python", "2025-01-01")
        print()

    # Simulate learning journey
    print("Simulating learning journey with different quiz scores:\n")

    for i in range(1, 6):
        day_key = f"day_{i}"

        current = scheduler.get_current_topic(demo_username)
        print(f"Day {i}: {current['topic']} ({current['type']})")

        # Simulate quiz score (varying performance)
        quiz_scores = [0.9, 0.45, 0.75, 0.95, 0.65]
        quiz_score = quiz_scores[i-1] if i-1 < len(quiz_scores) else 0.8

        print(f"  Quiz Score: {quiz_score}")

        # Process quiz
        result = scheduler.process_quiz_result(demo_username, day_key, quiz_score)

        print(f"  ML Prediction: {result['action']}")
        print(f"  Next: {result['next_topic']} ({result['next_type']})")
        print()

    # Show progress summary
    print("="*60)
    print("Progress Summary:")
    print("="*60)
    summary = scheduler.get_progress_summary(demo_username)
    for key, value in summary.items():
        print(f"{key}: {value}")
