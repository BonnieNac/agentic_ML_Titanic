# Contributing Guidelines

Thank you for your interest in contributing to this project! 🎉
We welcome contributions of all kinds — whether it's fixing bugs, improving documentation, suggesting new features, or writing code.

---

## How to Contribute

1. **Fork the repository**
2. **Clone your fork**

   ```bash
   git clone <repo-url>
   cd titanic_ml
   ```

3. **Create a new branch**

   ```bash
   git checkout -b feature/my-new-feature
   ```

4. **Make your changes**

   * Follow the [Coding Standards](#coding-standards) below.
   * Make sure your code is properly tested.

5. **Commit your changes**

   Use commitizen to enforce conventional commits:

   ```bash
   uv run cz c
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/my-new-feature
   ```

7. **Open a Pull Request (PR)**
   Describe your changes clearly using the PR template.

---

## Coding Standards

* Use clear, consistent naming conventions.
* Write clean, readable, and well-documented code.
* Keep functions small and focused.
* Run `make check` before submitting a PR / MR.

## Pre-commit hooks

Install the hooks once per clone:

```bash
uv run pre-commit install
```

They then run automatically on every commit (ruff, mypy, notebook output stripping,
basic file hygiene checks). Run them manually on the whole repo with:

```bash
uv run pre-commit run --all-files
```

---

## Tests

* Make sure that existing tests pass before submitting a PR / MR (`make test`).
* Add new tests if your changes add new functionality.

## Communication

* Use GitHub / GitLab Issues to report bugs or request features.
* Be respectful and constructive in discussions.

---

## Thank You!

Your contributions make this project better. We really appreciate your time and effort!
