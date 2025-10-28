#!/bin/bash
set -e

echo "🔄 Rewriting commit messages..."

# Backup current branch
git branch backup-before-rewrite 2>/dev/null || true

# Use git filter-branch to rewrite messages
export FILTER_BRANCH_SQUELCH_WARNING=1

git filter-branch -f --msg-filter '
msg=$(cat)
if [ "$msg" = "Auto-commit: Agent tool execution" ]; then
    case "$GIT_COMMIT" in
        bf696bb*) echo "Add input validation functions for user data" ;;
        f2a9d90*) echo "Implement UserProfile and Schedule data models" ;;
        8603e38*) echo "Create JSON data persistence layer" ;;
        b29b927*) echo "Initialize data directory structure" ;;
        3cd02f5*) echo "Add project dependencies" ;;
        9f2916c*) echo "Update .gitignore with Python patterns" ;;
        0744003*) echo "Document project structure and quick start" ;;
        4d414f1*) echo "Add learning curriculum for 3 languages" ;;
        c5a422e*) echo "Create synthetic training data generator" ;;
        b8be9c4*) echo "Generate 1000 training examples" ;;
        e92b3a5*) echo "Implement Random Forest ML model" ;;
        f8af69d*) echo "Train ML model (97.5% accuracy)" ;;
        821934b*) echo "Build adaptive scheduler with ML integration" ;;
        009d79d*) echo "Add adaptive learning demo script" ;;
        1511bcc*) echo "Create personality message templates (100+)" ;;
        81de87d*) echo "Implement message engine with anti-repetition" ;;
        9979717*) echo "Initialize message history tracking" ;;
        41a6693*) echo "Build notification service with desktop alerts" ;;
        f373f0d*) echo "Update message history" ;;
        37510c0*) echo "Track notification delivery" ;;
        6117ecb*) echo "Add personality comparison demo" ;;
        5fdf607*) echo "Log demo notifications" ;;
        0b597f2*) echo "Fix scheduler initialization bug" ;;
        9d971ac*) echo "Update message history after fix" ;;
        19d5de2*) echo "Create Flask web app with 11 routes" ;;
        85cf468*) echo "Add base template and landing page" ;;
        c497855*) echo "Create login and onboarding pages" ;;
        9c42694*) echo "Build main dashboard" ;;
        2ca437e*) echo "Implement quiz interface and results" ;;
        bed45b7*) echo "Add progress tracking and settings pages" ;;
        ebd80f4*) echo "Design modern UI with personality themes" ;;
        cbae12f*) echo "Create web app startup script" ;;
        129e843*) echo "Document web application features" ;;
        0da1364*) echo "Implement streak tracking system" ;;
        3a86d99*) echo "Add daily reminder scheduler" ;;
        f0463f9*) echo "Update dependencies (add schedule library)" ;;
        74b96e4*) echo "Integrate streak tracker into dashboard" ;;
        58342b3*) echo "Import StreakTracker in Flask app" ;;
        c3f395d*) echo "Add animated streak card to dashboard" ;;
        5649a63*) echo "Style streak card with fire icon animation" ;;
        a34caf1*) echo "Document streak and reminder features" ;;
        5deb376*) echo "Add quick start launch guide" ;;
        *) echo "$msg" ;;
    esac
else
    echo "$msg"
fi
' -- --all

echo "✅ Done! Commit messages have been rewritten."
echo ""
echo "To see the changes, run: git log --oneline -20"
echo ""
echo "If you need to undo this, run: git reset --hard backup-before-rewrite"
