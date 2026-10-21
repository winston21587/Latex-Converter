#!/usr/bin/env python3
"""
LaTeX Translator
================
Two-way converter between LaTeX math and readable Unicode text.

    LaTeX -> Text :  $$\\sqrt{1^2 + 0^2}$$   ->   √(1² + 0²)
    Text -> LaTeX :  √(1² + 0²)             ->   $$\\sqrt{1^2 + 0^2}$$

Usage:
    python latex_to_text.py                       # opens the GUI
    python latex_to_text.py input.txt             # CLI: LaTeX -> text
    python latex_to_text.py input.txt --reverse   # CLI: text -> LaTeX
    python latex_to_text.py input.txt -o out.txt
"""
import re
import sys
import json
import argparse
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, font as tkfont
except ImportError:  # CLI still works without tkinter
    tk = None

# ═════════════════════════════════════════════════════════════════════════════
#  LaTeX  ->  readable text
# ═════════════════════════════════════════════════════════════════════════════
SYMBOLS = {
    "approx": "≈", "neq": "≠", "ne": "≠", "leq": "≤", "le": "≤",
    "geq": "≥", "ge": "≥", "times": "×", "cdot": "·", "div": "÷",
    "pm": "±", "mp": "∓", "infty": "∞", "pi": "π", "theta": "θ",
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "Delta": "Δ",
    "lambda": "λ", "mu": "μ", "sigma": "σ", "Sigma": "Σ", "omega": "ω",
    "phi": "φ", "rightarrow": "→", "to": "→", "leftarrow": "←",
    "Rightarrow": "⇒", "sum": "Σ", "int": "∫", "partial": "∂",
    "degree": "°", "circ": "°", "left": "", "right": "", "quad": "  ",
    "qquad": "    ", "ldots": "…", "dots": "…",
}

SUP_PLAIN, SUP_UNI = "0123456789+-=()ni", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ"
SUB_PLAIN, SUB_UNI = "0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
SUPERSCRIPT = str.maketrans(SUP_PLAIN, SUP_UNI)
SUBSCRIPT = str.maketrans(SUB_PLAIN, SUB_UNI)
SIMPLE = re.compile(r"[\w.]+")
TEXT_CMDS = {"text", "mathrm", "mathbf", "mathit", "operatorname", "textbf"}


def read_group(s, i):
    """Read an argument starting at s[i]. Returns (content, next_index)."""
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s):
        return "", i
    if s[i] != "{":
        return s[i], i + 1
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def wrap(x):
    return x if SIMPLE.fullmatch(x) else f"({x})"


def script(x, table, marker):
    converted = x.translate(table)
    if all(c in table or c.isdigit() for c in x) and converted != x:
        return converted
    return marker + wrap(x)


def convert(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)", s[i:])
            if m:
                name = m.group(1)
                i += len(m.group(0))
                if name in TEXT_CMDS:
                    arg, i = read_group(s, i)
                    out.append(convert(arg))
                elif name == "sqrt":
                    arg, i = read_group(s, i)
                    out.append("√" + wrap(convert(arg)))
                elif name in ("frac", "dfrac", "tfrac"):
                    num, i = read_group(s, i)
                    den, i = read_group(s, i)
                    out.append(f"{wrap(convert(num))}/{wrap(convert(den))}")
                else:
                    out.append(SYMBOLS.get(name, name))
            else:
                nxt = s[i + 1] if i + 1 < len(s) else ""
                out.append(" " if nxt in ",;:!" else nxt)
                i += 2
        elif c == "^":
            arg, i = read_group(s, i + 1)
            out.append(script(convert(arg), SUPERSCRIPT, "^"))
        elif c == "_":
            arg, i = read_group(s, i + 1)
            out.append(script(convert(arg), SUBSCRIPT, "_"))
        elif c in "{}":
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def translate_text(text):
    """Replace every math block ($$..$$, $..$, \\[..\\], \\(..\\)) with plain text."""
    def sub(m):
        return convert(m.group(1)).strip()
    text = re.sub(r"\$\$(.+?)\$\$", sub, text, flags=re.S)
    text = re.sub(r"\\\[(.+?)\\\]", sub, text, flags=re.S)
    text = re.sub(r"\\\((.+?)\\\)", sub, text, flags=re.S)
    text = re.sub(r"\$(.+?)\$", sub, text, flags=re.S)
    return text


# ═════════════════════════════════════════════════════════════════════════════
#  readable text  ->  LaTeX
# ═════════════════════════════════════════════════════════════════════════════
REVERSE = {
    "≈": r"\approx", "≠": r"\neq", "≤": r"\leq", "≥": r"\geq",
    "×": r"\times", "·": r"\cdot", "÷": r"\div", "±": r"\pm", "∓": r"\mp",
    "∞": r"\infty", "π": r"\pi", "θ": r"\theta", "α": r"\alpha",
    "β": r"\beta", "γ": r"\gamma", "δ": r"\delta", "Δ": r"\Delta",
    "λ": r"\lambda", "μ": r"\mu", "σ": r"\sigma", "Σ": r"\Sigma",
    "ω": r"\omega", "φ": r"\phi", "→": r"\rightarrow", "←": r"\leftarrow",
    "⇒": r"\Rightarrow", "∂": r"\partial", "∫": r"\int", "°": r"^\circ",
    "…": r"\ldots",
}
FUNCS = {"sin", "cos", "tan", "cot", "sec", "csc", "log", "ln", "exp", "min", "max", "lim"}
SUP_REV = dict(zip(SUP_UNI, SUP_PLAIN))
SUB_REV = dict(zip(SUB_UNI, SUB_PLAIN))
STRONG = set("√=") | set(REVERSE) - {"·", "…", "°"} | set(SUP_UNI) | set(SUB_UNI)
PURE = set("0123456789.()+-*/^=<>,[]abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
ATOM = r"(?:\\text\{[A-Za-z]+\}|\([^()]*\)|[\w.^]+)"
SQRT_ARG = re.compile(r"\\text\{[A-Za-z]+\}|[\w.^]+")


def _brace(x):
    return x if len(x) == 1 else "{" + x + "}"


def _unparen(x):
    return x[1:-1] if x.startswith("(") and x.endswith(")") else x


def _sqrt_pass(s):
    out, i = [], 0
    while i < len(s):
        if s[i] != "√":
            out.append(s[i])
            i += 1
            continue
        j = i + 1
        if j < len(s) and s[j] == "(":
            depth, k = 0, j
            while k < len(s):
                if s[k] == "(":
                    depth += 1
                elif s[k] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            inner, i = s[j + 1:k], k + 1
        else:
            m = SQRT_ARG.match(s[j:])
            inner = m.group(0) if m else ""
            i = j + len(inner)
        out.append(r"\sqrt{" + _sqrt_pass(inner) + "}")
    return "".join(out)


def to_latex_expr(src):
    """Convert one readable math expression to LaTeX (no $ delimiters)."""
    # 1. words: functions -> \sin, other words (3+ letters) -> \text{word}
    def word(m):
        w = m.group(1)
        return "\\" + w if w in FUNCS else "\\text{" + w + "}"
    s = re.sub(r"(?<![A-Za-z\\])([A-Za-z]{3,})(?![A-Za-z])", word, src)

    # 2. superscripts / subscripts
    s = re.sub("[" + re.escape(SUP_UNI) + "]+",
               lambda m: "^" + _brace("".join(SUP_REV[c] for c in m.group())), s)
    s = re.sub("[" + re.escape(SUB_UNI) + "]+",
               lambda m: "_" + _brace("".join(SUB_REV[c] for c in m.group())), s)

    # 3. symbols (add a space after a command if a letter/digit follows)
    cur = s
    s = re.sub("[" + re.escape("".join(REVERSE)) + "]",
               lambda m: REVERSE[m.group()] +
               (" " if m.end() < len(cur) and cur[m.end()].isalnum() else ""), cur)

    # 4. fractions  a/b -> \frac{a}{b}
    s = re.sub(r"(?<![\w.^})\\])(" + ATOM + ")/(" + ATOM + r")(?![\w.^{(])",
               lambda m: r"\frac{" + _unparen(m.group(1)) + "}{" + _unparen(m.group(2)) + "}", s)

    # 5. square roots
    return _sqrt_pass(s)


def _convert_plain(p, display):
    toks = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", p)]
    n = len(toks)
    strong = [any(c in STRONG for c in t[2]) for t in toks]
    used = [False] * n

    def is_word(t):
        return re.fullmatch(r"[A-Za-z]{2,}", t.strip(".,;:!?()[]\"'")) is not None

    def pure(t):
        return all(c in PURE for c in t)

    def adjacent(a, b):
        return "\n" not in p[toks[a][1]:toks[b][0]]

    spans = []
    for i in range(n):
        if not strong[i] or used[i]:
            continue
        lo = hi = i
        while lo > 0 and not used[lo - 1] and adjacent(lo - 1, lo):
            t = toks[lo - 1][2]
            if is_word(t):
                if toks[lo][2].startswith("="):
                    lo -= 1  # "Length =" : keep the label, then stop
                break
            if pure(t):
                lo -= 1
            else:
                break
        while hi < n - 1 and adjacent(hi, hi + 1):
            t = toks[hi + 1][2]
            if strong[hi + 1] or (pure(t) and not is_word(t)):
                hi += 1
            else:
                break
        for k in range(lo, hi + 1):
            used[k] = True
        spans.append((toks[lo][0], toks[hi][1]))

    out, pos = [], 0
    for start, end in spans:
        seg = p[start:end]
        while seg and (seg[-1] in ".,;:!?" or (seg[-1] == ")" and seg.count(")") > seg.count("("))):
            seg = seg[:-1]
        end = start + len(seg)
        if not re.search(r"[A-Za-z0-9]", seg):
            continue
        delim = "$$" if display and any(c in seg for c in "=≈≠≤≥") else "$"
        out.append(p[pos:start])
        out.append(delim + to_latex_expr(seg) + delim)
        pos = end
    out.append(p[pos:])
    return "".join(out)


def text_to_latex(text, display=True):
    """Find math-looking expressions in plain text and rewrite them as LaTeX.
    Code in `backticks` and existing $...$ math are left untouched."""
    parts = re.split(r"(`[^`]*`|\$\$.+?\$\$|\$[^$\n]+\$)", text, flags=re.S)
    return "".join(p if i % 2 else _convert_plain(p, display) for i, p in enumerate(parts))


# ═════════════════════════════════════════════════════════════════════════════
#  GUI
# ═════════════════════════════════════════════════════════════════════════════
CONFIG = Path.home() / ".latex_translator.json"

PALETTES = {
    "dark": dict(bg="#16171d", panel="#1f212b", text_bg="#1a1c25", fg="#e8e9f1",
                 muted="#8c8fa5", accent="#6d8dff", accent_hover="#839dff",
                 accent_fg="#ffffff", border="#2e3140", btn="#2a2d3b",
                 btn_hover="#363a4d", select="#34437f"),
    "light": dict(bg="#f1f2f7", panel="#ffffff", text_bg="#ffffff", fg="#1b1d29",
                  muted="#6a6e84", accent="#4a67e8", accent_hover="#5f79ee",
                  accent_fg="#ffffff", border="#d5d8e4", btn="#e6e8f2",
                  btn_hover="#d8dcee", select="#c7d2ff"),
}


def load_cfg():
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cfg(d):
    try:
        CONFIG.write_text(json.dumps(d), encoding="utf-8")
    except Exception:
        pass


class Btn(tk.Label if tk else object):
    """Flat label-based button (themes properly on every OS)."""

    def __init__(self, parent, app, text, command, kind="normal", padx=14, pady=6):
        super().__init__(parent, text=text, padx=padx, pady=pady,
                         cursor="hand2", font=app.f_ui_bold)
        self.app, self.cmd, self.kind, self.hover = app, command, kind, False
        self.bind("<Enter>", lambda e: self._hover(True))
        self.bind("<Leave>", lambda e: self._hover(False))
        self.bind("<Button-1>", lambda e: self.cmd())
        app.buttons.append(self)
        self.restyle()

    def _hover(self, v):
        self.hover = v
        self.restyle()

    def set_kind(self, kind):
        self.kind = kind
        self.restyle()

    def restyle(self):
        P = self.app.P
        if self.kind == "accent":
            base, hov, fg = P["accent"], P["accent_hover"], P["accent_fg"]
        else:
            base, hov, fg = P["btn"], P["btn_hover"], P["fg"]
        self.configure(bg=hov if self.hover else base, fg=fg)


class App:
    MODES = {
        "l2t": ("LaTeX input", "Readable output"),
        "t2l": ("Readable input", "LaTeX output"),
    }

    def __init__(self):
        if sys.platform == "win32":
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass

        self.cfg = load_cfg()
        self.theme = self.cfg.get("theme", "dark")
        if self.theme not in PALETTES:
            self.theme = "dark"
        self.mode = self.cfg.get("mode", "l2t")
        if self.mode not in self.MODES:
            self.mode = "l2t"
        self.buttons, self.registry = [], []

        self.root = root = tk.Tk()
        root.title("LaTeX Translator")
        root.geometry("1060x620")
        root.minsize(780, 460)
        self.display_var = tk.BooleanVar(value=self.cfg.get("display", True))
        self.status = tk.StringVar()
        self.count = tk.StringVar()

        fams = set(tkfont.families())
        pick = lambda opts, default: next((f for f in opts if f in fams), default)
        ui = pick(["Segoe UI", "SF Pro Text", "Helvetica Neue", "Ubuntu", "DejaVu Sans"],
                  tkfont.nametofont("TkDefaultFont").actual("family"))
        mono = pick(["Cascadia Code", "Consolas", "Menlo", "DejaVu Sans Mono"],
                    tkfont.nametofont("TkFixedFont").actual("family"))
        self.f_ui = tkfont.Font(family=ui, size=11)
        self.f_ui_bold = tkfont.Font(family=ui, size=10, weight="bold")
        self.f_small = tkfont.Font(family=ui, size=9)
        self.f_title = tkfont.Font(family=ui, size=17, weight="bold")
        self.f_text = tkfont.Font(family=ui, size=13)
        self.f_mono = tkfont.Font(family=mono, size=12)

        self._build()
        self.apply_theme()
        self.set_mode(self.mode)
        root.protocol("WM_DELETE_WINDOW", self.close)

    @property
    def P(self):
        return PALETTES[self.theme]

    def reg(self, widget, **opts):
        """Register a widget whose options map to palette keys."""
        self.registry.append((widget, opts))
        return widget

    # ── layout ──────────────────────────────────────────────────────────────
    def _build(self):
        root = self.root
        self.reg(root, bg="bg")

        # header
        header = self.reg(tk.Frame(root), bg="bg")
        header.pack(fill="x", padx=22, pady=(18, 6))
        left = self.reg(tk.Frame(header), bg="bg")
        left.pack(side="left")
        self.reg(tk.Label(left, text="LaTeX Translator", font=self.f_title),
                 bg="bg", fg="fg").pack(anchor="w")
        self.reg(tk.Label(left, text="Paste on the left — the result appears on the right instantly",
                          font=self.f_small), bg="bg", fg="muted").pack(anchor="w")
        self.theme_btn = Btn(header, self, "", self.toggle_theme)
        self.theme_btn.pack(side="right")

        # toolbar
        bar = self.reg(tk.Frame(root), bg="bg")
        bar.pack(fill="x", padx=22, pady=(8, 10))
        self.btn_l2t = Btn(bar, self, "LaTeX  →  Text", lambda: self.set_mode("l2t"), padx=18)
        self.btn_t2l = Btn(bar, self, "Text  →  LaTeX", lambda: self.set_mode("t2l"), padx=18)
        self.btn_l2t.pack(side="left")
        self.btn_t2l.pack(side="left", padx=(6, 0))
        self.chk = self.reg(
            tk.Checkbutton(bar, text="Use $$ … $$ for equations", variable=self.display_var,
                           command=self.on_option, font=self.f_small, bd=0,
                           highlightthickness=0, cursor="hand2"),
            bg="bg", fg="fg", activebackground="bg", activeforeground="fg",
            selectcolor="text_bg")

        # cards
        body = self.reg(tk.Frame(root), bg="bg")
        body.pack(fill="both", expand=True, padx=22)
        body.columnconfigure(0, weight=1, uniform="c")
        body.columnconfigure(1, weight=1, uniform="c")
        body.rowconfigure(0, weight=1)

        self.in_title, self.inp = self._card(body, 0, "Paste", self.paste, editable=True)
        self.out_title, self.out = self._card(body, 1, "Copy", self.copy, editable=False)
        self.inp.bind("<<Modified>>", self._modified)
        self.inp.focus_set()

        # footer
        foot = self.reg(tk.Frame(root), bg="bg")
        foot.pack(fill="x", padx=22, pady=(10, 16))
        Btn(foot, self, "⇄  Swap", self.swap).pack(side="left")
        Btn(foot, self, "Clear", self.clear).pack(side="left", padx=(6, 0))
        self.reg(tk.Label(foot, textvariable=self.count, font=self.f_small),
                 bg="bg", fg="muted").pack(side="right")
        self.reg(tk.Label(foot, textvariable=self.status, font=self.f_ui_bold),
                 bg="bg", fg="accent").pack(side="right", padx=14)

    def _card(self, parent, col, action_text, action, editable):
        outer = self.reg(tk.Frame(parent, padx=1, pady=1), bg="border")
        outer.grid(row=0, column=col, sticky="nsew", padx=(0, 8) if col == 0 else (8, 0))
        inner = self.reg(tk.Frame(outer), bg="panel")
        inner.pack(fill="both", expand=True)

        head = self.reg(tk.Frame(inner), bg="panel")
        head.pack(fill="x", padx=12, pady=(10, 4))
        title = self.reg(tk.Label(head, font=self.f_ui_bold), bg="panel", fg="muted")
        title.pack(side="left")
        Btn(head, self, action_text, action, kind="accent", padx=12, pady=3).pack(side="right")

        wrap_f = self.reg(tk.Frame(inner), bg="panel")
        wrap_f.pack(fill="both", expand=True)
        text = self.reg(
            tk.Text(wrap_f, wrap="word", relief="flat", bd=0, highlightthickness=0,
                    padx=14, pady=10, undo=editable, font=self.f_text,
                    state="normal" if editable else "disabled"),
            bg="text_bg", fg="fg", insertbackground="fg", selectbackground="select",
            selectforeground="fg")
        sb = ttk.Scrollbar(wrap_f, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)
        return title, text

    # ── theme ───────────────────────────────────────────────────────────────
    def apply_theme(self):
        P = self.P
        for w, opts in self.registry:
            w.configure(**{k: P.get(v, v) for k, v in opts.items()})
        st = ttk.Style(self.root)
        st.theme_use("clam")
        st.configure("Vertical.TScrollbar", background=P["btn"], troughcolor=P["text_bg"],
                     bordercolor=P["text_bg"], arrowcolor=P["fg"], lightcolor=P["btn"],
                     darkcolor=P["btn"], relief="flat", gripcount=0)
        st.map("Vertical.TScrollbar", background=[("active", P["btn_hover"])])
        self.theme_btn.configure(text="☀  Light mode" if self.theme == "dark" else "☾  Dark mode")
        for b in self.buttons:
            b.restyle()

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()
        self.persist()

    # ── behaviour ───────────────────────────────────────────────────────────
    def set_mode(self, mode):
        self.mode = mode
        self.btn_l2t.set_kind("accent" if mode == "l2t" else "normal")
        self.btn_t2l.set_kind("accent" if mode == "t2l" else "normal")
        in_t, out_t = self.MODES[mode]
        self.in_title.configure(text=in_t.upper())
        self.out_title.configure(text=out_t.upper())
        self.inp.configure(font=self.f_mono if mode == "l2t" else self.f_text)
        self.out.configure(font=self.f_text if mode == "l2t" else self.f_mono)
        if mode == "t2l":
            self.chk.pack(side="right")
        else:
            self.chk.pack_forget()
        self.update()
        self.persist()

    def on_option(self):
        self.update()
        self.persist()

    def _modified(self, _event=None):
        if self.inp.edit_modified():
            self.inp.edit_modified(False)
            self.update()

    def update(self):
        src = self.inp.get("1.0", "end-1c")
        if self.mode == "l2t":
            res = translate_text(src)
        else:
            res = text_to_latex(src, self.display_var.get())
        self.out.configure(state="normal")
        self.out.delete("1.0", "end")
        self.out.insert("1.0", res)
        self.out.configure(state="disabled")
        self.count.set(f"{len(src)} characters")

    def flash(self, msg):
        self.status.set(msg)
        self.root.after(2000, lambda: self.status.set(""))

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.out.get("1.0", "end-1c"))
        self.flash("Copied to clipboard ✓")

    def paste(self):
        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            self.flash("Clipboard is empty")
            return
        self.inp.delete("1.0", "end")
        self.inp.insert("1.0", text)

    def clear(self):
        self.inp.delete("1.0", "end")
        self.update()
        self.status.set("")

    def swap(self):
        result = self.out.get("1.0", "end-1c")
        self.set_mode("t2l" if self.mode == "l2t" else "l2t")
        self.inp.delete("1.0", "end")
        self.inp.insert("1.0", result)

    def persist(self):
        save_cfg({"theme": self.theme, "mode": self.mode, "display": self.display_var.get()})

    def close(self):
        self.persist()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
def run_gui():
    if tk is None:
        sys.exit("tkinter is not available. On Linux install it with: sudo apt install python3-tk")
    App().run()


def run_cli(args):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    text = open(args.input, encoding="utf-8").read()
    result = text_to_latex(text) if args.reverse else translate_text(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        print(result)


def main():
    ap = argparse.ArgumentParser(description="Convert between LaTeX math and readable text.")
    ap.add_argument("input", nargs="?", help="input file (omit to open the GUI)")
    ap.add_argument("-o", "--output", help="output file (CLI mode)")
    ap.add_argument("-r", "--reverse", action="store_true", help="CLI: convert text -> LaTeX")
    args = ap.parse_args()
    run_cli(args) if args.input else run_gui()


if __name__ == "__main__":
    main()
