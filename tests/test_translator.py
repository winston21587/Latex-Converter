import unittest
import sys
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from latex_to_text import convert, translate_text, text_to_latex, to_latex_expr


class TestLatexToText(unittest.TestCase):
    def test_basic_conversion(self):
        self.assertEqual(convert(r"\alpha + \beta = \gamma"), "α + β = γ")
        self.assertEqual(convert(r"x \approx 3.14"), "x ≈ 3.14")
        self.assertEqual(convert(r"a \neq b"), "a ≠ b")

    def test_superscripts_and_subscripts(self):
        self.assertEqual(convert(r"x^2 + y_1"), "x² + y₁")
        self.assertEqual(convert(r"x^{12} + a_{ij}"), "x¹² + a_ij")
        self.assertEqual(convert(r"a_{i+j}"), "a_(i+j)")

    def test_fractions(self):
        self.assertEqual(convert(r"\frac{1}{2}"), "1/2")
        self.assertEqual(convert(r"\frac{x + 1}{y - 1}"), "(x + 1)/(y - 1)")

    def test_square_roots(self):
        self.assertEqual(convert(r"\sqrt{x}"), "√x")
        self.assertEqual(convert(r"\sqrt{1^2 + 0^2}"), "√(1² + 0²)")

    def test_text_commands(self):
        self.assertEqual(convert(r"\text{Length} = 1.414"), "Length = 1.414")
        self.assertEqual(convert(r"\mathrm{dx} / \mathbf{len}"), "dx / len")

    def test_translate_text_environments(self):
        doc = (
            "For diagonal movement: $$\\text{Length} = 1.414$$ "
            "and inline $\\frac{1}{2}$ with \\[\\sqrt{4} = 2\\] and \\(\\pi \\approx 3.14\\)."
        )
        expected = (
            "For diagonal movement: Length = 1.414 "
            "and inline 1/2 with √4 = 2 and π ≈ 3.14."
        )
        self.assertEqual(translate_text(doc), expected)

    def test_plain_text_unaltered(self):
        plain = "Hello world! This has no math at all."
        self.assertEqual(translate_text(plain), plain)

    def test_empty_string(self):
        self.assertEqual(translate_text(""), "")
        self.assertEqual(convert(""), "")


class TestTextToLatex(unittest.TestCase):
    def test_symbol_conversion(self):
        self.assertEqual(to_latex_expr("α + β ≈ γ"), r"\alpha + \beta \approx \gamma")

    def test_powers_and_indices(self):
        self.assertEqual(to_latex_expr("x² + y₁"), "x^2 + y_1")

    def test_square_root(self):
        self.assertEqual(to_latex_expr("√(x + y)"), r"\sqrt{x + y}")
        self.assertEqual(to_latex_expr("√x"), r"\sqrt{x}")

    def test_fractions(self):
        self.assertEqual(to_latex_expr("1/2"), r"\frac{1}{2}")
        self.assertEqual(to_latex_expr("(x + 1)/(y - 1)"), r"\frac{x + 1}{y - 1}")

    def test_text_to_latex_with_plain_text(self):
        sample = "Length = 1.414 and dx/len ≈ 0.7071"
        res = text_to_latex(sample)
        self.assertIn(r"\approx", res)
        self.assertIn(r"\frac", res)

    def test_backticks_preserved(self):
        sample = "Look at `inline code with = and /` and then Length = 1.414"
        res = text_to_latex(sample)
        self.assertIn("`inline code with = and /`", res)


class TestRoundtrip(unittest.TestCase):
    def test_roundtrip_diagonal_sample(self):
        latex_input = "$$\\text{Length} = 1.414$$ $$\\frac{dx}{\\text{len}} = \\frac{1}{1.414} \\approx 0.7071$$"
        readable = translate_text(latex_input)
        self.assertEqual(readable, "Length = 1.414 dx/len = 1/1.414 ≈ 0.7071")
        back_to_latex = text_to_latex(readable)
        self.assertIn(r"\frac{1}{1.414}", back_to_latex)
        self.assertIn(r"\approx 0.7071", back_to_latex)


if __name__ == "__main__":
    unittest.main()
