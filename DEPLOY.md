# Deployment Guide

## Quick Deploy to GitHub

Your repository is already initialized and configured with:
- Remote: https://github.com/Krisha2000/Gandhinagar-Comic-AI.git
- Branch: main
- All files committed locally

### Step 1: Get GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name (e.g., "Gandhinagar Comic AI")
4. Select scope: **repo** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

### Step 2: Push to GitHub

Run this command in the terminal:

```bash
git push -u origin main
```

When prompted:
- **Username**: `Krisha2000`
- **Password**: Paste your Personal Access Token (not your GitHub password)

### Alternative: Use SSH (Recommended for future)

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. Add to GitHub: https://github.com/settings/keys
3. Change remote to SSH:
   ```bash
   git remote set-url origin git@github.com:Krisha2000/Gandhinagar-Comic-AI.git
   git push -u origin main
   ```

## After Deployment

Your code will be live at:
https://github.com/Krisha2000/Gandhinagar-Comic-AI

Remember to keep your `.env` file (in `Gandhinagar_Comic_AI_Secrets`) private!
