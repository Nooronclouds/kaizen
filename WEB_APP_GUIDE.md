# Kaizen Web Application Guide 🌱

Complete Flask web interface for Kaizen's adaptive learning system.

## Features

### 🎨 **Beautiful Modern UI**
- Clean, responsive design
- Personality-themed color schemes
- Smooth animations and transitions
- Mobile-friendly layout

### 🎭 **4 Unique Personalities**
Each tone mode has its own visual theme and message style:
- **😏 Playful**: Purple gradient theme, fun and witty
- **💪 Motivating**: Pink/red theme, energetic and pushing
- **🌙 Soft**: Teal/pink theme, gentle and supportive
- **💅 Genz**: Pink/yellow theme, internet culture vibes

### 📊 **Complete Learning Dashboard**
- Daily personalized message
- Current topic card with quiz access
- Real-time progress statistics
- Quick navigation to all features

### 🎯 **Interactive Quiz System**
- 5-level understanding rating
- ML-powered adaptive decisions
- Real-time schedule adjustments
- Visual feedback and confidence metrics

### 📈 **Progress Tracking**
- Comprehensive statistics dashboard
- Visual timeline of learning journey
- Topic completion tracking
- Average score analytics

### ⚙️ **Customization Settings**
- Easy personality switching
- Live message previews
- Account information display

## Quick Start

### 1. Start the Web Application

```bash
# Option 1: Using the startup script
./run_web_app.sh

# Option 2: Direct Python command
PYTHONPATH=/usr/local/lib/python3.12/site-packages python3 app.py
```

### 2. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### 3. Create Your Account

1. Click "Start Learning" on the landing page
2. Choose a username (3-20 characters)
3. Select your programming language
4. Pick your learning personality
5. Click "Start My Journey"

## User Flow

```
Landing Page
    ↓
Onboarding (New User) / Login (Existing User)
    ↓
Dashboard
    ├─→ Take Quiz → Quiz Result → Dashboard
    ├─→ View Progress (Timeline & Stats)
    └─→ Settings (Change Personality)
```

## Pages Overview

### 🏠 **Landing Page** (`/`)
- Feature showcase
- Call-to-action buttons
- Product overview

### 📝 **Onboarding** (`/onboard`)
- Account creation form
- Language selection
- Personality picker with descriptions

### 🔑 **Login** (`/login`)
- Simple username-based login
- Redirect to onboarding for new users

### 📊 **Dashboard** (`/dashboard`)
- Personalized daily message
- Current topic information
- Quiz button (if pending)
- Quick statistics grid
- Navigation to other sections

### 🎯 **Quiz** (`/quiz`)
- 5-level understanding rating
- Visual emoji-based options
- Submit to ML model

### 📈 **Quiz Results** (`/quiz/result`)
- ML decision display (proceed/review/accelerate)
- Next topic preview
- Confidence metrics visualization

### 📉 **Progress** (`/progress`)
- Summary statistics cards
- Full timeline of learning journey
- Topic completion status
- Visual progress bars

### ⚙️ **Settings** (`/settings`)
- Personality switcher
- Live message preview
- Account information

## API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET /onboard` - Onboarding form
- `POST /onboard` - Create account
- `GET /login` - Login form
- `POST /login` - User login

### Protected Routes (Require Login)
- `GET /dashboard` - Main dashboard
- `GET /quiz` - Quiz interface
- `POST /quiz` - Submit quiz
- `GET /quiz/result` - Quiz results
- `GET /progress` - Progress tracking
- `GET /settings` - Settings page
- `POST /settings` - Update settings
- `GET /logout` - User logout

### API Routes (AJAX)
- `GET /api/message/preview?tone=<mode>` - Preview message for tone

## Technical Stack

### Backend
- **Flask 3.1.2** - Web framework
- **Session Management** - User authentication
- **Jinja2** - Template engine

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid/Flexbox
- **Responsive Design** - Mobile-first approach

### Integration
- **Scheduler Module** - Adaptive learning logic
- **Notification Service** - Message generation
- **Data Manager** - JSON persistence
- **ML Model** - Random Forest classifier

## Customization

### Color Themes

Each personality has unique colors defined in `static/css/style.css`:

```css
--playful: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--motivating: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--soft: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
--genz: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
```

### Adding New Pages

1. Create route in `app.py`:
```python
@app.route('/new-page')
@require_login
def new_page():
    return render_template('new_page.html')
```

2. Create template in `templates/new_page.html`:
```html
{% extends "base.html" %}
{% block content %}
  <!-- Your content -->
{% endblock %}
```

3. Add navigation link in `templates/base.html`

### Custom Styling

Edit `static/css/style.css` to modify:
- Colors (`--primary`, `--secondary`, etc.)
- Spacing (`--space-sm`, `--space-md`, etc.)
- Border radius (`--radius-sm`, `--radius-md`, etc.)
- Shadows (`--shadow-sm`, `--shadow-md`, etc.)

## Session Management

- Session-based authentication (no passwords)
- Session data stored in Flask session
- Automatic logout on browser close
- Username-based user identification

## Security Notes

**⚠️ Important: This is a learning prototype**

Current implementation:
- ✅ Session-based authentication
- ✅ CSRF protection (Flask default)
- ✅ Input validation
- ❌ No password authentication
- ❌ No SSL/HTTPS enforcement
- ❌ No rate limiting

For production use, add:
- Password hashing (bcrypt)
- SSL certificates
- Rate limiting
- Enhanced session security
- Database instead of JSON files

## Troubleshooting

### Port Already in Use
```bash
# Kill existing Flask process
pkill -f "python3 app.py"

# Or use a different port
export FLASK_RUN_PORT=5001
python3 app.py
```

### Templates Not Found
```bash
# Ensure you're in the kaizen directory
cd kaizen

# Verify templates folder exists
ls templates/
```

### Static Files Not Loading
```bash
# Check static folder
ls static/css/

# Clear browser cache
# Press Ctrl+Shift+R in browser
```

### ML Model Errors
```bash
# Retrain the model
python3 ml_model.py

# Verify model file exists
ls data/adaptive_model.pkl
```

## Development Mode

Run Flask in development mode for auto-reload:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python3 app.py
```

## File Structure

```
kaizen/
├── app.py                      # Main Flask application
├── run_web_app.sh              # Startup script
├── templates/
│   ├── base.html               # Base template
│   ├── landing.html            # Landing page
│   ├── onboard.html            # Onboarding flow
│   ├── login.html              # Login page
│   ├── dashboard.html          # Main dashboard
│   ├── quiz.html               # Quiz interface
│   ├── quiz_result.html        # Quiz results
│   ├── progress.html           # Progress tracking
│   └── settings.html           # Settings page
├── static/
│   └── css/
│       └── style.css           # Main stylesheet
└── data/
    └── users/                  # User data storage
```

## Screenshots Walkthrough

### Landing Page
- Hero section with gradient title
- Feature grid showcasing capabilities
- CTA buttons for onboarding/login

### Dashboard
- Personalized greeting
- Daily motivational message (personality-specific)
- Current topic card with quiz button
- Statistics grid (completed quizzes, topics, average score, learning days)

### Quiz Interface
- Topic header with day badge
- 5 emoji-based understanding levels
- Clear descriptions for each level
- Submit button

### Progress Page
- Summary cards with visual progress bars
- Complete timeline of all learning days
- Color-coded badges (new topic, review, completed)
- Score display for completed days

### Settings Page
- 4 personality cards with descriptions
- Live message preview
- Account information display
- Save button

## Best Practices

1. **Always test changes locally first**
2. **Keep templates organized and DRY**
3. **Use CSS variables for consistent theming**
4. **Validate all user inputs**
5. **Provide clear user feedback (flash messages)**
6. **Make UI responsive for mobile**
7. **Follow RESTful routing conventions**

## Future Enhancements

Potential features to add:
- [ ] Real quiz questions with auto-grading
- [ ] Progress charts and graphs (Chart.js)
- [ ] Streak tracking and badges
- [ ] Social features (leaderboards)
- [ ] Dark mode toggle
- [ ] Notification scheduling
- [ ] Export progress reports
- [ ] Multi-language support
- [ ] Accessibility improvements (ARIA labels)

## Support

For issues or questions:
1. Check this guide first
2. Review Flask documentation
3. Check browser console for errors
4. Verify all dependencies are installed

---

Built with ❤️ using Flask, adaptive ML, and personality-driven design.

**Version:** 1.0.0
**Last Updated:** 2025-10-28
