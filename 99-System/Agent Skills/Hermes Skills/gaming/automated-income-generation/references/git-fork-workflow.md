## Git Fork Workflow - Session Notes

### Problem
When trying to push local commits to the original MoneyPrinterV2 repository, received:
```
ERROR: Permission to FujiwaraChoki/MoneyPrinterV2.git denied to codysumpter-cloud.
fatal: Could not read from remote repository.
```

### Root Cause
The local repository was configured to push to the original repository where the user doesn't have write access.

### Solution Steps

1. **Fork the repository** (if not already done):
   ```bash
   gh repo fork FujiwaraChoki/MoneyPrinterV2 --clone=false
   ```
   This creates a fork at `https://github.com/codysumpter-cloud/MoneyPrinterV2`

2. **Change the remote URL** to point to your fork:
   ```bash
   git remote set-url origin git@github.com:codysumpter-cloud/MoneyPrinterV2.git
   ```

3. **Verify the remote**:
   ```bash
   git remote -v
   # Should show:
   # origin  git@github.com:codysumpter-cloud/MoneyPrinterV2.git (fetch)
   # origin  git@github.com:codysumpter-cloud/MoneyPrinterV2.git (push)
   ```

4. **Push your commits**:
   ```bash
   git push -u origin main
   ```

5. **To keep fork updated with original** (optional but recommended):
   ```bash
   # Add upstream remote
   git remote add upstream git@github.com:FujiwaraChoki/MoneyPrinterV2.git

   # Fetch upstream changes
   git fetch upstream

   # Merge upstream changes into your main branch
   git merge upstream/main
   ```

### Alternative: SSH Key Issues
If you encounter SSH key problems:
1. Check if your key is loaded: `ssh-add -l`
2. Add your key if needed: `ssh-add ~/.ssh/id_ed25519`
3. Verify GitHub access: `ssh -T git@github.com`

### Prevention
- Always check remote URLs before pushing: `git remote -v`
- When cloning a repository you plan to contribute to, consider forking first
- Use the GitHub CLI (`gh`) for common fork operations
