"""
Comprehensive demo of Kaizen's personality-driven notification system.

Shows how the same learning context produces dramatically different messages
based on the user's chosen tone mode.
"""

import data_manager
from notification_service import NotificationService
from scheduler import AdaptiveScheduler


def compare_personalities():
    """
    Compare all four personalities side-by-side across different contexts.
    """
    print("="*80)
    print("KAIZEN PERSONALITY SYSTEM - Comparative Demo")
    print("="*80)
    print("\nThe same learning moment, four completely different personalities!")
    print("Choose the voice that motivates YOU.\n")

    # Initialize services
    service = NotificationService()

    # Test scenarios
    scenarios = [
        {
            "name": "Starting a New Topic",
            "context": "new_topic",
            "topic": "Object-Oriented Programming",
            "emoji": "📚"
        },
        {
            "name": "Reviewing After Struggling",
            "context": "review_topic",
            "topic": "Recursion",
            "emoji": "🔄"
        },
        {
            "name": "Reaching a Milestone",
            "context": "completion_milestone",
            "topic": None,
            "emoji": "🏆"
        },
        {
            "name": "Taking a Rest Day",
            "context": "rest_day",
            "topic": None,
            "emoji": "😌"
        }
    ]

    tone_modes = {
        "playful": {"desc": "Fun and witty", "icon": "😏"},
        "motivating": {"desc": "Energetic and pushing", "icon": "💪"},
        "soft": {"desc": "Gentle and supportive", "icon": "🌙"},
        "genz": {"desc": "Internet culture", "icon": "💅"}
    }

    # Create test users for each tone
    for tone in tone_modes.keys():
        username = f"demo_{tone}"
        if not data_manager.user_exists(username):
            data_manager.create_user(username, "python", tone, "2025-02-01")
            data_manager.update_schedule(username, "day_1", "Variables", "new_topic", 0.8)

    # Compare across all scenarios
    for scenario in scenarios:
        print("\n" + "="*80)
        print(f"{scenario['emoji']} SCENARIO: {scenario['name']}")
        print("="*80 + "\n")

        for tone, info in tone_modes.items():
            username = f"demo_{tone}"

            # Generate message
            from message_engine import MessageEngine
            engine = MessageEngine()
            message = engine.generate_message(
                username=username,
                context=scenario["context"],
                topic=scenario["topic"]
            )

            print(f"{info['icon']} {tone.upper()} ({info['desc']})")
            print(f"   \"{message}\"")
            print()


def show_daily_journey():
    """
    Show how notifications evolve throughout a learning journey.
    """
    print("\n" + "="*80)
    print("📅 A WEEK IN THE LIFE - One Learner's Journey (Playful Mode)")
    print("="*80 + "\n")

    username = "journey_demo"

    # Create user if doesn't exist
    if not data_manager.user_exists(username):
        scheduler = AdaptiveScheduler()
        scheduler.initialize_schedule(username, "python", "2025-02-01")

    service = NotificationService()
    engine = service.message_engine

    # Simulate a week of learning
    week_plan = [
        ("Monday", "new_topic", "Variables"),
        ("Tuesday", "new_topic", "Functions"),
        ("Wednesday", "review_topic", "Functions"),
        ("Thursday", "new_topic", "Lists and Arrays"),
        ("Friday", "new_topic", "Dictionaries"),
        ("Saturday", "rest_day", None),
        ("Sunday", "completion_milestone", None),
    ]

    for day, context, topic in week_plan:
        message = engine.generate_message(
            username=username,
            context=context,
            topic=topic
        )

        context_emoji = {
            "new_topic": "📚",
            "review_topic": "🔄",
            "rest_day": "😴",
            "completion_milestone": "🎉"
        }

        print(f"{context_emoji.get(context, '📌')} {day}: {message}")


def show_tone_personality_guide():
    """
    Show detailed personality guide for choosing a tone mode.
    """
    print("\n" + "="*80)
    print("🎭 PERSONALITY GUIDE - Find Your Perfect Learning Voice")
    print("="*80 + "\n")

    personalities = {
        "playful 😏": {
            "desc": "Fun, witty, and casual",
            "for": "People who learn best with humor and creativity",
            "energy": "Medium-High",
            "example": "Ready to conquer Variables today? Let's make coding look easy! 😎"
        },
        "motivating 💪": {
            "desc": "Energetic, inspirational, and pushing",
            "for": "People who thrive on challenge and achievement",
            "energy": "Very High",
            "example": "Time to dominate Variables! You were born ready! 💪"
        },
        "soft 🌙": {
            "desc": "Gentle, supportive, and calming",
            "for": "People who prefer patience and encouragement",
            "energy": "Low-Medium",
            "example": "Take your time with Variables today. You're doing wonderfully 🌸"
        },
        "genz 💅": {
            "desc": "Internet slang, trending, and relatable",
            "for": "People who connect with internet culture",
            "energy": "High",
            "example": "Variables just dropped and it's giving main character energy 💅"
        }
    }

    for tone, details in personalities.items():
        print(f"{tone}")
        print(f"  What it is: {details['desc']}")
        print(f"  Best for: {details['for']}")
        print(f"  Energy Level: {details['energy']}")
        print(f"  Sample: \"{details['example']}\"")
        print()


if __name__ == "__main__":
    # Run all demos
    compare_personalities()
    show_daily_journey()
    show_tone_personality_guide()

    print("\n" + "="*80)
    print("✨ Kaizen's Personality System - Complete")
    print("="*80)
    print("\nKey Features:")
    print("  ✓ 4 distinct personalities (playful, motivating, soft, genz)")
    print("  ✓ Context-aware messaging (new topic, review, milestone, rest)")
    print("  ✓ Template rotation to prevent repetition")
    print("  ✓ Emoji variation for freshness")
    print("  ✓ 100+ unique message combinations per personality")
    print("\nThe notification engine that makes learning personal! 🚀")
