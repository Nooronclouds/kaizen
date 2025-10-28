"""
Flask web application for Kaizen adaptive learning system.

Provides a complete web interface for users to:
- Onboard and set preferences
- View daily learning topics
- Take quizzes
- Track progress
- Adjust settings
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import secrets
from datetime import datetime

# Import Kaizen modules
import data_manager
from scheduler import AdaptiveScheduler
from notification_service import NotificationService
from message_engine import detect_context_from_schedule
from curriculum import get_supported_languages, get_curriculum
from streak_tracker import StreakTracker

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize services
scheduler = AdaptiveScheduler()
notification_service = NotificationService()
streak_tracker = StreakTracker()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_user():
    """Get current user from session."""
    return session.get('username')


def require_login(f):
    """Decorator to require login for routes."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            flash('Please log in first.', 'warning')
            return redirect(url_for('landing'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def landing():
    """Landing page."""
    # If already logged in, go to dashboard
    if get_current_user():
        return redirect(url_for('dashboard'))

    return render_template('landing.html')


@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    """User onboarding flow."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        language = request.form.get('language', '').lower()
        tone_mode = request.form.get('tone_mode', '').lower()

        # Validate inputs
        if not username or not language or not tone_mode:
            flash('All fields are required.', 'error')
            return redirect(url_for('onboard'))

        # Check if user already exists
        if data_manager.user_exists(username):
            flash('Username already exists. Please log in.', 'warning')
            return redirect(url_for('login'))

        try:
            # Initialize schedule
            start_date = datetime.now().strftime("%Y-%m-%d")
            scheduler.initialize_schedule(username, language, start_date)

            # Update tone mode
            user_data = data_manager.load_user_data(username)
            user_data['profile']['tone_mode'] = tone_mode
            data_manager.save_user_data(username, user_data)

            # Log in the user
            session['username'] = username
            flash(f'Welcome to Kaizen, {username}! 🎉', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
            return redirect(url_for('onboard'))

    # GET request
    languages = get_supported_languages()
    tone_modes = ['playful', 'motivating', 'soft', 'genz']

    return render_template('onboard.html', languages=languages, tone_modes=tone_modes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()

        if data_manager.user_exists(username):
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('User not found. Please create an account.', 'error')
            return redirect(url_for('onboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout."""
    username = get_current_user()
    session.clear()
    flash(f'Goodbye, {username}! Keep learning! 📚', 'info')
    return redirect(url_for('landing'))


@app.route('/dashboard')
@require_login
def dashboard():
    """Main dashboard - today's learning."""
    username = get_current_user()
    user_data = data_manager.load_user_data(username)

    # Get current topic
    current = scheduler.get_current_topic(username)

    # Generate today's message
    try:
        context, topic = detect_context_from_schedule(username)
        message = notification_service.message_engine.generate_message(
            username=username,
            context=context,
            topic=topic
        )
    except:
        message = "Welcome to your learning journey! 🚀"
        context = "new_topic"

    # Get progress summary
    progress = scheduler.get_progress_summary(username)

    # Get streak information
    streak_stats = streak_tracker.get_streak_stats(username)

    return render_template(
        'dashboard.html',
        user=user_data['profile'],
        current=current,
        message=message,
        context=context,
        progress=progress,
        streak=streak_stats
    )


@app.route('/quiz', methods=['GET', 'POST'])
@require_login
def quiz():
    """Quiz interface."""
    username = get_current_user()
    current = scheduler.get_current_topic(username)

    if not current or current.get('quiz_score') is not None:
        flash('No pending quiz available.', 'info')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Process quiz submission
        score = float(request.form.get('score', 0))

        if score < 0 or score > 1:
            flash('Invalid score.', 'error')
            return redirect(url_for('quiz'))

        # Submit to adaptive scheduler
        result = scheduler.process_quiz_result(
            username=username,
            current_day_key=current['day_key'],
            quiz_score=score
        )

        # Show results
        session['quiz_result'] = result
        return redirect(url_for('quiz_result'))

    # GET request - show quiz
    user_data = data_manager.load_user_data(username)

    return render_template(
        'quiz.html',
        user=user_data['profile'],
        current=current
    )


@app.route('/quiz/result')
@require_login
def quiz_result():
    """Quiz result page."""
    result = session.pop('quiz_result', None)

    if not result:
        return redirect(url_for('dashboard'))

    username = get_current_user()
    user_data = data_manager.load_user_data(username)

    # Get action explanation
    action_messages = {
        'proceed': 'Great work! Moving to the next topic.',
        'schedule_review': 'Let\'s review this topic again to strengthen your understanding.',
        'accelerate': 'Excellent! You\'re ready to skip ahead!'
    }

    action_message = action_messages.get(result['action'], 'Continuing your journey...')

    return render_template(
        'quiz_result.html',
        user=user_data['profile'],
        result=result,
        action_message=action_message
    )


@app.route('/progress')
@require_login
def progress():
    """Progress tracking page."""
    username = get_current_user()
    user_data = data_manager.load_user_data(username)
    schedule = user_data['schedule']

    # Get progress summary
    summary = scheduler.get_progress_summary(username)

    # Get curriculum info
    language = user_data['profile']['language']
    curriculum = get_curriculum(language)

    # Format schedule for timeline
    schedule_timeline = []
    for day_key in sorted(schedule.keys(), key=lambda k: int(k.split('_')[1])):
        day_data = schedule[day_key]
        schedule_timeline.append({
            'day': day_key,
            'topic': day_data['topic'],
            'type': day_data['type'],
            'quiz_score': day_data.get('quiz_score'),
            'completed': day_data.get('quiz_score') is not None
        })

    return render_template(
        'progress.html',
        user=user_data['profile'],
        summary=summary,
        schedule_timeline=schedule_timeline,
        curriculum_length=len(curriculum)
    )


@app.route('/settings', methods=['GET', 'POST'])
@require_login
def settings():
    """Settings page."""
    username = get_current_user()
    user_data = data_manager.load_user_data(username)

    if request.method == 'POST':
        # Update tone mode
        new_tone = request.form.get('tone_mode', '').lower()

        if new_tone in ['playful', 'motivating', 'soft', 'genz']:
            user_data['profile']['tone_mode'] = new_tone
            data_manager.save_user_data(username, user_data)
            flash('Settings updated successfully!', 'success')
        else:
            flash('Invalid tone mode.', 'error')

        return redirect(url_for('settings'))

    # GET request
    tone_modes = ['playful', 'motivating', 'soft', 'genz']

    # Get message preview for current tone
    try:
        context, topic = detect_context_from_schedule(username)
        sample_message = notification_service.message_engine.generate_message(
            username=username,
            context=context,
            topic=topic or "Sample Topic"
        )
    except:
        sample_message = "Your personalized message will appear here!"

    return render_template(
        'settings.html',
        user=user_data['profile'],
        tone_modes=tone_modes,
        sample_message=sample_message
    )


# ============================================================================
# API ROUTES (for AJAX)
# ============================================================================

@app.route('/api/message/preview')
@require_login
def api_message_preview():
    """Get message preview for a tone mode."""
    username = get_current_user()
    tone = request.args.get('tone', 'playful')

    # Temporarily change tone
    user_data = data_manager.load_user_data(username)
    original_tone = user_data['profile']['tone_mode']
    user_data['profile']['tone_mode'] = tone
    data_manager.save_user_data(username, user_data)

    # Generate message
    try:
        context, topic = detect_context_from_schedule(username)
        message = notification_service.message_engine.generate_message(
            username=username,
            context='new_topic',
            topic=topic or "Sample Topic"
        )
    except:
        message = "Preview message"

    # Restore original tone
    user_data['profile']['tone_mode'] = original_tone
    data_manager.save_user_data(username, user_data)

    return jsonify({'message': message})


# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("🚀 Starting Kaizen Web Application")
    print("="*70)
    print("\nAccess the app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
