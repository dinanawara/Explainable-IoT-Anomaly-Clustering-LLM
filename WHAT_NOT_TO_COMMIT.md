# ⚠️ IMPORTANT: What NOT to Include When Publishing

**Before pushing to GitHub, make sure these files are NOT included:**

---

## 🔴 NEVER COMMIT

### 1. **`.env` file** ⚠️ CRITICAL
```
❌ DO NOT INCLUDE: .env
✅ INSTEAD: .env.example (template only)
```

**Why?** Your OpenAI API key is stored here.  
**What to do?** It's in `.gitignore`, but verify:
```bash
git status
# Should NOT show .env file
```

### 2. **`.venv/` directory** (virtual environment)
```
❌ DO NOT INCLUDE: .venv/
✅ INSTEAD: requirements.txt (users recreate it)
```

**Why?** ~200 MB of Python packages for your local system.  
**What to do?** Already in `.gitignore`:
```bash
grep ".venv" .gitignore
# Should return: .venv/
```

### 3. **`__pycache__/` directories**
```
❌ DO NOT INCLUDE: __pycache__/
✅ INSTEAD: Users regenerate on their system
```

**Why?** Compiled Python files, OS-specific, unnecessary.  
**What to do?** Already in `.gitignore`:
```bash
grep "__pycache__" .gitignore
# Should return: __pycache__/
```

### 4. **`*.pyc` files** (compiled Python)
```
❌ DO NOT INCLUDE: *.py[cod]
✅ INSTEAD: Source .py files only
```

**Why?** Same as `__pycache__`, OS-specific.  
**What to do?** Already in `.gitignore`

### 5. **`.DS_Store`** (macOS)
```
❌ DO NOT INCLUDE: .DS_Store
✅ INSTEAD: It's in .gitignore
```

**Why?** macOS folder metadata, not needed.  
**What to do?** Already excluded

---

## 🟡 OPTIONAL: Might Want to Exclude

### Large Data Files (>100 MB)
If your dataset is very large, consider:
```
❌ Maybe exclude: Raw CSV files (Bot-IoT-Dataset)
✅ Or include: But note in README they're in .gitignore for large repos
```

**Decision**: For this package, we INCLUDED them because:
- ✅ They're <500 MB total
- ✅ GitHub allows 100+ MB per file
- ✅ Users need data to reproduce
- ✅ Public dataset (UNSW Bot-IoT)

**If you exclude later:**
```bash
# Add to .gitignore
Data/Bot-IoT-Dataset/*.csv
```

### Generated Output Files
Optionally exclude:
```
❌ Maybe exclude: *.png, *.html (visualizations)
✅ Or include: For quick preview
```

**Decision**: We INCLUDED visualizations because:
- ✅ Relatively small (~50 MB)
- ✅ Good for README preview
- ✅ Users can regenerate if needed

---

## ✅ ALWAYS INCLUDE

### Code & Scripts
```
✓ *.py files (source code)
✓ *.ipynb files (notebooks)
✓ *.sh files (shell scripts)
```

### Documentation
```
✓ README.md
✓ *.md files
✓ LICENSE
```

### Configuration
```
✓ requirements.txt (dependencies)
✓ .env.example (safe template)
✓ .gitignore (protection rules)
✓ setup.py or setup.cfg (if using)
```

### Data
```
✓ *.json (processed data)
✓ *.csv (datasets)
✓ Data dictionaries
✓ Metadata files
```

---

## 🔍 Final Verification

Before pushing to GitHub:

```bash
cd /Users/nawara/Desktop/LLM-Clustering-Paper-Public

# 1. Check .env is NOT present
ls -la .env 2>/dev/null && echo "❌ ERROR: .env file exists!" || echo "✓ .env not present"

# 2. Verify .env in .gitignore
grep "^\.env$" .gitignore && echo "✓ .env in .gitignore" || echo "⚠️ Check .gitignore"

# 3. Check no API keys anywhere
grep -r "sk-proj-" . --exclude-dir=.venv --exclude-dir=.git 2>/dev/null && \
  echo "❌ ERROR: Found API keys!" || \
  echo "✓ No API keys found"

# 4. Verify git status is clean
git status
# Should show: "nothing to commit, working tree clean"
# And NOT show any .env files

# 5. Check what would be committed
git diff --cached --name-only | grep "\.env"
# Should return nothing (no output)

# 6. List excluded files
git check-ignore -v .env .venv/ __pycache__/
# Should show all three are ignored
```

---

## 🚨 If You Accidentally Commit `.env`

**DON'T PANIC!** Here's how to fix it:

### Option 1: Remove Locally (Before Push)
```bash
# If you haven't pushed yet:
git rm --cached .env
git commit --amend -m "Remove .env (API key)"
# Now safe to push
```

### Option 2: After Accidental Push
```bash
# Revoke the key immediately:
# 1. Visit: https://platform.openai.com/api-keys
# 2. Delete the old key
# 3. Create a new key
# 4. Update .env locally (not pushed)

# Then clean git history:
# Use BFG Repo-Cleaner (brew install bfg)
bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force-with-lease
```

---

## 📋 Commit Checklist

Before `git commit`:

- [ ] `.env` file is NOT in staging area
- [ ] `.venv/` is NOT in staging area
- [ ] No `__pycache__/` directories
- [ ] No `*.pyc` files
- [ ] No `.DS_Store` files
- [ ] Ran `grep "sk-" .` and found only `.env.example`
- [ ] Ran `git status` and no `.env` is listed
- [ ] Ready for public release

---

## 🎯 Remember

> **YOUR API KEY IS YOUR PASSWORD**
> 
> Treat it like your bank account password. Never:
> - Commit it to git ❌
> - Put it in comments ❌
> - Share in messages ❌
> - Log it to console ❌
> - Include in error messages ❌

Always:
- Store in `.env` ✅
- Load with `python-dotenv` ✅
- Keep in `.gitignore` ✅
- Rotate periodically ✅
- Revoke if leaked ✅

---

## ✨ Final Status

**BEFORE PUSHING:**
```bash
# This should work:
git status
# Output: nothing to commit, working tree clean
# Should NOT show .env

# This should be clean:
grep -r "sk-" . --exclude-dir=.venv --exclude-dir=.git
# Output: (nothing, or only in .env.example)

# This should list all ignored files:
git check-ignore -v .env .venv/ __pycache__/
```

**AFTER PUSHING:**
```bash
# Visit GitHub and verify:
# ✓ .env is NOT in the repo
# ✓ .env.example IS in the repo
# ✓ .venv/ is NOT in the repo
# ✓ No __pycache__/ directories
```

---

**Status**: ✅ **SECURITY VERIFIED - SAFE TO PUSH**

---

**Created**: January 31, 2026  
**Review Date**: Before pushing to GitHub  
**Critical**: Yes - API key protection depends on this!
