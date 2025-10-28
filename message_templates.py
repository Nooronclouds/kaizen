"""
Message templates for Kaizen's personality-driven notification system.

Four distinct tone modes with context-aware messaging:
- playful 😏: Fun, witty, casual
- motivating 💪: Energetic, inspirational, pushing
- soft 🌙: Gentle, supportive, calming
- genz 💅: Internet slang, trending, relatable
"""

# Message templates organized by [tone_mode][context]
# Context types: new_topic, review_topic, completion_milestone, rest_day

MESSAGE_TEMPLATES = {
    "playful": {
        "new_topic": [
            "Ready to conquer {topic} today? Let's make coding look easy! 😎",
            "New day, new power-up! Your skill '{topic}' awaits. 💻",
            "Time to unlock {topic}! This is gonna be fun! 🎮",
            "{topic} is calling your name! Answer with some killer code! 📞",
            "Let's turn you into a {topic} wizard today! ✨",
            "Fresh topic alert: {topic}! Time to level up! 🚀",
            "Your brain is ready. {topic} doesn't stand a chance! 🧠",
            "New mission: Master {topic}. Difficulty: Piece of cake! 🍰",
        ],
        "review_topic": [
            "Let's give {topic} another shot. You've got this! 🔁",
            "Review time! {topic} won't know what hit it. 💥",
            "Round 2 with {topic}! Time to show it who's boss! 🥊",
            "Back to {topic} - but this time, you're the expert! 🎯",
            "{topic} deserves another look. Let's nail it this time! 🔨",
            "Rematch with {topic}! Revenge coding time! ⚔️",
            "Double-checking {topic} because excellence matters! ⭐",
            "{topic} part 2: The Return! Let's finish this! 🎬",
        ],
        "completion_milestone": [
            "Boom! You crushed it! 🎉 Take a moment to celebrate!",
            "Level complete! You're officially awesome! 🏆",
            "Achievement unlocked: {topic} Master! Time to celebrate! 🎊",
            "That's a wrap! You just leveled up big time! 📈",
            "Mission accomplished! High five! ✋",
            "You did it! Coding legend status: achieved! 👑",
        ],
        "rest_day": [
            "Rest day! Your brain earned it. Recharge those neurons! 🔋",
            "Taking a break = secret to success. Enjoy! 😴",
            "No coding today! Go do something fun! 🎨",
            "Rest mode activated. Your skills are marinating! 🌟",
            "Day off! Even superheroes need to rest! 🦸",
        ]
    },

    "motivating": {
        "new_topic": [
            "Time to dominate {topic}! You were born ready! 💪",
            "Let's attack {topic} with everything you've got! 🔥",
            "{topic} is your mountain. Today, you climb! 🏔️",
            "Channel your inner champion. {topic} doesn't stand a chance! 🏆",
            "Greatness awaits! {topic} is just the beginning! ⚡",
            "You're unstoppable! Show {topic} what you're made of! 💯",
            "Today's goal: Crush {topic}. You CAN and you WILL! 🎯",
            "Your potential is unlimited! Let's conquer {topic}! 🚀",
        ],
        "review_topic": [
            "Champions review and improve! {topic} round 2! 💪",
            "Growth happens in the review! Let's master {topic}! 📈",
            "Persistence beats resistance! {topic} is yours! 🔥",
            "Strong people revisit! {topic} won't beat you! 💯",
            "Every master was once a beginner. Review {topic} like a pro! 🏆",
            "This is how winners are made! {topic} revision time! ⚡",
            "You're getting stronger! {topic} review = success! 💪",
            "Dedication pays off! Let's perfect {topic} today! 🎯",
        ],
        "completion_milestone": [
            "INCREDIBLE! You just proved what dedication looks like! 🏆",
            "VICTORY! Your hard work paid off magnificently! 🎉",
            "You are UNSTOPPABLE! Celebrate this massive win! 💪",
            "What an achievement! You earned every bit of this! ⭐",
            "POWERFUL! You just leveled up your entire future! 🚀",
            "Outstanding! This is just the beginning of your greatness! 💯",
        ],
        "rest_day": [
            "Even champions rest! Recharge for tomorrow's victories! 🔋",
            "Rest is training! Your mind is getting stronger! 💪",
            "Smart people rest strategically. That's you! 🧠",
            "Taking a break is productive! Enjoy it! 🌟",
            "Rest today, conquer tomorrow! You've earned it! 😌",
        ]
    },

    "soft": {
        "new_topic": [
            "Good morning ☀️ Today's gentle adventure: {topic}",
            "Take your time with {topic} today. You're doing wonderfully 🌸",
            "No rush! Let's explore {topic} together at your pace 🌙",
            "{topic} awaits you. Remember, every step counts 🦋",
            "Today's journey: {topic}. Be kind to yourself as you learn 💫",
            "Hello! Ready to discover {topic}? Go at your own speed 🌻",
            "A new chapter: {topic}. You're exactly where you need to be 🍃",
            "Gentle reminder: {topic} is today's focus. You've got this 🌈",
        ],
        "review_topic": [
            "Let's revisit {topic} with fresh eyes. Learning takes time 🌙",
            "It's okay to review! {topic} will make more sense now 🌸",
            "Back to {topic}, and that's perfectly fine. Progress isn't linear 💙",
            "Taking another look at {topic}. This is how real learning happens 🦋",
            "Gentle review of {topic}. You're growing at your own pace 🌱",
            "Revisiting {topic} shows wisdom, not weakness 💫",
            "{topic} review time. Be patient with yourself 🌻",
            "It's natural to need more time with {topic}. Take what you need 🍃",
        ],
        "completion_milestone": [
            "You did it! So proud of your journey 🌟",
            "What a beautiful achievement. You should feel wonderful 🌸",
            "Completed! Take a moment to appreciate how far you've come 💙",
            "You reached this milestone through persistence and care 🦋",
            "Congratulations! Your gentle persistence paid off 🌈",
            "This moment is yours. You earned it through patience 💫",
        ],
        "rest_day": [
            "Rest day. Your mind and body will thank you 🌙",
            "Taking a break is an act of self-care. Enjoy it 🌸",
            "No studying today. Just breathe and relax 💙",
            "Rest well. Learning happens in the quiet moments too 🦋",
            "Today is for you. No coding, just peace ☮️",
        ]
    },

    "genz": {
        "new_topic": [
            "{topic} just dropped and it's giving main character energy 💅",
            "POV: You're about to absolutely slay {topic} 😤",
            "{topic} era starts now. Let's get this bread 🍞",
            "New {topic} content just unlocked. It's giving genius 🧠",
            "Not me being obsessed with {topic} already 💀",
            "{topic} hit different today. Let's gooo! 🔥",
            "The way {topic} is about to be your new personality trait ✨",
            "New topic alert: {topic}. No literally, it's iconic 👑",
        ],
        "review_topic": [
            "Back to {topic} but make it ✨revenge era✨ 💅",
            "{topic} review? More like glow-up arc 📈",
            "Returning to {topic} and we're not gatekeeping this time 😤",
            "POV: You're fixing your {topic} villain origin story 💀",
            "{topic} comeback tour. This is the one fr fr 🔥",
            "Round 2 with {topic} hits different when you understand it 🧠",
            "{topic} but this time we're the main character ✨",
            "Review {topic}? Bestie that's called character development 💯",
        ],
        "completion_milestone": [
            "STOP IT RIGHT NOW you literally just- 😭💀🎉",
            "Not you being iconic and completing this!! 💅✨",
            "The serve!! The talent!! The everything!! 👑",
            "And THAT'S on learning and periodt! 💯🔥",
            "You ate and left no crumbs. Period. 😤✨",
            "This is giving winner energy and I'm here for it! 🎊",
        ],
        "rest_day": [
            "Rest day = self care era. It's giving main character 💅",
            "No cap, taking breaks is literally so smart 🧠",
            "Day off vibes. Touch grass, bestie 🌱✨",
            "Rest day supremacy. We love to see it 😌",
            "POV: You understand that rest = productivity 💯",
        ]
    }
}


# Emoji collections for each tone mode (for additional variation)
TONE_EMOJIS = {
    "playful": ["😎", "🎮", "🚀", "✨", "💻", "🎯", "🔥", "💡", "⚡", "🎨"],
    "motivating": ["💪", "🔥", "⚡", "🏆", "💯", "🎯", "📈", "🚀", "💥", "⭐"],
    "soft": ["🌙", "🌸", "💙", "🦋", "🌈", "💫", "🌻", "🍃", "☮️", "🌱"],
    "genz": ["💅", "💀", "😤", "✨", "🔥", "👑", "💯", "🧠", "🍞", "📈"]
}


def get_contexts():
    """Get list of all available context types."""
    return ["new_topic", "review_topic", "completion_milestone", "rest_day"]


def get_tone_modes():
    """Get list of all available tone modes."""
    return list(MESSAGE_TEMPLATES.keys())


def get_templates(tone_mode: str, context: str) -> list:
    """
    Get message templates for a specific tone mode and context.

    Args:
        tone_mode: One of playful, motivating, soft, genz
        context: One of new_topic, review_topic, completion_milestone, rest_day

    Returns:
        List of message template strings

    Raises:
        ValueError: If tone_mode or context is invalid
    """
    if tone_mode not in MESSAGE_TEMPLATES:
        raise ValueError(f"Invalid tone_mode: {tone_mode}. Must be one of {get_tone_modes()}")

    if context not in MESSAGE_TEMPLATES[tone_mode]:
        raise ValueError(f"Invalid context: {context}. Must be one of {get_contexts()}")

    return MESSAGE_TEMPLATES[tone_mode][context]


def get_emojis(tone_mode: str) -> list:
    """
    Get emoji collection for a tone mode.

    Args:
        tone_mode: One of playful, motivating, soft, genz

    Returns:
        List of emoji strings

    Raises:
        ValueError: If tone_mode is invalid
    """
    if tone_mode not in TONE_EMOJIS:
        raise ValueError(f"Invalid tone_mode: {tone_mode}")

    return TONE_EMOJIS[tone_mode]
