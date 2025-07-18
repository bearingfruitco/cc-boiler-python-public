# Enhanced Worktree Management

Create and manage git worktrees for parallel Claude Code sessions.

## Arguments:
- $ACTION: create|list|switch|remove|sync
- $FEATURE_NAME: Feature/branch name (for create/switch/remove)

## Why This Command is Critical:
- Run multiple Claude Code agents in parallel
- Each agent works on isolated codebase copy
- No merge conflicts during development
- Essential for multitasking workflow

## Steps:

### Action: CREATE
1. **Get Project Info**
   ```bash
   # Get current project folder name
   PROJECT_NAME=$(basename $(pwd))
   PARENT_DIR=$(dirname $(pwd))
   
   # Create worktrees directory if doesn't exist
   WORKTREES_DIR="$PARENT_DIR/${PROJECT_NAME}-worktrees"
   mkdir -p "$WORKTREES_DIR"
   ```

2. **Create Git Worktree**
   ```bash
   # Create worktree with new branch
   BRANCH_NAME="${FEATURE_NAME}"
   WORKTREE_PATH="$WORKTREES_DIR/$BRANCH_NAME"
   
   git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH"
   ```

3. **Copy Essential Files** (Critical!)
   ```bash
   # Copy files that git doesn't track
   cd "$WORKTREE_PATH"
   
   # Environment files
   cp ../../${PROJECT_NAME}/.env* . 2>/dev/null || true
   
   # Claude configuration
   cp -r ../../${PROJECT_NAME}/.claude . 2>/dev/null || true
   
   # Cursor settings
   cp -r ../../${PROJECT_NAME}/.cursor . 2>/dev/null || true
   
   # VS Code settings
   cp -r ../../${PROJECT_NAME}/.vscode . 2>/dev/null || true
   
   # Install dependencies (if needed)
   if [ -f "package.json" ]; then
     npm install
   fi
   ```

4. **Create Context File**
   ```bash
   # Create worktree context for Claude
   cat > .claude/WORKTREE_CONTEXT.md << EOF
   # Worktree: $BRANCH_NAME
   
   Created: $(date)
   Purpose: [Add purpose here]
   Main branch: $(cd ../../${PROJECT_NAME} && git branch --show-current)
   
   ## Design System Rules
   - Typography: 4 sizes, 2 weights only
   - Spacing: 4px grid
   - Touch targets: 44px minimum
   
   ## Notes
   - This is a worktree of ${PROJECT_NAME}
   - Changes here are isolated until merged
   - Run validation before merging back
   EOF
   ```

5. **Provide Next Steps**
   ```markdown
   ✅ Worktree created: $WORKTREE_PATH
   
   ## Next Steps:
   1. Open in new Cursor window:
      cursor "$WORKTREE_PATH"
   
   2. Or use terminal:
      cd "$WORKTREE_PATH"
   
   3. Start Claude Code:
      claude
   
   4. For parallel work, run server on different port:
      - Main: PORT=3000
      - This: PORT=3001 (or 3002, 3003, etc.)
   ```

### Action: LIST
```bash
# Show all worktrees with useful info
echo "🌳 Git Worktrees for $(basename $(pwd))"
echo ""

git worktree list --porcelain | while IFS= read -r line; do
  if [[ $line == worktree* ]]; then
    WTPATH=$(echo $line | cut -d' ' -f2)
    BRANCH=$(cd "$WTPATH" 2>/dev/null && git branch --show-current)
    
    echo "📁 $WTPATH"
    echo "   Branch: $BRANCH"
    
    # Check for uncommitted changes
    if [ -d "$WTPATH" ]; then
      CHANGES=$(cd "$WTPATH" && git status --porcelain | wc -l)
      if [ "$CHANGES" -gt 0 ]; then
        echo "   ⚠️  Uncommitted changes: $CHANGES files"
      else
        echo "   ✅ Clean"
      fi
    fi
    
    # Check if Claude is running
    if pgrep -f "claude.*$WTPATH" > /dev/null; then
      echo "   🤖 Claude Code: Running"
    fi
    echo ""
  fi
done
```

### Action: SWITCH
```bash
# Open worktree in new Cursor window
WORKTREES_DIR="../$(basename $(pwd))-worktrees"
WORKTREE_PATH="$WORKTREES_DIR/$FEATURE_NAME"

if [ -d "$WORKTREE_PATH" ]; then
  echo "Opening worktree in Cursor: $FEATURE_NAME"
  cursor "$WORKTREE_PATH"
else
  echo "❌ Worktree not found: $FEATURE_NAME"
  echo "Available worktrees:"
  git worktree list
fi
```

### Action: REMOVE
```bash
# Clean up worktree
WORKTREES_DIR="../$(basename $(pwd))-worktrees"
WORKTREE_PATH="$WORKTREES_DIR/$FEATURE_NAME"

# Check for uncommitted changes
if [ -d "$WORKTREE_PATH" ]; then
  CHANGES=$(cd "$WORKTREE_PATH" && git status --porcelain | wc -l)
  if [ "$CHANGES" -gt 0 ]; then
    echo "⚠️  Worktree has uncommitted changes!"
    echo "Commit or stash changes first."
    exit 1
  fi
fi

# Remove worktree
git worktree remove "$WORKTREE_PATH"
echo "✅ Removed worktree: $FEATURE_NAME"
```

### Action: SYNC
```bash
# Update all worktrees with main branch changes
echo "🔄 Syncing all worktrees with main..."

# First, update main
CURRENT_BRANCH=$(git branch --show-current)
git checkout main
git pull origin main

# Update each worktree
git worktree list --porcelain | while IFS= read -r line; do
  if [[ $line == worktree* ]] && [[ ! $line == *main* ]]; then
    WTPATH=$(echo $line | cut -d' ' -f2)
    BRANCH=$(cd "$WTPATH" && git branch --show-current)
    
    echo "Updating $BRANCH..."
    (cd "$WTPATH" && git pull origin main --rebase)
  fi
done

# Return to original branch
git checkout "$CURRENT_BRANCH"
```

## Pro Tips from the Video:

1. **Folder Structure**:
   ```
   /projects/
     music-shop/          # Main project
     music-shop-worktrees/  # Worktrees folder
       drums/            # Feature worktree
       keyboards/        # Feature worktree
       bases/            # Feature worktree
   ```

2. **Multiple Terminals**: Use different ports for each worktree
   - Main: `npm run dev` (port 3000)
   - Worktree 1: `PORT=3001 npm run dev`
   - Worktree 2: `PORT=3002 npm run dev`

3. **Desktop Management**: Use separate desktop spaces for each worktree

4. **Parallel Claude Sessions**: Each worktree can run its own Claude Code

## Example Workflow:

```bash
# Create worktrees for parallel features
/worktree create add-auth-components
/worktree create update-dashboard
/worktree create fix-mobile-layout

# List active worktrees
/worktree list

# Each opens in new Cursor window
# Each can run Claude Code independently
# Each works on isolated files

# After features complete, merge back
git merge add-auth-components
git merge update-dashboard
git merge fix-mobile-layout

# Clean up
/worktree remove add-auth-components
/worktree remove update-dashboard
/worktree remove fix-mobile-layout
```

This enables TRUE parallel development with multiple Claude Code agents!
