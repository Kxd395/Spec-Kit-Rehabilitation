# How to Properly Set Up Your Forked/Modified Spec-Kit

**Date:** October 18, 2025

## 🔴 **CRITICAL ISSUE IDENTIFIED**

Your repository is currently pointing to the **official GitHub spec-kit** repo:
```
origin: https://github.com/github/spec-kit.git
```

**This is WRONG for your use case because:**

1. ❌ You can't push your changes to GitHub's official repo (you don't have permission)
2. ❌ Your "rehabilitation" features will never be accepted upstream (they're experimental)
3. ❌ You're on a branch called "main" that tracks GitHub's official project
4. ❌ Other developers would clone GitHub's repo, not your modified version
5. ❌ The repo name "EventDeskPro" doesn't match the content "spec-kit"

---

## 🎯 **WHAT YOU NEED TO DECIDE**

### **Option 1: Create Your Own Fork (Recommended)**
*Best if you want to build on spec-kit and add your own features*

### **Option 2: Create Standalone Project**
*Best if you want complete independence from spec-kit*

### **Option 3: Contribute Upstream**
*Best if you want your changes in the official spec-kit*

---

## ✅ **OPTION 1: Create Your Own Fork** (RECOMMENDED)

This is what you should do if you want to:
- Build on top of spec-kit
- Add your rehabilitation features
- Use it across multiple projects
- Eventually share with others

### **Step 1: Create Your Own GitHub Repository**

```bash
# Go to GitHub.com and create a NEW repository
# Name it something meaningful:
# - "spec-kit-enhanced" 
# - "spec-kit-rehabilitation"
# - "spec-analyzer" (if you build the real tools)
# 
# Do NOT initialize with README (you already have files)
```

### **Step 2: Update Git Remote**

```bash
cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit

# Rename current remote from 'origin' to 'upstream'
git remote rename origin upstream

# Add YOUR new repository as 'origin'
git remote add origin https://github.com/YOUR_USERNAME/YOUR_NEW_REPO_NAME.git

# Verify configuration
git remote -v

# Should show:
# origin    https://github.com/YOUR_USERNAME/YOUR_NEW_REPO_NAME.git (fetch)
# origin    https://github.com/YOUR_USERNAME/YOUR_NEW_REPO_NAME.git (push)
# upstream  https://github.com/github/spec-kit.git (fetch)
# upstream  https://github.com/github/spec-kit.git (push)
```

### **Step 3: Commit Your Changes**

```bash
# Stage all your new files
git add .

# Commit with clear message
git commit -m "Add rehabilitation features and analysis tools

- Added real security scanning (Bandit integration)
- Created roadmap for legitimate tool development
- Added honest assessment documentation
- Included quick start implementation guide
- Enhanced with security analysis templates"

# Push to YOUR repository
git push -u origin main
```

### **Step 4: Update README**

Add this section to the top of your README:

```markdown
# Spec-Kit Enhanced (or your chosen name)

**A fork of [GitHub Spec-Kit](https://github.com/github/spec-kit) with enhanced project rehabilitation features.**

## What's Different?

This fork extends the official Spec-Kit with:
- **Real security analysis** (Bandit, Safety integration)
- **Code quality metrics** (Radon, complexity analysis)
- **Project rehabilitation tools** (reverse engineering, auditing)
- **AI-enhanced workflows** (combines static analysis + AI review)

## Upstream Relationship

This project is based on GitHub's Spec-Kit but adds significant enhancements.
We periodically sync with upstream to get bug fixes and improvements.

To sync with upstream:
\`\`\`bash
git fetch upstream
git merge upstream/main
\`\`\`

## Original Spec-Kit

For the official, minimal Spec-Kit, see: https://github.com/github/spec-kit
```

### **Step 5: Add Fork Attribution**

Create a `ATTRIBUTION.md` file:

```markdown
# Attribution

This project is a fork of [GitHub Spec-Kit](https://github.com/github/spec-kit).

## Original Authors
- GitHub, Inc. and contributors
- Original repository: https://github.com/github/spec-kit
- License: MIT (see LICENSE file)

## Enhancements
Additional features and modifications by [Your Name/Team].

## License Compliance
This fork maintains the original MIT license and complies with all
attribution requirements.
```

### **Step 6: Update pyproject.toml**

```toml
[project]
name = "spec-kit-enhanced"  # or your chosen name
version = "0.1.0"  # Start fresh with your versioning
description = "Enhanced Spec-Kit with real code analysis and project rehabilitation tools"
# ... rest of config
```

---

## ✅ **OPTION 2: Create Standalone Project**

Choose this if you want **complete independence** from spec-kit.

### **Step 1: Extract Only What You Need**

```bash
# Create new project directory
mkdir -p ~/Projects/my-code-analyzer
cd ~/Projects/my-code-analyzer

# Copy only YOUR files (not upstream spec-kit)
cp -r /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit/src .
cp /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit/pyproject.toml .
cp /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit/tests .
cp /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit/ROADMAP_TO_LEGITIMACY.md .
cp /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit/QUICK_START_IMPLEMENTATION.md .

# Initialize NEW git repository
git init
git add .
git commit -m "Initial commit: Code analyzer tool"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/code-analyzer.git
git push -u origin main
```

### **Step 2: Remove Spec-Kit Branding**

- Rename CLI from `specify` to something else (e.g., `codeaudit`)
- Remove spec-kit specific features you don't need
- Write your own README from scratch
- Create your own identity

### **Step 3: Credit Original Inspiration**

In your README:

```markdown
## Inspiration

This project was inspired by [GitHub Spec-Kit](https://github.com/github/spec-kit)
but has been completely rewritten to focus on code analysis and security scanning.
```

---

## ✅ **OPTION 3: Contribute Upstream**

Choose this if you want your features in the **official spec-kit**.

**⚠️ BUT FIRST:** The official spec-kit maintainers might NOT want:
- Experimental rehabilitation features
- Heavy dependencies (Bandit, Safety, etc.)
- Features that increase complexity

### **Before Investing Time:**

1. **Open a GitHub Discussion:**
   ```
   Title: "Proposal: Add Project Rehabilitation Features"
   
   Hey team, I've built some enhancements to spec-kit that add:
   - Real security scanning (Bandit integration)
   - Code analysis tools
   - Project rehabilitation workflows
   
   Would this be in scope for the official project?
   If so, I can clean it up and submit a PR.
   ```

2. **Wait for Response:**
   - If YES → Clean up code, submit PR
   - If NO → Go with Option 1 (fork) instead

---

## 🔧 **FIXING THE NESTED DIRECTORY STRUCTURE**

Regardless of which option you choose, fix this:

```bash
# Current structure (WRONG):
# EventDeskPro/Spec-Kit-Rehabilitation/spec-kit/

# Move everything up to proper location
cd /Users/VScode_Projects/projects/
mv Spec-Kit-Rehabilitation/spec-kit spec-kit-enhanced  # or your chosen name
rm -rf Spec-Kit-Rehabilitation  # Remove empty wrapper

# Now you have:
# spec-kit-enhanced/
# ├── .git/
# ├── src/
# ├── tests/
# └── ...
```

---

## 📋 **RECOMMENDED ACTION PLAN**

### **For Your Situation, I Recommend Option 1 (Fork):**

**Why?**
- You want to use this across multiple projects
- You're building real enhancements
- You want to potentially share with others
- You might want to sync bug fixes from upstream

**Steps This Weekend:**

```bash
# 1. Create GitHub repo (on GitHub.com)
#    Name: "spec-kit-enhanced" or "spec-analyzer"

# 2. Update git remotes
cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit
git remote rename origin upstream
git remote add origin https://github.com/YOUR_USERNAME/spec-kit-enhanced.git

# 3. Commit your changes
git add .
git commit -m "Add rehabilitation and analysis features"
git push -u origin main

# 4. Fix directory structure
cd /Users/VScode_Projects/projects/
mv Spec-Kit-Rehabilitation/spec-kit spec-kit-enhanced
rm -rf Spec-Kit-Rehabilitation

# 5. Update README with fork attribution
# (see example above)
```

---

## 🎯 **AFTER FIXING THE REPOSITORY**

Once you have your own repo set up properly:

### **Syncing with Upstream (Optional)**

If you want bug fixes from official spec-kit:

```bash
# Fetch updates from official spec-kit
git fetch upstream

# Merge their changes into your branch
git merge upstream/main

# Resolve any conflicts
# Then push to your repo
git push origin main
```

### **Working on Features**

```bash
# Create feature branches
git checkout -b add-security-scanning
# ... make changes ...
git commit -m "Implement Bandit security scanner"
git push origin add-security-scanning

# Merge to main when ready
git checkout main
git merge add-security-scanning
git push origin main
```

---

## ⚠️ **LEGAL/LICENSE CONSIDERATIONS**

### **If You Fork (Option 1):**

✅ **You MUST:**
- Keep original MIT license
- Credit original authors
- Include attribution

✅ **You CAN:**
- Add your own features
- Use any name you want
- Charge for services/support (but code stays MIT)

❌ **You CANNOT:**
- Remove GitHub's copyright
- Claim you created the original
- Change the license without permission

### **If You Go Standalone (Option 2):**

If you use ANY code from spec-kit:
- ✅ Still must credit in ATTRIBUTION.md
- ✅ Still must keep MIT license on borrowed code
- ✅ Can add new code under different license

If you write EVERYTHING from scratch:
- ✅ Can use any license
- ✅ No attribution needed (but nice to credit inspiration)

---

## 🚀 **NEXT STEPS CHECKLIST**

After reading this, you need to:

- [ ] **Decide:** Option 1 (Fork), Option 2 (Standalone), or Option 3 (Upstream)
- [ ] **Create:** New GitHub repository with proper name
- [ ] **Update:** Git remotes to point to YOUR repo
- [ ] **Commit:** All your changes
- [ ] **Push:** To your repository
- [ ] **Fix:** Directory structure (flatten it)
- [ ] **Add:** Attribution and fork documentation
- [ ] **Update:** README with what's different
- [ ] **Update:** pyproject.toml with new name/version

**Time Required:** 30-60 minutes

---

## 💡 **MY SPECIFIC RECOMMENDATION FOR YOU**

Based on what you've told me:

1. **Choose Option 1 (Fork)** - You want to use across projects
2. **Name it:** "spec-kit-enhanced" or "spec-analyzer"
3. **Keep attribution:** It's the right thing to do + legally required
4. **Build the real tools:** Follow QUICK_START_IMPLEMENTATION.md
5. **Share it:** Once working, others might benefit

**This gives you:**
- ✅ Your own repository you control
- ✅ Ability to sync upstream fixes
- ✅ Proper setup for multiple projects
- ✅ Foundation for building real tools
- ✅ Legal compliance
- ✅ Good standing with open source community

---

## ❓ **QUESTIONS TO ASK YOURSELF**

1. **Do I want to contribute back to official spec-kit?**
   - YES → Try Option 3 first
   - NO → Option 1 or 2

2. **Will I build significant new features?**
   - YES → Option 1 (fork) or 2 (standalone)
   - NO → Just use official spec-kit

3. **Do I want to maintain sync with upstream?**
   - YES → Option 1 (fork)
   - NO → Option 2 (standalone)

4. **What should I name my project?**
   - Based on spec-kit: "spec-kit-enhanced", "spec-kit-pro"
   - Independent identity: "code-analyzer", "dev-auditor"

---

## 📞 **Ready to Fix This?**

Let me know which option you want and I'll walk you through the exact commands to run!

**Most likely you want Option 1 (Fork).** It's the cleanest approach for your use case.
