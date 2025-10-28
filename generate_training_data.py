"""
Generate synthetic training data for the adaptive learning ML model.

Creates realistic training examples based on common learning patterns.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple


def generate_synthetic_data(n_samples: int = 1000) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic training data for the ML model.

    The model predicts next action based on:
    - quiz_score: 0.0 to 1.0 (quiz performance)
    - topic_difficulty: 0.0 to 1.0 (how hard the topic is)
    - days_since_scheduled: integer (days since topic was first scheduled)
    - user_pace: 0.0 to 1.0 (overall learning speed, higher = faster)

    Actions:
    - proceed: Move to next topic (good performance)
    - schedule_review: Review this topic again (poor performance)
    - accelerate: Skip ahead faster (excellent performance on easy topics)

    Args:
        n_samples: Number of training examples to generate

    Returns:
        Tuple of (features_df, labels_series)
    """
    np.random.seed(42)

    features = []
    labels = []

    for _ in range(n_samples):
        # Generate random features
        quiz_score = np.random.uniform(0.0, 1.0)
        topic_difficulty = np.random.uniform(0.0, 1.0)
        days_since_scheduled = np.random.randint(0, 8)
        user_pace = np.random.uniform(0.3, 1.0)

        # Decision logic based on realistic learning patterns
        action = _determine_action(quiz_score, topic_difficulty, days_since_scheduled, user_pace)

        features.append([quiz_score, topic_difficulty, days_since_scheduled, user_pace])
        labels.append(action)

    # Create DataFrame
    feature_names = ['quiz_score', 'topic_difficulty', 'days_since_scheduled', 'user_pace']
    X = pd.DataFrame(features, columns=feature_names)
    y = pd.Series(labels, name='action')

    return X, y


def _determine_action(
    quiz_score: float,
    topic_difficulty: float,
    days_since_scheduled: int,
    user_pace: float
) -> str:
    """
    Determine the appropriate action based on learning patterns.

    Learning patterns:
    1. High quiz score (>0.8) on any topic → proceed
    2. Very high score (>0.9) on easy topic (<0.5 difficulty) → accelerate
    3. Low quiz score (<0.5) → schedule_review
    4. Medium score (0.5-0.8) on hard topic (>0.7 difficulty) → proceed if fast pace, else review
    5. Multiple days on same topic (>3 days) with medium score → proceed (avoid getting stuck)
    6. Fast learner (pace >0.8) with decent score (>0.7) → accelerate

    Args:
        quiz_score: Quiz performance (0.0-1.0)
        topic_difficulty: Topic difficulty (0.0-1.0)
        days_since_scheduled: Days spent on this topic
        user_pace: User's overall learning pace (0.0-1.0)

    Returns:
        Action string: "proceed", "schedule_review", or "accelerate"
    """
    # Pattern 1: Excellent performance → proceed
    if quiz_score > 0.85:
        # Pattern 2: Excellent on easy topic → accelerate
        if topic_difficulty < 0.5 and user_pace > 0.7:
            return "accelerate"
        return "proceed"

    # Pattern 3: Poor performance → review
    if quiz_score < 0.5:
        return "schedule_review"

    # Pattern 4: Stuck too long → proceed (avoid infinite reviews)
    if days_since_scheduled > 3 and quiz_score > 0.6:
        return "proceed"

    # Pattern 5: Fast learner with good score → accelerate
    if user_pace > 0.8 and quiz_score > 0.75:
        return "accelerate"

    # Pattern 6: Medium score on hard topic
    if quiz_score >= 0.65 and topic_difficulty > 0.7:
        if user_pace > 0.6:
            return "proceed"
        else:
            return "schedule_review"

    # Pattern 7: Medium score overall
    if quiz_score >= 0.6:
        return "proceed"

    # Default: needs more practice
    return "schedule_review"


def save_training_data(filepath: str = "data/training_data.csv"):
    """
    Generate and save training data to CSV file.

    Args:
        filepath: Path where CSV file should be saved
    """
    import os

    X, y = generate_synthetic_data(n_samples=1000)

    # Combine features and labels
    data = X.copy()
    data['action'] = y

    # Create directory if needed
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Save to CSV
    data.to_csv(filepath, index=False)
    print(f"Training data saved to {filepath}")
    print(f"Total samples: {len(data)}")
    print(f"\nAction distribution:")
    print(data['action'].value_counts())


if __name__ == "__main__":
    # Generate and display sample data
    print("Generating synthetic training data...\n")

    X, y = generate_synthetic_data(n_samples=1000)

    print("Feature columns:", list(X.columns))
    print(f"\nGenerated {len(X)} training examples")
    print(f"\nAction distribution:")
    print(y.value_counts())
    print(f"\nSample data (first 5 rows):")
    sample = X.head()
    sample['action'] = y.head()
    print(sample)

    # Save to file
    print("\n" + "="*50)
    save_training_data()
