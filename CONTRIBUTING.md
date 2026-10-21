# Contributing to LaTeX Translator

Thank you for your interest in contributing to **LaTeX Translator**! We welcome bug fixes, documentation improvements, symbol additions, and UI enhancements.

---

## 🛠️ Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tabotabowinston/latex-translator.git
   cd latex-translator
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

---

## 🧪 Running Tests

Run the test suite using Python's built-in `unittest`:
```bash
python -m unittest discover -s tests -v
```

Or using `pytest`:
```bash
pytest -v
```

---

## 🚀 Running Locally

- **Launch the GUI:**
  ```bash
  python latex_to_text.py
  ```

- **Run CLI translation:**
  ```bash
  python latex_to_text.py input.txt
  python latex_to_text.py input.txt --reverse
  ```

---

## 📦 Building Standalone Binaries

- **Windows:** Run `build_exe.bat` or:
  ```cmd
  python -m PyInstaller "LaTeX Translator.spec"
  ```

- **macOS / Linux:** Run `build_app.sh` or:
  ```bash
  chmod +x build_app.sh
  ./build_app.sh
  ```

---

## 📝 Pull Request Guidelines

1. Fork the repo and create a descriptive branch: `git checkout -b feature/new-math-symbol`.
2. Add appropriate tests in `tests/test_translator.py`.
3. Verify all tests pass locally.
4. Commit your changes with clear messages (`git commit -m "Add support for partial derivatives"`).
5. Open a Pull Request referencing any open issue.
