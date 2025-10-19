# Step-by-Step: Fork spec-kit into EventDeskPro

**Your Situation:**
- ✅ You own: `https://github.com/Kxd395/EventDeskPro`
- ✅ You want to: Fork GitHub's spec-kit into it
- ✅ You want to: Add your rehabilitation features

---

## 🚀 QUICK SETUP (Copy-Paste These Commands)

### **Step 1: Update Git Remotes** (2 minutes)

```bash
cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit

# Rename current remote from 'origin' to 'upstream'
# (This keeps the link to GitHub's official spec-kit)
git remote rename origin upstream

# Add YOUR EventDeskPro repository as 'origin'
git remote add origin https://github.com/Kxd395/EventDeskPro.git

# Verify it worked
git remote -v
```

**You should see:**
```
origin    https://github.com/Kxd395/EventDeskPro.git (fetch)
origin    https://github.com/Kxd395/EventDeskPro.git (push)
upstream  https://github.com/github/spec-kit.git (fetch)
upstream  https://github.com/github/spec-kit.git (push)
```

### **Step 2: Commit Your New Files** (3 minutes)

```bash
# Add all your new files to git
git add .

# Create a commit with all your enhancements
git commit -m "Fork spec-kit and add rehabilitation features

- Add real security scanning capabilities (Bandit, Safety)
- Create roadmap for building legitimate analysis tools
- Add honest assessment and limitations documentation
- Include quick start implementation guide
- Enhance with project rehabilitation templates
- Add comprehensive testing infrastructure"

# Check the status
git status
```

### **Step 3: Push to YOUR Repository** (1 minute)

```bash
# Push to EventDeskPro
git push -u origin main
```

**If it asks for credentials:** Use your GitHub personal access token

### **Step 4: Update README** (5 minutes)

Let's make it clear this is a fork with enhancements:

```bash
# Open README in editor
code README.md
```

Add this at the very top:

```markdown
# EventDeskPro - Enhanced Spec-Kit

**A fork of [GitHub Spec-Kit](https://github.com/github/spec-kit) with enhanced project rehabilitation and code analysis features.**

[![Based on Spec-Kit](https://img.shields.io/badge/based%20on-spec--kit-blue)](https://github.com/github/spec-kit)

---

## 🎯 What's Different from Original Spec-Kit?

This fork extends the official Spec-Kit with:

- **🔒 Real Security Analysis** - Bandit and Safety integration (not just AI prompts)
- **📊 Code Quality Metrics** - Radon complexity analysis
- **🔄 Project Rehabilitation** - Tools for analyzing and improving existing projects
- **🤖 AI-Enhanced Workflows** - Combines static analysis with AI review
- **✅ Comprehensive Testing** - Tests with vulnerable code samples

## 🚀 For Original Spec-Kit Users

If you just want the standard Spec-Kit functionality, this fork is 100% compatible.
All original features work exactly as documented in the [official repo](https://github.com/github/spec-kit).

## 🔧 Enhanced Features (Experimental)

The project rehabilitation features are experimental but functional:
- `/speckit.audit` - Real security scanning using Bandit
- `/speckit.reverse-engineer` - Generate specs from existing code
- `/speckit.upgrade` - Modernize existing specifications
- See [ROADMAP_TO_LEGITIMACY.md](ROADMAP_TO_LEGITIMACY.md) for full implementation plan

---

# 📖 Original Spec-Kit Documentation

*The documentation below is from the original spec-kit project...*
```

Then save and commit:

```bash
git add README.md
git commit -m "Update README to clarify this is an enhanced fork"
git push origin main
```

### **Step 5: Add Attribution File** (2 minutes)

```bash
# Create attribution file
cat > ATTRIBUTION.md << 'EOF'
# Attribution

## Original Project

This project is a **fork** of [GitHub Spec-Kit](https://github.com/github/spec-kit).

- **Original Authors:** GitHub, Inc. and contributors
- **Original Repository:** https://github.com/github/spec-kit
- **Original License:** MIT License

## Enhancements

Additional features and modifications by:
- **Repository:** https://github.com/Kxd395/EventDeskPro
- **Enhancements:**
  - Real security analysis integration (Bandit, Safety)
  - Code quality metrics (Radon)
  - Project rehabilitation workflows
  - Comprehensive testing infrastructure
  - Enhanced documentation and roadmaps

## License Compliance

This fork maintains the original MIT license from GitHub Spec-Kit.
All enhancements are also released under the MIT license.

See [LICENSE](LICENSE) file for full license text.
EOF

git add ATTRIBUTION.md
git commit -m "Add attribution to original spec-kit project"
git push origin main
```

### **Step 6: Update pyproject.toml** (2 minutes)

```bash
code pyproject.toml
```

Change these lines:

```toml
[project]
name = "eventdesk-speckit"  # or "spec-kit-enhanced"
version = "0.1.0"  # Start with your own versioning
description = "Enhanced Spec-Kit with real code analysis and project rehabilitation - Fork of github/spec-kit"
# Keep the rest...
```

Commit:

```bash
git add pyproject.toml
git commit -m "Update project metadata for fork"
git push origin main
```

---

## ✅ **DONE! Verify Everything Works**

### Check on GitHub:

1. Go to: `https://github.com/Kxd395/EventDeskPro`
2. You should see all your files
3. You should see your commit messages
4. README should show it's a fork

### Verify Git Setup:

```bash
git remote -v
# Should show:
# origin    https://github.com/Kxd395/EventDeskPro.git
# upstream  https://github.com/github/spec-kit.git

git log --oneline -5
# Should show your new commits on top
```

---

## 🔄 **FUTURE: Syncing with Upstream**

Whenever GitHub updates the official spec-kit with bug fixes:

```bash
# Fetch updates from official spec-kit
git fetch upstream

# See what changed
git log HEAD..upstream/main --oneline

# Merge their changes into your fork
git merge upstream/main

# Resolve any conflicts if needed
# Then push to your repo
git push origin main
```

---

## 📁 **BONUS: Fix Directory Structure**

After everything is pushed, clean up the nested structure:

```bash
# Move to parent directory
cd /Users/VScode_Projects/projects/

# Rename to something clearer
mv Spec-Kit-Rehabilitation/spec-kit EventDeskPro-SpecKit

# Remove empty wrapper
rm -rf Spec-Kit-Rehabilitation

# Now you have clean structure:
# EventDeskPro-SpecKit/
# ├── .git/
# ├── src/
# ├── tests/
# └── ...
```

---

## 🎯 **SUMMARY**

After running these commands, you'll have:

- ✅ **EventDeskPro** properly set as your repository
- ✅ **Upstream link** to GitHub's spec-kit for updates
- ✅ **All your changes** committed and pushed
- ✅ **Clear attribution** to original project
- ✅ **Updated documentation** explaining the fork

**Total Time:** ~15 minutes

---

## ❓ **TROUBLESHOOTING**

### "Permission denied" when pushing

You need a GitHub Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo` (all checkboxes)
4. Copy the token
5. When git asks for password, paste the token

### "EventDeskPro already has content"

That's OK! The push will merge your local files with whatever is there.

If you want to start fresh:
```bash
git push -f origin main  # Force push (WARNING: overwrites remote)
```

### "Already up to date" when syncing upstream

That's good! It means you have all the latest changes.

---

## 🚀 **READY TO RUN?**

Just copy-paste the commands from each step in order!

Start with Step 1 (Update Git Remotes) right now. 👇
