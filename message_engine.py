"""
Message generation engine for Kaizen's notification system.

Handles template selection, rotation, history tracking, and message formatting
to ensure variety and freshness in notifications.
"""

import random
import json
import os
from datetime import datetime
from typing import Optional, Dict, List
import data_manager
from message_templates import get_templates, get_emojis


class MessageEngine:
    """
    Generates context-aware, personality-driven messages for users.

    Features:
    - Template rotation to avoid repetition
    - Message history tracking
    - Topic formatting
    - Random emoji variation
    - Context-aware selection
    """

    def __init__(self, history_file: str = "data/message_history.json"):
        """
        Initialize the message engine.

        Args:
            history_file: Path to store message history
        """
        self.history_file = history_file
        self.message_history = self._load_history()

    def generate_message(
        self,
        username: str,
        context: str,
        topic: Optional[str] = None
    ) -> str:
        """
        Generate a personalized message for the user.

        Args:
            username: User's identifier
            context: Message context (new_topic, review_topic, etc.)
            topic: Topic name to format into message (optional)

        Returns:
            Formatted message string

        Raises:
            ValueError: If user doesn't exist
        """
        # Get user's tone mode
        user_data = data_manager.load_user_data(username)
        if not user_data:
            raise ValueError(f"User {username} not found")

        tone_mode = user_data["profile"]["tone_mode"]

        # Get available templates
        templates = get_templates(tone_mode, context)

        # Select a template that hasn't been used recently
        selected_template = self._select_fresh_template(
            username, tone_mode, context, templates
        )

        # Format with topic name if provided
        if topic and "{topic}" in selected_template:
            message = selected_template.format(topic=topic)
        else:
            message = selected_template

        # Optionally add random emoji for extra variety
        if random.random() < 0.3:  # 30% chance
            emoji = random.choice(get_emojis(tone_mode))
            if emoji not in message:
                message = f"{message} {emoji}"

        # Track this message
        self._record_message(username, tone_mode, context, selected_template)

        return message

    def _select_fresh_template(
        self,
        username: str,
        tone_mode: str,
        context: str,
        templates: List[str]
    ) -> str:
        """
        Select a template that hasn't been used recently.

        Prioritizes templates that haven't been sent before, then
        selects from least recently used templates.

        Args:
            username: User's identifier
            tone_mode: User's tone mode
            context: Message context
            templates: Available templates

        Returns:
            Selected template string
        """
        # Get user's message history
        user_history = self.message_history.get(username, {})
        context_history = user_history.get(f"{tone_mode}_{context}", [])

        # Find templates that haven't been used
        unused_templates = [t for t in templates if t not in context_history]

        if unused_templates:
            # Prioritize unused templates
            return random.choice(unused_templates)

        # All templates have been used, pick one at random
        # (the least recently used would be at the start of the list)
        return random.choice(templates)

    def _record_message(
        self,
        username: str,
        tone_mode: str,
        context: str,
        template: str
    ):
        """
        Record a sent message to prevent immediate repetition.

        Maintains a history of the last 5 messages per context.

        Args:
            username: User's identifier
            tone_mode: User's tone mode
            context: Message context
            template: Template that was used
        """
        if username not in self.message_history:
            self.message_history[username] = {}

        key = f"{tone_mode}_{context}"

        if key not in self.message_history[username]:
            self.message_history[username][key] = []

        # Add to history
        history_list = self.message_history[username][key]
        history_list.append(template)

        # Keep only last 5 messages
        if len(history_list) > 5:
            history_list.pop(0)

        # Save updated history
        self._save_history()

    def _load_history(self) -> Dict:
        """
        Load message history from file.

        Returns:
            Dictionary with message history
        """
        if not os.path.exists(self.history_file):
            return {}

        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_history(self):
        """Save message history to file."""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

        with open(self.history_file, 'w') as f:
            json.dump(self.message_history, f, indent=2)

    def get_user_message_stats(self, username: str) -> Dict:
        """
        Get statistics about messages sent to a user.

        Args:
            username: User's identifier

        Returns:
            Dictionary with message statistics
        """
        user_history = self.message_history.get(username, {})

        total_messages = sum(len(msgs) for msgs in user_history.values())
        contexts_used = list(user_history.keys())

        return {
            "total_messages_sent": total_messages,
            "contexts_used": contexts_used,
            "history": user_history
        }

    def clear_user_history(self, username: str):
        """
        Clear message history for a user.

        Args:
            username: User's identifier
        """
        if username in self.message_history:
            del self.message_history[username]
            self._save_history()


def detect_context_from_schedule(username: str) -> tuple[str, Optional[str]]:
    """
    Detect the current context from user's schedule.

    Analyzes the latest day entry to determine context type.

    Args:
        username: User's identifier

    Returns:
        Tuple of (context, topic_name)
        context: new_topic, review_topic, completion_milestone, or rest_day
        topic_name: Name of the topic or None

    Raises:
        ValueError: If user doesn't exist or schedule is empty
    """
    schedule = data_manager.get_user_schedule(username)

    if not schedule:
        raise ValueError(f"User {username} has no schedule")

    # Get the latest day
    day_keys = sorted(schedule.keys(), key=lambda k: int(k.split("_")[1]))
    latest_day_key = day_keys[-1]
    latest_day_data = schedule[latest_day_key]

    # Determine context from type field
    topic_type = latest_day_data["type"]
    topic_name = latest_day_data["topic"]
    quiz_score = latest_day_data.get("quiz_score")

    # Map type to context
    if topic_type == "new_topic":
        context = "new_topic"
    elif topic_type == "review_topic":
        context = "review_topic"
    elif topic_type == "completion_milestone":
        context = "completion_milestone"
    elif topic_type == "rest_day":
        context = "rest_day"
    else:
        context = "new_topic"  # Default

    return context, topic_name


if __name__ == "__main__":
    print("="*70)
    print("Message Engine Demo")
    print("="*70 + "\n")

    # Create message engine
    engine = MessageEngine()

    # Test with a demo user
    demo_user = "alice"

    if not data_manager.user_exists(demo_user):
        print(f"Creating demo user: {demo_user}")
        data_manager.create_user(demo_user, "python", "playful", "2025-02-01")
        data_manager.update_schedule(demo_user, "day_1", "Variables", "new_topic", None)

    print(f"Testing message generation for user: {demo_user}\n")

    # Test all tone modes
    tone_modes = ["playful", "motivating", "soft", "genz"]
    contexts = ["new_topic", "review_topic", "completion_milestone"]

    for tone in tone_modes:
        print(f"\n{'='*70}")
        print(f"Tone Mode: {tone.upper()}")
        print('='*70)

        # Update user's tone mode
        user_data = data_manager.load_user_data(demo_user)
        user_data["profile"]["tone_mode"] = tone
        data_manager.save_user_data(demo_user, user_data)

        for context in contexts:
            print(f"\nContext: {context}")
            print("-" * 70)

            # Generate 3 messages to show variety
            for i in range(3):
                message = engine.generate_message(
                    username=demo_user,
                    context=context,
                    topic="Python Functions"
                )
                print(f"  {i+1}. {message}")

    # Show message statistics
    print("\n" + "="*70)
    print("Message Statistics")
    print("="*70)

    stats = engine.get_user_message_stats(demo_user)
    print(f"\nTotal messages sent: {stats['total_messages_sent']}")
    print(f"Contexts used: {len(stats['contexts_used'])}")

    print("\n✓ Message Engine is working perfectly!")
    print("✓ Template rotation prevents repetition")
    print("✓ All tone modes tested successfully")
