"""plotting.py - Visualization module (Rivera, Kobie)

Draws the real function (from Python's math library) and the n-term Taylor
estimate on the same labeled axes, with a marker at the chosen x.

Function names used here: "exp", "ln", "sin", "cos", "tan".
If config.py uses different keys, change them in FUNC_INFO below (or in config.py).
"""

import math

# ---------------------------------------------------------------------------
# Settings per function (mirrors config.py). If config.py exists, use it.
# ---------------------------------------------------------------------------
FUNC_INFO = {
    "exp": {"label": "e^x",    "x_min": -2.0, "x_max": 2.0},
    "ln":  {"label": "ln(x)",  "x_min": 0.5,  "x_max": 1.5},
    "sin": {"label": "sin(x)", "x_min": -2.0, "x_max": 2.0},
    "cos": {"label": "cos(x)", "x_min": -2.0, "x_max": 2.0},
    "tan": {"label": "tan(x)", "x_min": -1.0, "x_max": 1.0},
}

try:
    from config import FUNCTIONS  # TODO: confirm key names with Cabrera
    for _name, _cfg in FUNCTIONS.items():
        if _name in FUNC_INFO:
            FUNC_INFO[_name].update(
                {k: _cfg[k] for k in ("label", "x_min", "x_max") if k in _cfg}
            )
except ImportError:
    pass  # config.py not available yet; use the defaults above


# ---------------------------------------------------------------------------
# Real (reference) values - math library is allowed here, for the REAL curve only
# ---------------------------------------------------------------------------
def _real_value(func, x):
    if func == "exp":
        return math.exp(x)
    if func == "ln":
        return math.log(x)
    if func == "sin":
        return math.sin(x)
    if func == "cos":
        return math.cos(x)
    if func == "tan":
        return math.tan(x)
    raise ValueError(f"Unsupported function: {func}")


# ---------------------------------------------------------------------------
# TEMP placeholder estimate (NOT using math library).
# Used only until series.py from Aivan and Isabelle is available.
# Once series.py exists, the try/except below automatically uses the real one.
# ---------------------------------------------------------------------------
def _temp_approximate(func, x, n):
    """TEMP: replace with series.approximate() once the group's file exists."""
    total = 0.0
    if func == "exp":                      # sum x^k / k!
        term = 1.0
        for k in range(n):
            total += term
            term = term * x / (k + 1)
    elif func == "sin":                    # x - x^3/3! + x^5/5! ...
        term = x
        for k in range(n):
            total += term
            term = -term * x * x / ((2 * k + 2) * (2 * k + 3))
    elif func == "cos":                    # 1 - x^2/2! + x^4/4! ...
        term = 1.0
        for k in range(n):
            total += term
            term = -term * x * x / ((2 * k + 1) * (2 * k + 2))
    elif func == "ln":                     # centered at 1: sum (-1)^(k+1) (x-1)^k / k
        for k in range(1, n + 1):
            total += ((-1) ** (k + 1)) * ((x - 1) ** k) / k
    elif func == "tan":                    # fixed coefficients
        coeffs = [(1, 1), (3, 1 / 3), (5, 2 / 15), (7, 17 / 315), (9, 62 / 2835)]
        for power, c in coeffs[:n]:
            total += c * (x ** power)
    else:
        raise ValueError(f"Unsupported function: {func}")
    return total


try:
    from series import approximate as _approximate  # the group's real code
except ImportError:
    _approximate = _temp_approximate


# ---------------------------------------------------------------------------
# Required functions (from the planned design)
# ---------------------------------------------------------------------------
def curve_points(func, n, x_min, x_max, steps):
    """Return (xs, approx_ys, ref_ys) evenly spaced from x_min to x_max."""
    if steps < 2:
        raise ValueError("steps must be at least 2")
    step_size = (x_max - x_min) / (steps - 1)
    xs, approx_ys, ref_ys = [], [], []
    for i in range(steps):
        x = x_min + i * step_size
        xs.append(x)
        approx_ys.append(_approximate(func, x, n))
        ref_ys.append(_real_value(func, x))
    return xs, approx_ys, ref_ys


def draw_comparison(ax, func, n, x_value, approx):
    """Draw the real curve and the n-term estimate on the given Matplotlib axes."""
    info = FUNC_INFO[func]
    xs, approx_ys, ref_ys = curve_points(func, n, info["x_min"], info["x_max"], 200)

    ax.clear()
    ax.plot(xs, ref_ys, label=f"Real {info['label']}", linewidth=2)
    ax.plot(xs, approx_ys, "--", label=f"Taylor estimate ({n} term{'s' if n != 1 else ''})", linewidth=2)

    # Marker at the chosen x
    ax.plot([x_value], [_real_value(func, x_value)], "o", color="green", label="Real value at x")
    ax.plot([x_value], [approx], "x", color="red", markersize=10, markeredgewidth=2,
            label="Estimate at x")
    ax.axvline(x_value, color="gray", linestyle=":", linewidth=1)

    ax.set_title(f"{info['label']}: real value vs. {n}-term estimate")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()


def draw_partial_curves(ax, func, n, x_min, x_max):
    """OPTIONAL: draw faint curves for the partial sums S1..Sn.
    Call this AFTER draw_comparison(), because draw_comparison() clears the axes."""
    for k in range(1, n + 1):
        xs, approx_ys, _ = curve_points(func, k, x_min, x_max, 200)
        ax.plot(xs, approx_ys, color="gray", alpha=0.35, linewidth=1,
                label="Partial sums S1..Sn" if k == 1 else None)
    ax.legend()


# ---------------------------------------------------------------------------
# Quick standalone test: run `python plotting.py`
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    TEST_FUNC = "sin"  # change to "exp", "cos", "ln" or "tan" to test the others
    for ax, n in zip(axes, (2, 5)):
        x_test = 1.0
        draw_comparison(ax, TEST_FUNC, n, x_test, _approximate(TEST_FUNC, x_test, n))
        draw_partial_curves(ax, TEST_FUNC, n,
                            FUNC_INFO[TEST_FUNC]["x_min"], FUNC_INFO[TEST_FUNC]["x_max"])
    plt.tight_layout()
    plt.show()