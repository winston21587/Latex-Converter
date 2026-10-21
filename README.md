# LaTeX Translator 📐✨

[![CI](https://github.com/tabotabowinston/latex-translator/actions/workflows/ci.yml/badge.svg)](https://github.com/tabotabowinston/latex-translator/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A fast, lightweight, bidirectional converter between **LaTeX math expressions** and **clean, readable Unicode text**.

Includes both an intuitive, modern **desktop GUI application** (with dark/light themes) and a scriptable **CLI** for batch pipelines. Zero external runtime dependencies required!

---

## 🌟 Features

- **🔄 Seamless Two-Way Conversion**:
  - **LaTeX $\to$ Readable Text**: Turns complex mathematical notation like `$$\sqrt{1^2 + 0^2}$$` into clean Unicode `√(1² + 0²)`.
  - **Readable Text $\to$ LaTeX**: Converts handwritten or copied plain math notation back into properly formatted LaTeX blocks (`$$` / `$`).
- **🖥️ Modern Desktop GUI**:
  - Clean, responsive dual-pane editor built with Python's native Tkinter.
  - One-click **Dark / Light mode** toggle with persistent configuration.
  - Quick **Swap Mode**, **Copy**, **Paste**, and **Clear** actions.
  - High-DPI support on Windows displays for crisp typography.
- **⚡ Scriptable CLI**:
  - Process text files directly: pipe output or save to disk.
  - Built-in UTF-8 safety ensuring proper rendering across Windows command prompts, PowerShell, and Unix shells.
- **📦 Zero External Runtime Dependencies**:
  - Uses only Python's standard library. Works immediately out of the box.
- **🚀 Standalone Executables**:
  - Ships with automated scripts to compile into a single `.exe` (Windows) or native binary (macOS/Linux) via PyInstaller.

---

## 📸 Preview

```
┌────────────────────────────────────────────────────────────────────────┐
│  LaTeX Translator                                    [☀️ Light] [⇄ Swap]│
├────────────────────────────────────┬───────────────────────────────────┤
│ LaTeX Input                        │ Readable Output                   │
│                                    │                                   │
│  $$\text{Length} = 1.414$$         │  Length = 1.414                   │
│  $$\frac{dx}{\text{len}} \approx   │  dx/len ≈ 0.7071                  │
│  0.7071$$                          │                                   │
├────────────────────────────────────┴───────────────────────────────────┤
│ [Translate]  [📋 Copy]  [📥 Paste]  [🧹 Clear]            Status: Ready │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Requirements

- Python 3.9+ installed.
- *Linux users only*: If Tkinter isn't installed in your minimal Python environment:
  ```bash
  sudo apt install python3-tk
  ```

### 2. Launch the GUI

Simply run:
```bash
python latex_to_text.py
```

### 3. Use via Command Line (CLI)

- **Convert LaTeX file to readable Unicode text:**
  ```bash
  python latex_to_text.py input.txt
  ```

- **Save output directly to a file:**
  ```bash
  python latex_to_text.py input.txt -o output.txt
  ```

- **Reverse conversion (Readable text $\to$ LaTeX):**
  ```bash
  python latex_to_text.py input.txt --reverse
  python latex_to_text.py input.txt -r -o math.tex
  ```

---

## 🧮 Supported Syntax & Conversions

| Type | LaTeX Input | Converted Unicode |
| :--- | :--- | :--- |
| **Fractions** | `\frac{a}{b}`, `\dfrac{1}{2}` | `a/b`, `1/2` |
| **Roots** | `\sqrt{x}`, `\sqrt{1^2 + 0^2}` | `√x`, `√(1² + 0²)` |
| **Powers** | `x^2`, `x^{12}` | `x²`, `x¹²` |
| **Subscripts** | `y_1`, `a_{ij}` | `y₁`, `a_ij` |
| **Greek Letters** | `\alpha`, `\beta`, `\pi`, `\theta`, `\Sigma` | `α`, `β`, `π`, `θ`, `Σ` |
| **Relations** | `\approx`, `\neq`, `\leq`, `\geq` | `≈`, `≠`, `≤`, `≥` |
| **Operators** | `\times`, `\cdot`, `\div`, `\pm`, `\int`, `\partial` | `×`, `·`, `÷`, `±`, `∫`, `∂` |
| **Text Labels** | `\text{Length}`, `\mathrm{dx}` | `Length`, `dx` |
| **Enclosures** | `$$...$$`, `$...$`, `\[...\]`, `\(...\)` | Clean formatted text block |

---

## 🛠️ Building Standalone Binaries

Distribute the application as a standalone executable without requiring users to have Python installed:

### Windows (`.exe`)
Run the bundled batch script:
```cmd
build_exe.bat
```
Your standalone binary will be generated at:
```
dist\LaTeX Translator.exe
```

### macOS / Linux
Run the shell script:
```bash
chmod +x build_app.sh
./build_app.sh
```
The executable will be located in the `dist/` directory.

---

## 🧪 Testing

The project uses Python's built-in `unittest` framework (also compatible with `pytest`):

```bash
# Run unit tests with standard unittest
python -m unittest discover -s tests -v

# Or with pytest (if installed)
pytest -v
```

---

## 📂 Project Structure

```
.
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # Multi-OS test matrix (Ubuntu, Windows, macOS)
│   │   └── release.yml          # Automated PyInstaller packaging workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── tests/
│   ├── __init__.py
│   └── test_translator.py       # Unit test suite
├── .gitattributes               # Cross-platform line endings configuration
├── .gitignore                   # Ignores build/, dist/, caches, and temp files
├── build_app.sh                 # macOS / Linux PyInstaller build script
├── build_exe.bat                # Windows PyInstaller build script
├── CHANGELOG.md                 # Version release history
├── CONTRIBUTING.md              # Contribution guidelines
├── input.txt                    # Sample test input file
├── latex_to_text.py             # Main application (GUI + CLI converter)
├── LaTeX Translator.spec        # PyInstaller specification file
├── LICENSE                      # MIT License
├── pyproject.toml               # PEP 517/621 package metadata & config
├── requirements.txt             # Runtime requirements (Standard Library)
└── requirements-dev.txt         # Development & packaging dependencies
```

---

## 🤝 Contributing

Contributions are warmly welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on setting up your environment, running tests, and submitting pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) © 2026 Winston.
