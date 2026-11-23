# formatter.py -- turns numbers into text for the GUI table and result labels.
# No calculations about the series happen here, only formatting.

from config import FUNCTIONS


def format_number(value, digits=8):
    """Show a number with a fixed number of decimal places."""
    return f"{value:.{digits}f}"


def format_error(value):
    """Errors can be very small, so use scientific notation (e.g. 4.0e-03)."""
    return f"{value:.3e}"


def format_term_rows(terms, sums):
    """Rows for the term table: (term number, term value, running sum)."""
    rows = []
    for i in range(len(terms)):
        rows.append((i + 1, format_number(terms[i]), format_number(sums[i])))
    return rows


def format_result(result):
    """result is the dictionary from the controller.
    Returns a dictionary of display strings for the result labels."""
    return {
        "x": str(result["x"]),
        "n": str(result["n"]),
        "approx": format_number(result["approx"]),
        "reference": format_number(result["reference"]),
        "error": format_error(result["error"]),
    }


# ---------------------------------------------------------------------------
# Series text (shown in the Series panel and the "Term formula" column)
# ---------------------------------------------------------------------------
_TAN_FORMULAS = ["x", "x^3/3", "2x^5/15", "17x^7/315", "62x^9/2835"]


def term_formula(func, k):
    """Text of the k-th term (k = 1, 2, ...), including its sign."""
    sign = "-" if k % 2 == 0 else ""
    if func == "exp":
        if k == 1:
            return "1"
        if k == 2:
            return "x"
        return f"x^{k - 1}/{k - 1}!"
    if func == "sin":
        p = 2 * k - 1
        return "x" if k == 1 else f"{sign}x^{p}/{p}!"
    if func == "cos":
        p = 2 * k - 2
        return "1" if k == 1 else f"{sign}x^{p}/{p}!"
    if func == "ln":
        return "(x-1)" if k == 1 else f"{sign}(x-1)^{k}/{k}"
    if func == "tan":
        return _TAN_FORMULAS[k - 1]
    raise ValueError("Unsupported function: " + str(func))


def term_formulas(func, n):
    """List of formulas for terms 1..n (for the table column)."""
    return [term_formula(func, k) for k in range(1, n + 1)]


def _join(parts):
    """Join pieces so a leading '-' becomes ' - ' and others become ' + '."""
    text = parts[0]
    for p in parts[1:]:
        if p.startswith("-"):
            text += " - " + p[1:]
        else:
            text += " + " + p
    return text


def series_general(func):
    """General series from config.py, e.g. 'e^x = 1 + x + x^2/2! + ...'"""
    return FUNCTIONS[func]["general_series"]


def series_n_terms(func, n):
    """The n-term polynomial, e.g. 'e^x ≈ 1 + x + x^2/2!'"""
    return FUNCTIONS[func]["label"] + " ≈ " + _join(term_formulas(func, n))


def series_substituted(func, x, n):
    """The n-term polynomial with x replaced by its value."""
    xs = f"{x:g}"
    if x < 0:
        xs = "(" + xs + ")"
    parts = [f.replace("x", xs) for f in term_formulas(func, n)]
    return "≈ " + _join(parts)


def series_evaluated(terms, approx):
    """The same sum with each term as a number, ending in the estimate."""
    parts = [f"{t:.6g}" for t in terms]
    return "= " + _join(parts) + f" = {approx:.8f}"