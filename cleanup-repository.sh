#!/bin/bash
# cleanup-repository.sh
# This script fixes the repository structure and removes unnecessary files

set -e  # Exit on error

echo "======================================"
echo "Repository Cleanup Script"
echo "======================================"
echo ""

# Check we're in the right place
if [ ! -f "STRUCTURE_ANALYSIS.md" ]; then
    echo "❌ Error: Please run this script from the spec-kit directory"
    echo "   cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Step 1: Remove unnecessary files
echo "🗑️  Step 1: Removing unnecessary files..."
rm -f .DS_Store
rm -f ../.DS_Store
rm -f HONEST_ASSESSMENT.md
rm -f README_FOR_USER.md
rm -f STRUCTURE_ANALYSIS.md
rm -f STRUCTURE_QUICK_ANSWER.md
echo "   ✅ Removed redundant documentation files"

# Step 2: Update .gitignore (add missing entries)
echo ""
echo "📝 Step 2: Updating .gitignore..."
if ! grep -q ".pytest_cache/" .gitignore 2>/dev/null; then
    cat >> .gitignore << 'EOF'

# Testing artifacts
.pytest_cache/
.coverage
htmlcov/
.tox/
*.cover
EOF
    echo "   ✅ Added testing artifacts to .gitignore"
else
    echo "   ℹ️  .gitignore already has testing artifacts"
fi

# Step 3: Show structure info
echo ""
echo "📊 Step 3: Repository structure analysis..."
echo ""
echo "Current nesting:"
echo "   /Spec-Kit-Rehabilitation/        ← Wrapper directory"
echo "   └── spec-kit/                    ← Actual project (you are here)"
echo ""
echo "⚠️  RECOMMENDATION: Flatten this structure"
echo ""
echo "To flatten (move everything up one level):"
echo "   cd .."
echo "   mv spec-kit/* ."
echo "   mv spec-kit/.* . 2>/dev/null || true"
echo "   rmdir spec-kit"
echo ""

# Step 4: Check for files to merge
echo "📋 Step 4: Files that need attention..."
echo ""

if [ -f "CHANGELOG-REHABILITATION.md" ]; then
    echo "   ⚠️  CHANGELOG-REHABILITATION.md exists"
    echo "      → Should be merged into CHANGELOG.md, then deleted"
fi

if [ -f "REHABILITATION-ENHANCEMENT-SUMMARY.md" ]; then
    echo "   ⚠️  REHABILITATION-ENHANCEMENT-SUMMARY.md exists"
    echo "      → Consider if this should be merged into PROJECT-REHABILITATION.md"
fi

echo ""
echo "✅ Step 5: Cleanup complete!"
echo ""
echo "📄 Files cleaned up:"
echo "   ✅ Removed .DS_Store files"
echo "   ✅ Removed redundant documentation (HONEST_ASSESSMENT.md, README_FOR_USER.md)"
echo "   ✅ Updated .gitignore"
echo ""
echo "📌 Next steps:"
echo "   1. Review STRUCTURE_ANALYSIS.md for detailed recommendations"
echo "   2. Consider flattening the directory structure (see above)"
echo "   3. Merge CHANGELOG-REHABILITATION.md into CHANGELOG.md"
echo "   4. Commit changes: git add -A && git commit -m 'Clean up repository structure'"
echo ""
echo "======================================"
echo "Cleanup Complete!"
echo "======================================"
