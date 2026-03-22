# Bài 07: Git Mastery

## 🎯 Mục tiêu
- Branching strategies (Git Flow, Trunk-based)
- Rebase, cherry-pick, bisect
- Conventional commits, monorepo

---

## 1. Branching Strategies

### Trunk-Based Development ⭐ (recommended)
```
main ──●──●──●──●──●──●──●──●──●──
       │     ↑  │     ↑
       └─────┘  └─────┘
     short-lived  short-lived
     feature      feature
     branches     branches
     (< 1 day)   (< 1 day)

Rules:
- Feature branches live < 1-2 days
- All devs merge to main frequently
- Feature flags for incomplete features
- CI runs on every push to main
```

### Git Flow (for release-based products)
```
main     ──●──────────────●────────────●──
            \             / \          /
release     ─●───●───●──/   ●───●───●/
              \       /       \
develop  ●──●──●──●──●──●──●──●──●──●──
          \  /    \  /  \  /
feature   ─●──    ─●──  ─●──
```

---

## 2. Git Advanced Commands

```bash
# Interactive rebase — clean up commit history
git rebase -i HEAD~5
# pick, squash, reword, drop commits

# Cherry-pick specific commit
git cherry-pick abc123

# Bisect — find bug-introducing commit
git bisect start
git bisect bad              # current commit is bad
git bisect good v1.0        # v1.0 was good
# Git binary-searches commits, you test each one
git bisect good / git bisect bad
# → finds exact commit that introduced the bug

# Stash
git stash push -m "WIP: feature X"
git stash list
git stash pop

# Reflog — recover lost commits
git reflog
git checkout HEAD@{5}

# Blame — who wrote this line?
git blame src/app.py -L 50,60
```

---

## 3. Conventional Commits

```
Format: <type>(<scope>): <description>

Types:
  feat:     new feature
  fix:      bug fix
  docs:     documentation
  style:    formatting (no code change)
  refactor: code change that neither fixes nor adds feature
  perf:     performance improvement
  test:     adding tests
  chore:    maintenance (deps, CI)

Examples:
  feat(auth): add JWT refresh token rotation
  fix(payment): handle timeout in Stripe webhook
  refactor(order): extract pricing logic to domain service
  perf(search): add composite index for product search

Breaking change:
  feat(api)!: change pagination from offset to cursor-based

  BREAKING CHANGE: removed 'page' parameter, use 'cursor' instead
```

---

## 4. Commit Best Practices

```
✅ Atomic commits: 1 commit = 1 logical change
✅ Meaningful messages: explain WHY, not just WHAT
✅ Squash WIP commits before merge
✅ Never commit secrets/credentials

❌ "fix stuff", "WIP", "asdf"
❌ 1 giant commit with 50 files
❌ Mixing feature + refactor in same commit
```

---

## 📝 Bài tập

1. Practice interactive rebase: squash 5 commits into 2
2. Use git bisect to find a bug in codebase
3. Setup pre-commit hooks (commitlint, lint, format)
4. Create branching strategy document for your team

---

## 📚 Tài liệu
- *Pro Git* — Scott Chacon (free online)
- [Conventional Commits Spec](https://www.conventionalcommits.org/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
