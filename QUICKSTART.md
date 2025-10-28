# Kaizen - Quick Start Guide 🚀

Get Kaizen running in 3 simple steps!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation & Launch

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- pandas (data processing)
- scikit-learn (ML model)
- flask (web framework)
- plyer (notifications)
- schedule (daily reminders)

### Step 2: Start the Web App

**Option A: Using the startup script (Recommended)**
```bash
./run_web_app.sh
```

**Option B: Direct Python command**
```bash
PYTHONPATH=/usr/local/lib/python3.12/site-packages python3 app.py
```

### Step 3: Open Your Browser

Navigate to:
```
http://localhost:5000
```

That's it! 🎉

## First Time Setup

1. **Click "Start Learning"** on the landing page
2. **Create your account:**
   - Choose a username (3-20 characters)
   - Select your language (Python, JavaScript, or Java)
   - Pick your personality (playful, motivating, soft, or genz)
3. **Click "Start My Journey"**
4. You're in! 🌱

## Using Kaizen

### Daily Workflow

1. **Dashboard** - See today's topic and your streak
2. **Take Quiz** - Rate your understanding (5 levels)
3. **Get Results** - ML adapts your schedule automatically
4. **Check Progress** - View your learning timeline
5. **Repeat Daily** - Build your streak! 🔥

### Key Features

- 📊 **Dashboard** - Daily topic, streak counter, stats
- 🎯 **Quiz System** - 5-level understanding rating
- 📈 **Progress Page** - Complete timeline and analytics
- ⚙️ **Settings** - Change your personality anytime
- 🔥 **Streak Tracking** - Build consecutive learning days
- 🧠 **ML Adaptation** - Schedule adjusts to your performance

## Troubleshooting

### Port Already in Use
```bash
# Kill existing process
pkill -f "python3 app.py"

# Or use different port
export FLASK_RUN_PORT=5001
python3 app.py
```

### Dependencies Won't Install
```bash
# Try with sudo (Linux/Mac)
sudo pip install -r requirements.txt

# Or use Python module installer
python3 -m pip install -r requirements.txt
```

### ML Model Error
The app automatically trains the model on first run. If you see errors:
```bash
# Manually train the model
PYTHONPATH=/usr/local/lib/python3.12/site-packages python3 ml_model.py
```

### Can't Access localhost:5000
- Make sure no firewall is blocking port 5000
- Try: http://127.0.0.1:5000
- Check if Flask started successfully in the terminal

## Demo Mode

Want to see it in action without creating an account?

```bash
# Run the adaptive learning demo
PYTHONPATH=/usr/local/lib/python3.12/site-packages python3 demo_adaptive_learning.py

# See all 4 personalities
PYTHONPATH=/usr/local/lib/python3.12/site-packages python3 demo_personalities.py
```

## Stopping the Server

Press `Ctrl+C` in the terminal where Flask is running.

## Next Steps

- ✅ Complete your first quiz
- ✅ Build a 3-day streak
- ✅ Try different personality modes
- ✅ Check out the progress timeline
- ✅ Reach your first milestone! 🎯

## Need Help?

- **Web App Guide**: Read `WEB_APP_GUIDE.md`
- **Streak System**: Read `STREAK_AND_REMINDERS_GUIDE.md`
- **General Info**: Read `README.md`

---

**Happy Learning! 🌱**

Built with ML, personality, and ❤️
