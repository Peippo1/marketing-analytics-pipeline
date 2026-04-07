# Release Checklist

Use this checklist before publishing or selling the repository as a downloadable product.

## Positioning

- README is consistent with the product positioning
- GitHub repository title, description, and About section match the README
- Product language is honest and does not overclaim production readiness

## Repository Hygiene

- No local virtual environments are tracked
- No generated model artifacts or processed data are tracked
- No `.DS_Store`, local caches, or temporary files are tracked
- `.gitignore` reflects Python, notebook, macOS, Airflow, and local artifact needs

## Demo Readiness

- `make setup` works on a clean machine
- `make demo` completes successfully
- `demo_outputs/latest/` contains expected files
- `make api` launches successfully
- `make dashboard` launches successfully

## Documentation

- README is up to date
- `PRODUCT.md` clearly explains buyer-facing value
- `DEPLOYMENT.md` reflects the current local and Docker setup
- `PROJECT_OVERVIEW.md` is aligned with the README
- `docs/DEMO_SCRIPT.md` is current
- `docs/SCREENSHOT_CHECKLIST.md` and `docs/SAMPLE_OUTPUTS.md` are still accurate

## Screenshots / Listing Assets

- At least one strong dashboard screenshot is captured
- API screenshot or sample response is ready
- Model training/evaluation output screenshot is ready
- `docs/assets/` contains the final screenshots or a clear asset plan
- Screenshots do not expose usernames, tokens, or local machine paths

## Trust / Quality

- Automated tests run cleanly
- CI status is green
- No obvious TODOs or debug noise remain in public-facing flows
- Example credentials are placeholders only

## Packaging

- License is present
- Downloaded archive opens with clean top-level structure
- Key docs are visible at the top level
- Listing copy and GitHub About text are aligned
- Branch history is trimmed and merged before release
