# 🚀 Quick GitHub Commands Reference

## Initial Setup (One-time only)

```bash
# Navigate to project
cd c:\Users\Yuvaraj\AgroMart

# Initialize Git (ALREADY DONE ✅)
git init

# Add all files (ALREADY DONE ✅)
git add .

# Create first commit
git commit -m "Initial commit: AgroMart agricultural marketplace platform"

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AgroMart.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Daily Git Commands (After making changes)

```bash
# Check what changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push
```

---

## Useful Git Commands

```bash
# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# View remote URL
git remote -v
```

---

## Commit Message Examples

```bash
git commit -m "Add: User profile page"
git commit -m "Fix: Cart total calculation bug"
git commit -m "Update: README with installation steps"
git commit -m "Refactor: Authentication logic"
git commit -m "Docs: Add API documentation"
```

---

## ⚠️ Important Notes

1. **NEVER commit .env file** - It's already in .gitignore ✅
2. **Always pull before push** if working with others
3. **Write clear commit messages** - Explain what and why
4. **Commit often** - Small, focused commits are better

---

## 🆘 Emergency Commands

### Accidentally committed .env file?
```bash
git rm --cached backend/.env
git commit -m "Remove .env file"
git push
```

### Want to start over?
```bash
rm -rf .git
git init
git add .
git commit -m "Fresh start"
```

### Wrong remote URL?
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/AgroMart.git
```

---

## 📝 Next Steps After First Push

1. ✅ Verify files on GitHub
2. ✅ Add repository description
3. ✅ Add topics/tags
4. ✅ Update README with your info
5. ✅ Star your own repo 😄
6. ✅ Share on LinkedIn

---

**Your Repository URL:** https://github.com/YOUR_USERNAME/AgroMart

Good luck! 🌾🚀
