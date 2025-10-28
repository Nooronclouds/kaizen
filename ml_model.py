"""
Machine learning model for adaptive learning schedule predictions.

Uses Random Forest classifier to decide next actions based on user performance.
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from typing import Tuple, Optional


class AdaptiveLearningModel:
    """
    ML model that predicts the next learning action based on user performance.

    Features:
    - quiz_score: Quiz performance (0.0-1.0)
    - topic_difficulty: Topic difficulty rating (0.0-1.0)
    - days_since_scheduled: Days spent on current topic
    - user_pace: Overall learning speed (0.0-1.0)

    Actions:
    - proceed: Move to next topic
    - schedule_review: Review current topic again
    - accelerate: Skip ahead faster (for fast learners)
    """

    def __init__(self, model_path: str = "data/adaptive_model.pkl"):
        """
        Initialize the adaptive learning model.

        Args:
            model_path: Path to save/load the trained model
        """
        self.model_path = model_path
        self.model: Optional[RandomForestClassifier] = None
        self.feature_names = ['quiz_score', 'topic_difficulty', 'days_since_scheduled', 'user_pace']
        self.action_labels = ['proceed', 'schedule_review', 'accelerate']

    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> dict:
        """
        Train the Random Forest classifier.

        Args:
            X: Feature DataFrame
            y: Target Series (actions)
            test_size: Proportion of data for testing

        Returns:
            Dictionary with training metrics (accuracy, classification report)
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Initialize Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'  # Handle class imbalance
        )

        # Train model
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        metrics = {
            'accuracy': accuracy,
            'classification_report': report,
            'train_size': len(X_train),
            'test_size': len(X_test)
        }

        return metrics

    def predict(
        self,
        quiz_score: float,
        topic_difficulty: float,
        days_since_scheduled: int,
        user_pace: float
    ) -> str:
        """
        Predict the next action for a user based on current performance.

        Args:
            quiz_score: Latest quiz score (0.0-1.0)
            topic_difficulty: Current topic difficulty (0.0-1.0)
            days_since_scheduled: Days since topic was scheduled
            user_pace: User's overall learning pace (0.0-1.0)

        Returns:
            Predicted action: "proceed", "schedule_review", or "accelerate"

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.model is None:
            raise ValueError("Model must be trained before making predictions")

        # Create feature array
        features = np.array([[quiz_score, topic_difficulty, days_since_scheduled, user_pace]])

        # Predict
        prediction = self.model.predict(features)[0]

        return prediction

    def predict_proba(
        self,
        quiz_score: float,
        topic_difficulty: float,
        days_since_scheduled: int,
        user_pace: float
    ) -> dict:
        """
        Get prediction probabilities for all actions.

        Args:
            quiz_score: Latest quiz score (0.0-1.0)
            topic_difficulty: Current topic difficulty (0.0-1.0)
            days_since_scheduled: Days since topic was scheduled
            user_pace: User's overall learning pace (0.0-1.0)

        Returns:
            Dictionary mapping actions to probabilities

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.model is None:
            raise ValueError("Model must be trained before making predictions")

        # Create feature array
        features = np.array([[quiz_score, topic_difficulty, days_since_scheduled, user_pace]])

        # Get probabilities
        probabilities = self.model.predict_proba(features)[0]

        # Map to action names
        result = {}
        for action, prob in zip(self.model.classes_, probabilities):
            result[action] = float(prob)

        return result

    def save(self):
        """
        Save the trained model to disk.

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.model is None:
            raise ValueError("Cannot save untrained model")

        # Create directory if needed
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)

        print(f"Model saved to {self.model_path}")

    def load(self):
        """
        Load a trained model from disk.

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)

        print(f"Model loaded from {self.model_path}")

    def get_feature_importance(self) -> dict:
        """
        Get feature importance scores from the trained model.

        Returns:
            Dictionary mapping feature names to importance scores

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.model is None:
            raise ValueError("Model must be trained first")

        importances = self.model.feature_importances_
        return {feature: float(importance) for feature, importance in zip(self.feature_names, importances)}


def train_and_save_model(data_path: str = "data/training_data.csv", model_path: str = "data/adaptive_model.pkl"):
    """
    Train the adaptive learning model and save it to disk.

    Args:
        data_path: Path to training data CSV
        model_path: Path to save trained model

    Returns:
        Tuple of (model, metrics)
    """
    # Load training data
    print(f"Loading training data from {data_path}...")
    data = pd.read_csv(data_path)

    X = data[['quiz_score', 'topic_difficulty', 'days_since_scheduled', 'user_pace']]
    y = data['action']

    print(f"Training data: {len(data)} samples")
    print(f"Action distribution:\n{y.value_counts()}\n")

    # Train model
    print("Training Random Forest model...")
    model = AdaptiveLearningModel(model_path=model_path)
    metrics = model.train(X, y)

    print(f"\nModel trained successfully!")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"\nFeature Importance:")
    for feature, importance in model.get_feature_importance().items():
        print(f"  {feature}: {importance:.4f}")

    # Save model
    model.save()

    return model, metrics


if __name__ == "__main__":
    # Train and save the model
    print("="*60)
    print("Training Adaptive Learning Model")
    print("="*60 + "\n")

    model, metrics = train_and_save_model()

    print("\n" + "="*60)
    print("Testing model predictions:")
    print("="*60)

    # Test predictions
    test_cases = [
        {
            "quiz_score": 0.9,
            "topic_difficulty": 0.3,
            "days_since_scheduled": 1,
            "user_pace": 0.8,
            "expected": "accelerate"
        },
        {
            "quiz_score": 0.4,
            "topic_difficulty": 0.7,
            "days_since_scheduled": 1,
            "user_pace": 0.5,
            "expected": "schedule_review"
        },
        {
            "quiz_score": 0.75,
            "topic_difficulty": 0.5,
            "days_since_scheduled": 1,
            "user_pace": 0.6,
            "expected": "proceed"
        }
    ]

    for i, case in enumerate(test_cases, 1):
        prediction = model.predict(
            case["quiz_score"],
            case["topic_difficulty"],
            case["days_since_scheduled"],
            case["user_pace"]
        )
        probs = model.predict_proba(
            case["quiz_score"],
            case["topic_difficulty"],
            case["days_since_scheduled"],
            case["user_pace"]
        )

        print(f"\nTest Case {i}:")
        print(f"  Quiz Score: {case['quiz_score']}, Difficulty: {case['topic_difficulty']}")
        print(f"  Days: {case['days_since_scheduled']}, Pace: {case['user_pace']}")
        print(f"  Expected: {case['expected']}")
        print(f"  Predicted: {prediction}")
        print(f"  Probabilities: {probs}")

    print("\n" + "="*60)
    print("Model training complete!")
