# Streak Tracking & Daily Reminders Guide 🔥

Complete documentation for Kaizen's streak tracking and daily reminder systems.

## Overview

The streak and reminder systems work together to boost user engagement and retention:

- **Streak Tracking**: Gamifies consistency by rewarding consecutive learning days
- **Daily Reminders**: Automated notifications to encourage daily practice
- **Personality Integration**: All messages adapt to user's chosen tone

## Streak Tracking System

### Features

**📊 Comprehensive Tracking**
- Current streak (consecutive days)
- Longest streak (personal best)
- Total learning days
- Last activity date
- Days since last activity

**🎯 Milestone System**
- 3 days: First milestone
- 7 days: Week streak
- 14 days: Two weeks
- 30 days: Month streak
- 100 days: Century club
- 365 days: Year achievement

**🎭 Personality-Driven Messages**
- Custom celebration messages for each milestone
- Tone-specific streak maintenance messages
- Encouraging recovery messages for broken streaks

### How It Works

**Streak Calculation Logic:**
1. Counts consecutive days with completed quizzes
2. Allows 1-day gaps (rest days)
3. Updates automatically after each quiz
4. Tracks both current and all-time longest streaks

**Active Streak Rules:**
- Must have activity today or yesterday
- Consecutive days count toward streak
- Missing 2+ days breaks the streak
- Streak resets but progress remains

### Usage Examples

**In Python Code:**

```python
from streak_tracker import StreakTracker, update_streak

# Initialize tracker
tracker = StreakTracker()

# Get streak statistics
stats = tracker.get_streak_stats("username")
print(f"Current streak: {stats['current_streak']} days")
print(f"Longest streak: {stats['longest_streak']} days")
print(f"Next milestone: {stats['next_milestone']} days")

# Check for milestones after quiz
result = update_streak("username")
if result['milestone_reached']:
    print(result['milestone_message'])

# Get personality-specific message
message = tracker.get_streak_message("username")
print(message)
```

**In Web Dashboard:**

The dashboard automatically displays:
- Large animated streak counter with 🔥 icon
- Active/inactive streak status
- Longest streak achievement (👑)
- Next milestone goal (🎯)
- Progress toward next milestone

### Milestone Messages by Personality

**3-Day Milestone:**
- **Playful**: "🔥 3-day streak! You're on fire! Keep the momentum going!"
- **Motivating**: "💪 3 DAYS STRAIGHT! This is how champions are built!"
- **Soft**: "🌸 3 lovely days together. I'm so proud of your consistency 💙"
- **Genz**: "💅 3 days? That's giving main character energy fr fr! 🔥"

**7-Day Milestone:**
- **Playful**: "🎉 WEEK STREAK! You're officially a learning machine! 🤖"
- **Motivating**: "🔥 ONE WEEK OF DOMINANCE! You're proving what dedication means!"
- **Soft**: "🌙 A full week! Your dedication brings so much joy 💫"
- **Genz**: "👑 Week streak? Not you being iconic! The serve! 💯"

**30-Day Milestone:**
- **Playful**: "🚀 MONTH STREAK! You're absolutely crushing it! 👑"
- **Motivating**: "🏆 MONTH OF MASTERY! You've earned legendary status!"
- **Soft**: "💙 A whole month! Your patience and persistence inspire me 🌈"
- **Genz**: "💀 A MONTH?! Bestie you ate and left NO CRUMBS! 💅✨"

## Daily Reminder System

### Features

**⏰ Flexible Scheduling**
- Customizable reminder times per user
- Automatic daily notifications
- Background thread execution
- Time zone aware

**🎯 Smart Content**
- Streak-aware messages
- Context detection from schedule
- Personality-driven content
- Avoids repetition

**🔔 Notification Methods**
- Desktop notifications (plyer)
- System tray integration
- Graceful fallback to console
- Cross-platform support

### How It Works

**Scheduling Process:**
1. User sets preferred reminder time (e.g., 9:00 AM)
2. Scheduler creates daily job for that time
3. Background thread runs continuously
4. At specified time, notification is sent
5. Message adapts to current streak and context

**Message Selection:**
- If active streak: Includes streak count and motivation
- If broken streak: Encouraging recovery message
- If new topic: Context-aware notification
- Always respects user's personality tone

### Usage Examples

**Basic Setup:**

```python
from daily_reminders import DailyReminderScheduler, schedule_daily_notifications

# Simple: Schedule all users at 9 AM
scheduler = schedule_daily_notifications("09:00")

# Start background service
scheduler.start_scheduler()

# (Runs continuously in background)
```

**Advanced Usage:**

```python
# Initialize scheduler
scheduler = DailyReminderScheduler()

# Schedule specific user
scheduler.schedule_user_reminder("alice", "09:00")
scheduler.schedule_user_reminder("bob", "20:00")  # 8 PM

# Schedule all existing users
scheduler.schedule_all_users("09:00")

# Start the scheduler
scheduler.start_scheduler()

# Check scheduled jobs
jobs = scheduler.list_scheduled_jobs()
for job in jobs:
    print(f"User: {job['tags']}, Next: {job['next_run']}")

# Get next reminder for user
next_time = scheduler.get_next_reminder_time("alice")
print(f"Next reminder: {next_time}")

# Remove reminder
scheduler.remove_user_reminder("alice")

# Stop scheduler when done
scheduler.stop_scheduler()
```

**Integration with Web App:**

Add to your Flask app startup:

```python
# In app.py or separate service file
from daily_reminders import DailyReminderScheduler

# Initialize on app start
reminder_scheduler = DailyReminderScheduler()
reminder_scheduler.schedule_all_users("09:00")
reminder_scheduler.start_scheduler()

# Add route for users to customize time
@app.route('/settings/reminders', methods=['POST'])
def update_reminders():
    time = request.form.get('reminder_time')
    username = get_current_user()

    scheduler.remove_user_reminder(username)
    scheduler.schedule_user_reminder(username, time)

    flash(f'Reminder set for {time}', 'success')
    return redirect(url_for('settings'))
```

## Integration Points

### Web Dashboard

**Visual Display:**
- Prominent streak card with animated fire icon
- Active/inactive status indicator
- Milestone progress bar
- Personal best display

**Location:** Above stats grid on dashboard

### Progress Page

Add streak timeline visualization:

```python
# In app.py progress route
streak_history = []
for day in schedule_timeline:
    if day['completed']:
        # Calculate streak at that point
        pass
```

### Quiz Completion

Auto-check for milestones:

```python
# After quiz submission in app.py
from streak_tracker import update_streak

result = update_streak(username)
if result['milestone_reached']:
    flash(result['milestone_message'], 'success')
```

### Settings Page

Add reminder configuration:

```html
<form method="POST" action="/settings/reminders">
    <label>Daily Reminder Time:</label>
    <input type="time" name="reminder_time" value="09:00">
    <button>Save</button>
</form>
```

## Gamification Features

### Streak Challenges

**Create Challenge System:**

```python
def create_streak_challenge(username, target_days, reward):
    """
    Create a streak challenge for a user.

    Args:
        username: User identifier
        target_days: Goal streak length
        reward: Badge/title to award
    """
    # Track challenge progress
    # Award on completion
    pass
```

### Leaderboard

**Top Streakers:**

```python
def get_streak_leaderboard(limit=10):
    """
    Get users with longest current streaks.

    Returns list of {username, streak, personality}
    """
    all_users = get_all_usernames()
    leaderboard = []

    for user in all_users:
        stats = tracker.get_streak_stats(user)
        leaderboard.append({
            'username': user,
            'streak': stats['current_streak'],
            'longest': stats['longest_streak']
        })

    return sorted(leaderboard, key=lambda x: x['streak'], reverse=True)[:limit]
```

### Streak Recovery

**Freeze System:**

```python
def use_streak_freeze(username):
    """
    Allow user to preserve streak for 1 day.

    Useful for planned breaks or emergencies.
    Only 1 freeze per month.
    """
    # Check if freeze available
    # Apply freeze to streak calculation
    pass
```

## Best Practices

### Streak Tracking

1. **Update After Each Quiz**: Call `update_streak()` after quiz completion
2. **Check Milestones**: Always check for milestone messages
3. **Display Prominently**: Streak should be visible on main dashboard
4. **Celebrate Achievements**: Show milestone messages with fanfare
5. **Encourage Recovery**: Be supportive when streaks break

### Daily Reminders

1. **Respect Time Zones**: Store and use user's local time
2. **Allow Customization**: Let users set preferred times
3. **Don't Spam**: One reminder per day maximum
4. **Make it Easy to Disable**: Provide opt-out option
5. **Test Notifications**: Verify platform compatibility

### User Experience

1. **Positive Reinforcement**: Focus on progress, not punishment
2. **Personality Consistency**: Match tone in all messages
3. **Clear Goals**: Show next milestone clearly
4. **Visual Feedback**: Use animations and colors
5. **Social Proof**: Show community streaks (optional)

## Technical Details

### Data Storage

**Streak calculation is derived from existing data:**
- No new database fields required
- Calculated from quiz completion dates
- Cached for performance (optional)

**Reminder preferences (future enhancement):**
```json
{
  "profile": {
    "username": "alice",
    "language": "python",
    "tone_mode": "playful",
    "start_date": "2025-01-01",
    "reminder_time": "09:00",
    "reminders_enabled": true
  }
}
```

### Dependencies

```txt
schedule>=1.2.0  # For reminder scheduling
```

### Performance Considerations

**Streak Calculation:**
- O(n) where n = number of completed days
- Cache results for current streak
- Recalculate only when needed

**Reminder Scheduler:**
- Single background thread
- Minimal CPU usage (checks every minute)
- Graceful shutdown on app stop

## Troubleshooting

### Streaks Not Updating

**Problem:** Streak count doesn't increase after quiz

**Solutions:**
1. Verify quiz was completed (score saved)
2. Check date calculations
3. Ensure consecutive days logic
4. Review day gap allowance

### Reminders Not Sending

**Problem:** No notifications received

**Solutions:**
1. Check if scheduler is running (`scheduler.running`)
2. Verify notification permissions on OS
3. Check scheduled jobs (`list_scheduled_jobs()`)
4. Test plyer notification manually
5. Check console for fallback messages

### Wrong Streak Count

**Problem:** Streak shows incorrect number

**Solutions:**
1. Verify quiz completion dates in schedule
2. Check for timezone issues
3. Review consecutive day logic
4. Test calculation manually with sample data

## Future Enhancements

**Potential Features:**
- [ ] Streak freeze tokens (preserve streak for 1 day)
- [ ] Weekly challenges with bonus rewards
- [ ] Streak sharing on social media
- [ ] Streak recovery suggestions
- [ ] Multi-day streak predictions
- [ ] Community streak leaderboards
- [ ] Streak milestone badges/trophies
- [ ] Email reminders as backup
- [ ] SMS notifications (Twilio integration)
- [ ] Smart reminder timing (ML-based)

## API Reference

### StreakTracker Class

```python
tracker = StreakTracker()

# Calculate current streak
stats = tracker.calculate_streak(username: str) -> Dict

# Get formatted stats for display
stats = tracker.get_streak_stats(username: str) -> Dict

# Check if milestone reached
milestone = tracker.check_milestone_reached(
    streak: int,
    previous_streak: int
) -> Optional[int]

# Get personality message
message = tracker.get_streak_message(
    username: str,
    milestone: Optional[int]
) -> str
```

### DailyReminderScheduler Class

```python
scheduler = DailyReminderScheduler()

# Schedule single user
scheduler.schedule_user_reminder(username: str, time: str)

# Schedule all users
scheduler.schedule_all_users(default_time: str)

# Remove user reminder
scheduler.remove_user_reminder(username: str)

# List scheduled jobs
jobs = scheduler.list_scheduled_jobs() -> List[Dict]

# Start/stop scheduler
scheduler.start_scheduler()
scheduler.stop_scheduler()

# Get next reminder time
next_time = scheduler.get_next_reminder_time(username: str) -> datetime
```

### Helper Functions

```python
# Update and check streak after quiz
result = update_streak(username: str) -> Dict

# Schedule all users quickly
scheduler = schedule_daily_notifications(time: str) -> DailyReminderScheduler
```

## Examples Gallery

### Streak Display Variations

**Active 5-Day Streak (Playful):**
```
🔥 5 Day Streak
Active 🔥

👑 Longest: 12 days
🎯 Next goal: 7 days
```

**Broken Streak (Soft):**
```
🔥 0 Day Streak
Start a new streak!

👑 Longest: 8 days
🎯 Next goal: 3 days

"It's okay to miss a day. You're human, and that's beautiful 🌙"
```

**Milestone Achieved (Genz):**
```
🎉 You've reached 30 days!

"💀 A MONTH?! Bestie you ate and left NO CRUMBS! 💅✨"
```

---

**Built with motivation, consistency, and personality! 🔥**

Version: 1.0.0
Last Updated: 2025-10-28
