# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Claude Code environment in this repo

This project's `.claude/settings.json` enforces some hard constraints (see
[.claude/README.md](.claude/README.md) for the full explanation, written for
newcomers to Claude Code):

- `git push` and `pip install`/`pip3 install` are **denied** outright — dependencies
  go through `uv add`/`uv sync`, and pushing is left to the user.
- `.env`/`.env.*` files and `*.pem` are **denied** for both read and write.
- `git rebase`/`git reset` always prompt for confirmation regardless of mode.
- A `PostToolUse` hook (`.claude/hooks/ruff-format.js`) runs `ruff check --fix` +
  `ruff format` on every file Claude writes or edits — don't hand-format Python,
  it happens automatically after each edit.
- `.claude/agents/code-quality-reviewer.md` is a subagent tuned to this pipeline's
  failure modes (data leakage, missing `random_state`, sklearn pitfalls); the
  built-in `/code-review` is more thorough for general review.
- `.claude/skills/pr-description/` provides a `/pr-description` skill that enforces
  a What/Why/Changes PR format from `git diff`.

## Commands

Dependency/environment management is via [uv](https://docs.astral.sh/uv/) — never use `pip` directly.
Most commands are wrapped in the `Makefile`; prefer `make <target>` when one exists.

```bash
make dev-install                           # uv sync + install pre-commit hooks
make train                                 # run the full ML pipeline (scripts/train_pipeline.py)
make run                                   # launch the Streamlit app (localhost:8501)
make run_api                               # launch the FastAPI app (localhost:8000)
make test                                  # uv run pytest tests/ -v
make test-fast                             # uv run pytest tests/ -x
make lint / make format                    # ruff check / ruff check --fix + format
make typecheck                             # uv run mypy --explicit-package-bases src/ app/
make check                                 # lint + typecheck + test (local CI)
uv run pytest tests/unit_test/test_train.py::test_train_model_fits_and_splits_data  # single test
make up / make down                        # docker-compose up/down (API + Streamlit)
uv run pre-commit run --all-files          # run the same hooks CI/commits would run
```

### Code style gotchas

Ruff (`pyproject.toml`, `line-length = 120`) enables the `D` (pydocstyle) and `ANN`
(flake8-annotations) rule sets across `src/`, `tests/`, and `app/` — not just `src/`.
Every function, including test functions and inner closures/monkeypatch stubs inside
tests, needs a docstring and full parameter/return type annotations, or `ruff check`
fails. `mypy --strict` additionally applies to `src/` and `app/` (not `tests/`). When
adding a function anywhere under those three trees, annotate and document it up front
rather than relying on ruff's `--fix` (most `ANN`/`D` violations have no autofix).

FastAPI's `TestClient` (via Starlette) in this environment requires the `httpx2`
package, not the more common `httpx` — it's already pinned in the `dev` dependency
group; if `uv sync` ever drops it, `tests/unit_test/test_api.py` and
`test_middleware.py` fail at collection time with a `RuntimeError`, not a normal
assertion failure.

## Architecture

Real installed package (`src` layout, `[tool.uv] package` is NOT set to false — unlike a plain
script project, `titanic_ml` is importable anywhere after `uv sync` thanks to the editable install).

Three delivery surfaces sit on top of one core:

- **`src/titanic_ml/core/`** — the actual ML pipeline, delivery-mechanism-agnostic:
  - `data_io/loader.py` — `load_data()` downloads/caches the Titanic CSV into `data/raw/` (via `RAW_DATA_DIR` from `core/utils/paths.py`).
  - `features/preprocessing.py` — `FEATURES` (= `NUMERIC_FEATURES + CATEGORICAL_FEATURES`) and `TARGET` are the single source of truth for which columns feed the model. `build_preprocessor()` returns a `ColumnTransformer` (impute+scale numeric, impute+one-hot categorical) driven entirely by those lists.
  - `models/train.py` — `build_model()` returns one sklearn `Pipeline` (preprocessor + `RandomForestClassifier`); `train_model()` does a stratified train/test split, 5-fold CV on the training set, then fits — returns `(model, X_test, y_test)` with the test set untouched until evaluation. `save_model()` writes to `MODELS_DIR` (`models/titanic_model.joblib`).
  - `models/evaluate.py` — `evaluate_model()` prints accuracy/ROC-AUC/classification report and saves the confusion matrix to `FIGURES_DIR` (`docs/figures/`).
  - `utils/paths.py` — every directory constant (`RAW_DATA_DIR`, `MODELS_DIR`, `FIGURES_DIR`, `LOGS_DIR`, ...) is derived from `PROJECT_ROOT`, found by walking up from `__file__` until a `pyproject.toml` is found. Add new shared paths here rather than hardcoding `Path(__file__).parent...` elsewhere.
  - `utils/version.py` — `get_project_version()` reads installed package metadata first, falls back to the `VERSION` file at repo root.
  - `features/`, `models/`, `data_io/`, `visualization/`, `front/` are all real subpackages; `visualization/` and `front/` are currently empty stubs reserved for future use.
- **`src/titanic_ml/api/`** — FastAPI app (`main.py` builds `app`, includes `routers/{base,greetings,system}.py`; `middlewares.py` has `LimitUploadSizeMiddleware` capping request size via `API_MAX_UPLOAD_SIZE`). Currently a generic skeleton (health/version/greetings) — it does not yet call into `core.models` for predictions.
- **`app/streamlit_app.py`** — generic Pygwalker-based CSV/Parquet/Excel explorer (upload any file, or point it at `data/raw/titanic.csv`). Not wired to the trained model either.
- **`scripts/train_pipeline.py`** — the only place that chains `data_io → features → models.train → models.evaluate` end to end; this is what `make train` runs. There is no root-level `main.py`.

Trained artifacts (`models/*.joblib`, `docs/figures/*.png`) and `data/{raw,interim,processed,external}/*` (except `.gitkeep`) are git-ignored and regenerated by `make train`.

Two CI configs exist but only one is live: `.github/workflows/ci.yml` runs on every push/PR.
`.gitlab-ci.yml` mirrors the same lint/typecheck/test/release stages but there is no GitLab
remote configured — it needs `CI_GIT_USERNAME`/`CI_GIT_TOKEN` CI variables to ever run the
`release` job, so don't assume it's exercised. No `LICENSE` file exists yet (deliberately
left unset, not an oversight).

## Testing conventions

`tests/unit_test/` holds all current tests (mirrors template categories `integration/` and `functional/` exist as empty placeholders for future use). Tests never hit the network or the real dataset:
- `tests/unit_test/conftest.py` provides a `titanic_df` fixture (60-row synthetic DataFrame shaped like the real dataset, including missing `Age`/`Embarked` values).
- `tests/unit_test/test_data_io.py` monkeypatches `titanic_ml.core.data_io.loader.RAW_DATA_DIR`/`DATA_PATH`/`urlretrieve` to test the download-vs-cache branches in isolation.
- `tests/unit_test/test_paths.py` monkeypatches the directory constants in `core.utils.paths` rather than touching the real filesystem.
- `tests/unit_test/test_api.py` / `test_middleware.py` use FastAPI's `TestClient` against the real `app` object — no network calls, everything is in-process ASGI.

Coverage is enforced via pytest config in `pyproject.toml` (`--cov=src --cov-fail-under=80`), scoped to `src/` only — `app/` (Streamlit) is not covered by the coverage gate.
