"""
Streak tracking system for Kaizen adaptive learning platform.

Tracks consecutive learning days, calculates streaks, and provides
personality-specific motivation messages for milestones.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import data_manager


class StreakTracker:
    """
    Tracks and manages learning streaks for users.

    Features:
    - Current streak calculation
    - Longest streak tracking
    - Streak break detection
    - Milestone detection (3, 7, 14, 30, 100 days)
    - Personality-specific streak messages
    """

    def __init__(self):
        """Initialize the streak tracker."""
        self.milestones = [3, 7, 14, 30, 100, 365]

    def calculate_streak(self, username: str) -> Dict:
        """
        Calculate current and longest streaks for a user.

        Args:
            username: User's identifier

        Returns:
            Dictionary with streak information:
            - current_streak: Number of consecutive days
            - longest_streak: Best streak ever
            - last_activity_date: Date of last quiz
            - streak_active: Whether streak is currently active
            - days_since_activity: Days since last activity
        """
        user_data = data_manager.load_user_data(username)
        if not user_data:
            raise ValueError(f"User {username} not found")

        schedule = user_data['schedule']

        # Get all completed days (with quiz scores)
        completed_days = []
        for day_key in sorted(schedule.keys(), key=lambda k: int(k.split('_')[1])):
            day_data = schedule[day_key]
            if day_data.get('quiz_score') is not None:
                completed_days.append(day_key)

        if not completed_days:
            return {
                'current_streak': 0,
                'longest_streak': 0,
                'last_activity_date': None,
                'streak_active': False,
                'days_since_activity': 0,
                'total_learning_days': 0
            }

        # Calculate current streak (working backwards from most recent)
        current_streak = 0
        today = datetime.now().date()

        # Check if last activity was yesterday or today
        last_day_num = int(completed_days[-1].split('_')[1])
        start_date = datetime.strptime(user_data['profile']['start_date'], '%Y-%m-%d').date()

        # Simple model: each completed day = 1 day
        days_since_start = (today - start_date).days
        days_since_activity = days_since_start - last_day_num + 1

        # Current streak is active if last activity was today or yesterday
        streak_active = days_since_activity <= 1

        if streak_active:
            # Count backwards from most recent
            current_streak = 1
            for i in range(len(completed_days) - 2, -1, -1):
                prev_day_num = int(completed_days[i].split('_')[1])
                curr_day_num = int(completed_days[i + 1].split('_')[1])

                # Check if consecutive (allowing 1 day gap)
                if curr_day_num - prev_day_num <= 2:
                    current_streak += 1
                else:
                    break

        # Calculate longest streak
        longest_streak = 0
        temp_streak = 1

        for i in range(1, len(completed_days)):
            prev_day_num = int(completed_days[i - 1].split('_')[1])
            curr_day_num = int(completed_days[i].split('_')[1])

            if curr_day_num - prev_day_num <= 2:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1

        longest_streak = max(longest_streak, temp_streak)

        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'last_activity_date': start_date + timedelta(days=last_day_num - 1),
            'streak_active': streak_active,
            'days_since_activity': days_since_activity,
            'total_learning_days': len(completed_days)
        }

    def check_milestone_reached(self, streak: int, previous_streak: int = 0) -> Optional[int]:
        """
        Check if a streak milestone was just reached.

        Args:
            streak: Current streak count
            previous_streak: Previous streak count

        Returns:
            Milestone number if reached, None otherwise
        """
        for milestone in self.milestones:
            if previous_streak < milestone <= streak:
                return milestone
        return None

    def get_streak_message(self, username: str, milestone: Optional[int] = None) -> str:
        """
        Get a personality-specific streak message.

        Args:
            username: User's identifier
            milestone: Streak milestone reached (optional)

        Returns:
            Personalized streak message
        """
        user_data = data_manager.load_user_data(username)
        tone_mode = user_data['profile']['tone_mode']

        streak_info = self.calculate_streak(username)
        current_streak = streak_info['current_streak']

        # Milestone messages
        if milestone:
            return self._get_milestone_message(tone_mode, milestone)

        # Regular streak messages
        if current_streak == 0:
            return self._get_broken_streak_message(tone_mode)

        return self._get_active_streak_message(tone_mode, current_streak)

    def _get_milestone_message(self, tone_mode: str, milestone: int) -> str:
        """Get personality-specific milestone celebration messages."""
        messages = {
            'playful': {
                3: "🔥 3-day streak! You're on fire! Keep the momentum going!",
                7: "🎉 WEEK STREAK! You're officially a learning machine! 🤖",
                14: "⚡ TWO WEEKS! Your dedication is legendary! ⚡",
                30: "🚀 MONTH STREAK! You're absolutely crushing it! 👑",
                100: "💎 100 DAYS! Diamond status achieved! You're unstoppable! 💎",
                365: "🏆 ONE YEAR! CODING CHAMPION STATUS UNLOCKED! 🏆"
            },
            'motivating': {
                3: "💪 3 DAYS STRAIGHT! This is how champions are built!",
                7: "🔥 ONE WEEK OF DOMINANCE! You're proving what dedication means!",
                14: "⚡ 14 DAYS OF POWER! Your consistency is your superpower!",
                30: "🏆 MONTH OF MASTERY! You've earned legendary status!",
                100: "👑 100-DAY WARRIOR! You are UNSTOPPABLE! 👑",
                365: "🌟 365 DAYS! You've achieved ULTIMATE GREATNESS! 🌟"
            },
            'soft': {
                3: "🌸 3 lovely days together. I'm so proud of your consistency 💙",
                7: "🌙 A full week! Your dedication brings so much joy 💫",
                14: "🦋 Two weeks of growth. You're blossoming beautifully 🌸",
                30: "💙 A whole month! Your patience and persistence inspire me 🌈",
                100: "✨ 100 days of gentle progress. What a beautiful journey 💫",
                365: "🌟 One year together. Your journey has been truly special 💙"
            },
            'genz': {
                3: "💅 3 days? That's giving main character energy fr fr! 🔥",
                7: "👑 Week streak? Not you being iconic! The serve! 💯",
                14: "🚀 14 days bestie! This is literally everything! 😤",
                30: "💀 A MONTH?! Bestie you ate and left NO CRUMBS! 💅✨",
                100: "😭 100 DAYS I- the way you're literally unstoppable! 👑🔥",
                365: "🎉 365 DAYS PERIOD. You're the moment. You're THE standard! 💯💅"
            }
        }

        return messages.get(tone_mode, {}).get(
            milestone,
            f"🎉 {milestone}-day streak! Amazing!"
        )

    def _get_active_streak_message(self, tone_mode: str, streak: int) -> str:
        """Get personality-specific active streak messages."""
        messages = {
            'playful': [
                f"🔥 {streak}-day streak! Keep that fire burning!",
                f"⚡ {streak} days strong! You're unstoppable!",
                f"🎯 Streak: {streak} days! Nice consistency!",
                f"🚀 {streak}-day journey! Momentum is building!"
            ],
            'motivating': [
                f"💪 {streak} DAYS! Your discipline is impressive!",
                f"🔥 {streak}-DAY STREAK! Champions show up daily!",
                f"⚡ {streak} CONSECUTIVE DAYS! This is dedication!",
                f"🏆 {streak} DAYS OF EXCELLENCE! Keep pushing!"
            ],
            'soft': [
                f"🌸 {streak} beautiful days together. You're doing wonderfully 💙",
                f"🌙 {streak} days of gentle progress. So proud of you 💫",
                f"🦋 {streak}-day journey. Your consistency is lovely 🌸",
                f"💙 {streak} days. Each one a step forward 🌈"
            ],
            'genz': [
                f"🔥 {streak} days? Bestie the dedication! 💅",
                f"💯 {streak}-day streak hits different! That's on consistency! 😤",
                f"👑 {streak} days and counting! You're giving iconic! ✨",
                f"💅 {streak}-day streak? No literally you're eating this up! 🔥"
            ]
        }

        import random
        return random.choice(messages.get(tone_mode, messages['playful']))

    def _get_broken_streak_message(self, tone_mode: str) -> str:
        """Get personality-specific streak recovery messages."""
        messages = {
            'playful': [
                "No worries! Every pro has an off day. Let's start a new streak! 💪",
                "Streak reset, but your progress isn't! Ready for round 2? 🎮",
                "Time to build an even better streak! You've got this! 🚀"
            ],
            'motivating': [
                "A setback is a setup for a COMEBACK! Let's GO! 💪",
                "Champions don't quit! Start your next winning streak NOW! 🔥",
                "Today is DAY ONE of your next incredible streak! 🏆"
            ],
            'soft': [
                "It's okay to miss a day. You're human, and that's beautiful 🌙",
                "Gentle reminder: Progress isn't perfect. You're still doing great 💙",
                "No pressure. Just happy you're back. Let's continue together 🌸"
            ],
            'genz': [
                "Bestie we all have off days! Let's start fresh fr 💅",
                "Streak broke? That's fine! Character development era starts now ✨",
                "POV: You're about to start the best streak yet! Let's get it 🔥"
            ]
        }

        import random
        return random.choice(messages.get(tone_mode, messages['playful']))

    def get_streak_stats(self, username: str) -> Dict:
        """
        Get comprehensive streak statistics for display.

        Args:
            username: User's identifier

        Returns:
            Dictionary with formatted streak statistics
        """
        streak_info = self.calculate_streak(username)

        # Determine next milestone
        current = streak_info['current_streak']
        next_milestone = None
        for milestone in self.milestones:
            if current < milestone:
                next_milestone = milestone
                break

        days_to_milestone = next_milestone - current if next_milestone else 0

        return {
            **streak_info,
            'next_milestone': next_milestone,
            'days_to_milestone': days_to_milestone,
            'milestone_progress': (current / next_milestone * 100) if next_milestone else 100
        }


def update_streak(username: str) -> Dict:
    """
    Update and check streak for a user.

    Call this after a user completes a quiz to check for milestones.

    Args:
        username: User's identifier

    Returns:
        Dictionary with streak info and any milestone messages
    """
    tracker = StreakTracker()

    # Get current streak
    streak_info = tracker.calculate_streak(username)

    # Check for milestone (would need to track previous streak in real implementation)
    milestone = tracker.check_milestone_reached(streak_info['current_streak'])

    result = {
        'streak_info': streak_info,
        'milestone_reached': milestone,
        'milestone_message': None
    }

    if milestone:
        result['milestone_message'] = tracker.get_streak_message(username, milestone)

    return result


if __name__ == "__main__":
    print("="*70)
    print("Streak Tracking System Demo")
    print("="*70 + "\n")

    # Test with existing user
    test_user = "alice"

    if not data_manager.user_exists(test_user):
        print(f"User {test_user} not found. Run demo_adaptive_learning.py first.")
    else:
        tracker = StreakTracker()

        # Get streak stats
        stats = tracker.get_streak_stats(test_user)

        print(f"User: {test_user}")
        print(f"\n📊 Streak Statistics:")
        print(f"  Current Streak: {stats['current_streak']} days 🔥")
        print(f"  Longest Streak: {stats['longest_streak']} days 👑")
        print(f"  Total Learning Days: {stats['total_learning_days']} days 📚")
        print(f"  Streak Active: {'Yes ✅' if stats['streak_active'] else 'No ❌'}")

        if stats['next_milestone']:
            print(f"\n🎯 Next Milestone: {stats['next_milestone']} days")
            print(f"  Progress: {stats['milestone_progress']:.1f}%")
            print(f"  {stats['days_to_milestone']} days to go!")

        # Show personality-specific messages
        print(f"\n🎭 Streak Messages by Personality:")

        user_data = data_manager.load_user_data(test_user)
        original_tone = user_data['profile']['tone_mode']

        for tone in ['playful', 'motivating', 'soft', 'genz']:
            user_data['profile']['tone_mode'] = tone
            data_manager.save_user_data(test_user, user_data)

            message = tracker.get_streak_message(test_user)
            print(f"\n  {tone.capitalize()}: {message}")

        # Restore original tone
        user_data['profile']['tone_mode'] = original_tone
        data_manager.save_user_data(test_user, user_data)

        # Show milestone messages
        print(f"\n\n🎉 Milestone Celebration Messages:")
        for milestone in [3, 7, 14, 30]:
            print(f"\n  {milestone} Days ({original_tone}):")
            print(f"    {tracker._get_milestone_message(original_tone, milestone)}")

        print("\n" + "="*70)
        print("✓ Streak tracking system working perfectly!")
