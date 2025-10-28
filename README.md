# Kaizen - Adaptive Learning Companion

An intelligent desktop application that uses machine learning to create personalized, adaptive learning schedules with playful, context-aware notifications.

## Setup

### Requirements
- Python 3.8 or higher

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
kaizen/
├── models.py           # User profile and schedule data classes
├── data_manager.py     # JSON persistence functions
├── validators.py       # Input validation functions
├── requirements.txt    # Python dependencies
├── data/
│   └── users/         # User data storage (JSON files)
└── README.md
```

## Quick Start

### Create a new user

```python
from data_manager import create_user

user_data = create_user(
    username="arfa",
    language="python",
    tone_mode="playful",
    start_date="2024-01-15"
)
```

### Update learning schedule

```python
from data_manager import update_schedule

update_schedule(
    username="arfa",
    day_key="day_1",
    topic="Variables",
    topic_type="new_topic",
    quiz_score=0.8
)
```

### Load user data

```python
from data_manager import load_user_data

user_data = load_user_data("arfa")
print(user_data["profile"])
print(user_data["schedule"])
```

## Data Validation

All user inputs are validated:
- **Username**: 3-20 characters, alphanumeric + underscore
- **Tone Mode**: playful, motivating, soft, or genz
- **Date Format**: YYYY-MM-DD (ISO 8601)
- **Quiz Score**: 0.0 to 1.0 or None

## Development Status

**Current Phase:** Foundation - Core data models and persistence ✅

**Coming Soon:**
- ML-based adaptive scheduler
- Context-aware notification engine
- Web interface
- Progress visualization

## License

TBD