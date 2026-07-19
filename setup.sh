#!/bin/bash
# Setup script for tv-playlist-automation
# Run this after creating the empty repo on GitHub

echo "📺 TV Playlist Automation Setup"
echo "================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize repo if not already
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: TV Playlist Auto-Updater

- fetch_and_combine.py: Fetches, filters, deduplicates playlists
- GitHub Actions workflow: Auto-updates every 6 hours
- 300+ curated Tamil local channels
- README with full documentation"

# Add remote (replace with your actual URL if different)
git remote add origin https://github.com/nuttle-nuttterr/tv-playlist-automation.git

echo ""
echo "✅ Repository ready!"
echo ""
echo "Next steps:"
echo "  1. Create empty repo on GitHub: https://github.com/new"
echo "     Name: tv-playlist-automation"
echo "     ❌ Do NOT initialize with README (we already have one)"
echo ""
echo "  2. Push to GitHub:"
echo "     git push -u origin main"
echo ""
echo "  3. Enable GitHub Actions:"
echo "     Settings → Actions → General → Read and write permissions"
echo ""
echo "  4. Run workflow manually first time:"
echo "     Actions → Update M3U Playlist → Run workflow"
