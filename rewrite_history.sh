#!/bin/bash

# Get the list of commits in reverse order (oldest first)
commits=(
  "bf696bb" "f2a9d90" "8603e38" "b29b927" "3cd02f5" "9f2916c" "0744003"
  "4d414f1" "c5a422e" "b8be9c4" "e92b3a5" "f8af69d" "821934b" "009d79d"
  "1511bcc" "81de87d" "9979717" "41a6693" "f373f0d" "37510c0" "6117ecb"
  "5fdf607" "0b597f2" "9d971ac" "19d5de2" "85cf468" "c497855" "9c42694"
  "2ca437e" "bed45b7" "ebd80f4" "cbae12f" "129e843" "0da1364" "3a86d99"
  "f0463f9" "74b96e4" "58342b3" "c3f395d" "5649a63" "a34caf1" "5deb376"
)

# New commit messages (matching order above)
messages=(
  "Add input validation functions for user data"
  "Implement UserProfile and Schedule data models"
  "Create JSON data persistence layer"
  "Initialize data directory structure"
  "Add project dependencies"
  "Update .gitignore with Python patterns"
  "Document project structure and quick start"
  "Add learning curriculum for 3 languages"
  "Create synthetic training data generator"
  "Generate 1000 training examples"
  "Implement Random Forest ML model"
  "Train ML model (97.5% accuracy)"
  "Build adaptive scheduler with ML integration"
  "Add adaptive learning demo script"
  "Create personality message templates (100+)"
  "Implement message engine with anti-repetition"
  "Initialize message history tracking"
  "Build notification service with desktop alerts"
  "Update message history"
  "Track notification delivery"
  "Add personality comparison demo"
  "Log demo notifications"
  "Fix scheduler initialization bug"
  "Update message history after fix"
  "Create Flask web app with 11 routes"
  "Add base template and landing page"
  "Create login and onboarding pages"
  "Build main dashboard"
  "Implement quiz interface and results"
  "Add progress tracking and settings pages"
  "Design modern UI with personality themes"
  "Create web app startup script"
  "Document web application features"
  "Implement streak tracking system"
  "Add daily reminder scheduler"
  "Update dependencies (add schedule library)"
  "Integrate streak tracker into dashboard"
  "Import StreakTracker in Flask app"
  "Add animated streak card to dashboard"
  "Style streak card with fire icon animation"
  "Document streak and reminder features"
  "Add quick start launch guide"
)

echo "🔄 Rewriting git history with proper commit messages..."
echo "This will reword 42 commits..."
echo

# Create a rebase script
cat > /tmp/rebase-todo << 'EOF'
#!/bin/bash
# This script will be used as GIT_SEQUENCE_EDITOR
sed -i 's/^pick /reword /' "$1"
EOF
chmod +x /tmp/rebase-todo

# Create commit message provider script
cat > /tmp/git-commit-msg << 'MSGEOF'
#!/bin/bash
# Read the current commit message
current_msg=$(cat "$1")

# Map of commit hashes to new messages
declare -A msg_map
msg_map["bf696bb"]="Add input validation functions for user data"
msg_map["f2a9d90"]="Implement UserProfile and Schedule data models"
msg_map["8603e38"]="Create JSON data persistence layer"
msg_map["b29b927"]="Initialize data directory structure"
msg_map["3cd02f5"]="Add project dependencies"
msg_map["9f2916c"]="Update .gitignore with Python patterns"
msg_map["0744003"]="Document project structure and quick start"
msg_map["4d414f1"]="Add learning curriculum for 3 languages"
msg_map["c5a422e"]="Create synthetic training data generator"
msg_map["b8be9c4"]="Generate 1000 training examples"
msg_map["e92b3a5"]="Implement Random Forest ML model"
msg_map["f8af69d"]="Train ML model (97.5% accuracy)"
msg_map["821934b"]="Build adaptive scheduler with ML integration"
msg_map["009d79d"]="Add adaptive learning demo script"
msg_map["1511bcc"]="Create personality message templates (100+)"
msg_map["81de87d"]="Implement message engine with anti-repetition"
msg_map["9979717"]="Initialize message history tracking"
msg_map["41a6693"]="Build notification service with desktop alerts"
msg_map["f373f0d"]="Update message history"
msg_map["37510c0"]="Track notification delivery"
msg_map["6117ecb"]="Add personality comparison demo"
msg_map["5fdf607"]="Log demo notifications"
msg_map["0b597f2"]="Fix scheduler initialization bug"
msg_map["9d971ac"]="Update message history after fix"
msg_map["19d5de2"]="Create Flask web app with 11 routes"
msg_map["85cf468"]="Add base template and landing page"
msg_map["c497855"]="Create login and onboarding pages"
msg_map["9c42694"]="Build main dashboard"
msg_map["2ca437e"]="Implement quiz interface and results"
msg_map["bed45b7"]="Add progress tracking and settings pages"
msg_map["ebd80f4"]="Design modern UI with personality themes"
msg_map["cbae12f"]="Create web app startup script"
msg_map["129e843"]="Document web application features"
msg_map["0da1364"]="Implement streak tracking system"
msg_map["3a86d99"]="Add daily reminder scheduler"
msg_map["f0463f9"]="Update dependencies (add schedule library)"
msg_map["74b96e4"]="Integrate streak tracker into dashboard"
msg_map["58342b3"]="Import StreakTracker in Flask app"
msg_map["c3f395d"]="Add animated streak card to dashboard"
msg_map["5649a63"]="Style streak card with fire icon animation"
msg_map["a34caf1"]="Document streak and reminder features"
msg_map["5deb376"]="Add quick start launch guide"

# Check if current message is an auto-commit
if [[ "$current_msg" == "Auto-commit: Agent tool execution" ]]; then
    # Get the current commit hash
    current_hash=$(git rev-parse HEAD 2>/dev/null || echo "")
    short_hash=${current_hash:0:7}

    # Look up new message
    if [[ -n "${msg_map[$short_hash]}" ]]; then
        echo "${msg_map[$short_hash]}" > "$1"
    fi
fi
MSGEOF
chmod +x /tmp/git-commit-msg

# Perform the rebase
export GIT_SEQUENCE_EDITOR=/tmp/rebase-todo
export GIT_EDITOR="cat"
FILTER_BRANCH_SQUELCH_WARNING=1 git rebase -i --root --committer-date-is-author-date

echo
echo "✅ Git history rewritten!"
echo "Run 'git log --oneline' to see the new commit messages"
