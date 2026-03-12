# 🚀 GitHub Setup Instructions for AgroMart

Follow these steps to push your AgroMart project to GitHub.

## Step 1: Create a GitHub Repository

1. Go to https://github.com
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name:** AgroMart
   - **Description:** Agricultural marketplace platform with real-time market rates
   - **Visibility:** Public (or Private if you prefer)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Initialize Git in Your Project

Open Command Prompt or PowerShell in your project directory:

```bash
cd c:\Users\Yuvaraj\AgroMart
```

Initialize Git:
```bash
git init
```

## Step 3: Add All Files to Git

```bash
git add .
```

## Step 4: Create Your First Commit

```bash
git commit -m "Initial commit: AgroMart agricultural marketplace platform"
```

## Step 5: Connect to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/AgroMart.git
```

## Step 6: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

**Note:** You may be prompted to enter your GitHub credentials.

## Step 7: Verify Upload

1. Go to your GitHub repository: https://github.com/YOUR_USERNAME/AgroMart
2. You should see all your files uploaded!

---

## ⚠️ IMPORTANT: Before Pushing

### 1. Check .env File is NOT Included
```bash
git status
```

Make sure `.env` is NOT listed. It should be ignored by `.gitignore`.

### 2. Remove Sensitive Data from .env (if accidentally committed)

If you accidentally committed `.env`:
```bash
git rm --cached backend/.env
git commit -m "Remove .env file"
```

### 3. Update .env.example

Make sure `backend/.env.example` has placeholder values, not real credentials.

---

## 📝 After Pushing to GitHub

### 1. Update README.md
- Replace `YOUR_USERNAME` with your actual GitHub username
- Add your LinkedIn profile link
- Add your email address

### 2. Add Topics to Your Repository
On GitHub, click "Settings" → "About" → Add topics:
- `agriculture`
- `marketplace`
- `fastapi`
- `nextjs`
- `react`
- `postgresql`
- `mongodb`
- `kafka`
- `jwt-authentication`

### 3. Create a GitHub Pages Site (Optional)
You can deploy your frontend to GitHub Pages or Vercel.

### 4. Add Screenshots (Optional)
Create a `screenshots/` folder and add images:
- Homepage
- Live rates page
- Cart page
- Login page

---

## 🔄 Future Updates

When you make changes to your project:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with a message
git commit -m "Add: Description of what you changed"

# Push to GitHub
git push
```

---

## 🆘 Troubleshooting

### Problem: "fatal: remote origin already exists"
**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/AgroMart.git
```

### Problem: Authentication failed
**Solution:**
Use a Personal Access Token instead of password:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`
4. Copy the token
5. Use it as your password when pushing

### Problem: Large files error
**Solution:**
Check if you accidentally included `node_modules/` or `.next/`:
```bash
git rm -r --cached frontend/node_modules
git rm -r --cached frontend/.next
git commit -m "Remove large files"
```

---

## ✅ Checklist Before Pushing

- [ ] `.env` file is in `.gitignore`
- [ ] No sensitive data in committed files
- [ ] `.env.example` has placeholder values
- [ ] README.md is updated with your info
- [ ] All files are added (`git add .`)
- [ ] First commit is created
- [ ] Remote origin is set
- [ ] Ready to push!

---

## 🎉 Success!

Once pushed, share your repository:
- Add it to your resume
- Share on LinkedIn
- Add to your portfolio

**Repository URL:** https://github.com/YOUR_USERNAME/AgroMart

---

Need help? Open an issue or contact me!
