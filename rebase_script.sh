#!/bin/bash

# Create a mapping of commit messages
cat > /tmp/commit_messages.txt << 'EOF'
bf696bb|Add input validation functions for user data
f2a9d90|Implement UserProfile and Schedule data models
8603e38|Create JSON data persistence layer
b29b927|Initialize data directory structure
3cd02f5|Add project dependencies (pandas, sklearn, flask, plyer)
9f2916c|Update .gitignore with Python-specific patterns
0744003|Document project structure and quick start guide
4d414f1|Add learning curriculum for Python, JavaScript, and Java
c5a422e|Create synthetic training data generator for ML model
b8be9c4|Generate 1000 training examples for adaptive learning
e92b3a5|Implement Random Forest adaptive learning model
f8af69d|Train ML model and save classifier (97.5% accuracy)
821934b|Build adaptive scheduler with ML integration
009d79d|Add adaptive learning demonstration script
1511bcc|Create personality-driven message templates (100+ messages)
81de87d|Implement message engine with anti-repetition logic
9979717|Initialize message history tracking
41a6693|Build notification service with desktop alerts
f373f0d|Update message history after notifications
37510c0|Track notification delivery status
6117ecb|Add personality comparison demo script
5fdf607|Log demo personality notifications
0b597f2|Fix scheduler initialization in demo (remove extra parameter)
9d971ac|Update message history from fixed demo
19d5de2|Create Flask web application with 11 routes
85cf468|Add base template and landing page
c497855|Create login and onboarding pages
9c42694|Build main dashboard with learning overview
2ca437e|Implement quiz interface and result pages
bed45b7|Add progress tracking and settings pages
ebd80f4|Design modern UI with personality themes and animations
cbae12f|Create web app startup script with environment setup
129e843|Document web application features and API
0da1364|Implement streak tracking with milestone celebrations
3a86d99|Add daily reminder scheduler with background threading
f0463f9|Update dependencies to include schedule library
74b96e4|Integrate streak tracker into dashboard route
58342b3|Import StreakTracker in Flask app
c3f395d|Add animated streak card to dashboard UI
5649a63|Style streak card with fire icon and pulse animation
a34caf1|Document streak tracking and daily reminders
5deb376|Add quick start guide for launching the app
EOF

# Use git filter-branch to rewrite commit messages
while IFS='|' read hash message; do
    export FILTER_BRANCH_SQUELCH_WARNING=1
    GIT_COMMITTER_DATE="$(git show -s --format=%cI $hash)" \
    git filter-branch -f --msg-filter "
        if [ \"\$GIT_COMMIT\" = \"$hash\" ]; then
            echo \"$message\"
        else
            cat
        fi
    " --tag-name-filter cat -- --all 2>/dev/null
done < /tmp/commit_messages.txt

echo "✅ Commit messages updated!"
