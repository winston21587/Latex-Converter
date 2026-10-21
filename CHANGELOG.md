# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-21

### Added
- **Bidirectional Math Translation**:
  - LaTeX to clean Unicode text conversion (`$$..$$`, `$..$`, `\[..\]`, `\(..\)`).
  - Readable Unicode text to valid LaTeX formulas with automatic delimiters (`$$` and `$`).
  - Support for Greek alphabet, fractions (`\frac`, `\dfrac`, `\tfrac`), roots (`\sqrt`), sub/superscripts (`x²`, `y₁`), and relational symbols (`≈`, `≠`, `≤`, `≥`, `×`, `÷`, `±`, `∞`, etc.).
  - Text-block preservation (`\text{...}`, `\mathrm{...}`, `\mathbf{...}`).
- **Interactive Modern GUI**:
  - Built with Tkinter, featuring custom flat modern buttons and clean responsive layout.
  - Seamless Dark and Light theme switching with persistence.
  - Live character/word count and status indicator.
  - Convenient Swap, Copy, Paste, and Clear controls.
  - Per-monitor DPI awareness support for crisp rendering on Windows.
- **Command Line Interface (CLI)**:
  - Input file processing and optional `-o/--output` file destination.
  - `--reverse` flag for text-to-LaTeX conversion from terminal/scripts.
  - Unicode/UTF-8 stdout safety across Windows cp1252 and Unix terminals.
- **Packaging & Build Automation**:
  - One-click build scripts: `build_exe.bat` for Windows and `build_app.sh` for macOS/Linux.
  - PyInstaller spec configuration for standalone windowed executable creation.
- **Testing & CI**:
  - Full test suite via standard `unittest` covering conversion, roundtrip, and edge cases.
  - Cross-platform GitHub Actions CI matrix across Ubuntu, Windows, and macOS (Python 3.9 - 3.13).
  - Automated binary release workflow.
