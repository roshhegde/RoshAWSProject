# Branching Strategy

Use this workflow for future changes:

## Branches
- main: production-ready code
- develop: integration branch for upcoming work
- feature/*: new features or changes
- hotfix/*: urgent fixes

## Recommended workflow
1. Start from develop:
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Create a feature branch:
   ```bash
   git checkout -b feature/my-change
   ```
3. Make commits and push the branch:
   ```bash
   git push -u origin feature/my-change
   ```
4. Open a pull request into develop.
5. After review, merge and delete the feature branch.

## Rules
- Do not commit directly to main or develop.
- Keep feature branches short-lived.
- Pull the latest develop branch before starting new work.
