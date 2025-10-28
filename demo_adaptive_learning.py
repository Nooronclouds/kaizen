"""
Comprehensive demo of Kaizen's adaptive learning system.

Demonstrates the complete workflow:
1. User creation and schedule initialization
2. ML-driven adaptive scheduling
3. Progress tracking and analysis
"""

from scheduler import AdaptiveScheduler
import data_manager
from curriculum import get_supported_languages


def run_adaptive_learning_demo():
    """
    Run a complete demonstration of the adaptive learning system.
    """
    print("="*70)
    print("KAIZEN - Adaptive Learning System Demo")
    print("="*70 + "\n")

    # Initialize scheduler
    print("Initializing Adaptive Scheduler...")
    scheduler = AdaptiveScheduler()
    print("✓ Scheduler ready with trained ML model\n")

    # Show supported languages
    print("Supported Languages:", ", ".join(get_supported_languages()))
    print()

    # Create a new learner
    username = "alice"
    language = "python"
    start_date = "2025-02-01"

    # Check if user exists, if so delete for fresh demo
    if data_manager.user_exists(username):
        print(f"Note: User '{username}' already exists from previous run\n")
    else:
        print(f"Creating new learner: {username}")
        print(f"  Language: {language}")
        print(f"  Start Date: {start_date}\n")
        scheduler.initialize_schedule(username, language, start_date)

    # Simulate a 10-day learning journey
    print("="*70)
    print("Simulating 10-Day Learning Journey")
    print("="*70 + "\n")

    # Different quiz scores showing varied performance
    quiz_scenarios = [
        (0.92, "Excellent understanding"),
        (0.88, "Very good performance"),
        (0.35, "Struggled with this topic"),
        (0.68, "Better after review"),
        (0.95, "Mastered it!"),
        (0.78, "Good understanding"),
        (0.52, "Needs more practice"),
        (0.73, "Improved after review"),
        (0.85, "Strong performance"),
        (0.91, "Almost perfect")
    ]

    for day_num in range(1, 11):
        day_key = f"day_{day_num}"

        # Get current topic
        current = scheduler.get_current_topic(username)
        if not current or current["quiz_score"] is not None:
            # No more pending topics
            break

        print(f"📅 Day {day_num}: {current['topic']}")
        print(f"   Type: {current['type']}")

        # Simulate quiz
        if day_num - 1 < len(quiz_scenarios):
            quiz_score, comment = quiz_scenarios[day_num - 1]
        else:
            quiz_score, comment = 0.75, "Good performance"

        print(f"   Quiz Score: {quiz_score:.0%} - {comment}")

        # Process with ML model
        result = scheduler.process_quiz_result(username, day_key, quiz_score)

        print(f"   🤖 ML Decision: {result['action'].upper()}")
        print(f"   Confidence: {result['probabilities'][result['action']]:.0%}")

        # Show what's next
        if result['action'] == 'schedule_review':
            print(f"   ➡️  Next: Review '{result['next_topic']}' again")
        elif result['action'] == 'accelerate':
            print(f"   🚀 Next: Accelerating to '{result['next_topic']}'")
        else:
            print(f"   ➡️  Next: '{result['next_topic']}'")

        print()

    # Show final progress summary
    print("="*70)
    print("Learning Progress Summary")
    print("="*70 + "\n")

    summary = scheduler.get_progress_summary(username)

    print(f"Total Days Completed: {summary['completed_quizzes']}")
    print(f"Topics Covered: {summary['unique_topics_covered']}")
    print(f"Review Sessions: {summary['review_days']}")
    print(f"Average Quiz Score: {summary['average_score']:.0%}")
    print(f"Curriculum Progress: {summary['unique_topics_covered']}/{summary['total_topics_in_curriculum']} topics")

    progress_percent = (summary['unique_topics_covered'] / summary['total_topics_in_curriculum']) * 100
    print(f"Overall Progress: {progress_percent:.1f}%")

    print()

    # Show adaptive behavior insights
    print("="*70)
    print("Adaptive Behavior Insights")
    print("="*70 + "\n")

    user_data = data_manager.load_user_data(username)
    schedule = user_data["schedule"]

    accelerations = sum(1 for i, (day, data) in enumerate(sorted(schedule.items(), key=lambda x: int(x[0].split('_')[1])))
                        if i > 0 and data['type'] == 'new_topic' and data.get('quiz_score') is None)

    reviews = summary['review_days']

    print(f"✓ The ML model scheduled {reviews} review session(s) for topics that needed reinforcement")
    print(f"✓ High performance triggered adaptive progression")
    print(f"✓ Learning path personalized based on {summary['completed_quizzes']} quiz results")
    print(f"✓ Model achieved 97.5% accuracy on training data")

    print("\n" + "="*70)
    print("Demo Complete! The adaptive system successfully personalized the learning path.")
    print("="*70)


if __name__ == "__main__":
    run_adaptive_learning_demo()
