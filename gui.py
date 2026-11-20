"""gui.py - Tkinter interface for the Taylor Series Mathematical Explorer

Collects the function, x and number of terms, calls controller.run_calculation(),
and shows the results, the series breakdown, the term table and the graph.
"""

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import plotting
from plotting import draw_comparison, draw_partial_curves

# ---------------------------------------------------------------------------
# Imports from the group's files, with TEMP fallbacks so this file runs alone.
# Once config.py and controller.py are in the repo, the real ones are used.
# ---------------------------------------------------------------------------
try:
    from config import FUNCTIONS
except ImportError:
    FUNCTIONS = {  # TEMP: replace with config.py
        "exp": {"label": "e^x",    "x_min": -2.0, "x_max": 2.0, "max_terms": 12},
        "ln":  {"label": "ln(x)",  "x_min": 0.5,  "x_max": 1.5, "max_terms": 20},
        "sin": {"label": "sin(x)", "x_min": -2.0, "x_max": 2.0, "max_terms": 12},
        "cos": {"label": "cos(x)", "x_min": -2.0, "x_max": 2.0, "max_terms": 12},
        "tan": {"label": "tan(x)", "x_min": -1.0, "x_max": 1.0, "max_terms": 5},
    }


def _fallback_run_calculation(func, x_text, n_text):
    """TEMP: replace with controller.run_calculation() once it exists."""
    cfg = FUNCTIONS[func]
    try:
        x = float(x_text)
    except ValueError:
        raise ValueError("x must be a number.")
    if not cfg["x_min"] <= x <= cfg["x_max"]:
        raise ValueError(f"x must be between {cfg['x_min']} and {cfg['x_max']}.")
    try:
        n = int(n_text)
    except ValueError:
        raise ValueError("Number of terms must be a whole number.")
    if not 1 <= n <= cfg["max_terms"]:
        raise ValueError(f"Number of terms must be between 1 and {cfg['max_terms']}.")

    sums = [plotting._approximate(func, x, k) for k in range(1, n + 1)]
    terms = [sums[0]] + [sums[i] - sums[i - 1] for i in range(1, n)]
    reference = plotting._real_value(func, x)
    return {
        "x": x, "n": n, "approx": sums[-1], "reference": reference,
        "error": abs(sums[-1] - reference), "terms": terms, "sums": sums,
        "formulas": [""] * n, "general": "", "n_terms_text": "",
        "substituted": "", "evaluated": "",
    }


try:
    from controller import run_calculation
except ImportError:
    run_calculation = _fallback_run_calculation


# ---------------------------------------------------------------------------
# The app window
# ---------------------------------------------------------------------------
class TaylorApp:
    def __init__(self, root):
        self.root = root
        root.title("Taylor Series Mathematical Explorer")
        root.geometry("1150x720")

        self.label_to_key = {cfg["label"]: key for key, cfg in FUNCTIONS.items()}
        self.func_var = tk.StringVar(value=next(iter(self.label_to_key)))
        self.x_var = tk.StringVar(value="1")
        self.n_var = tk.StringVar(value="3")
        self.partial_var = tk.BooleanVar(value=True)
        self.hint_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.series_var = tk.StringVar(value="Press Calculate to see the series.")
        self.result_vars = {
            name: tk.StringVar(value="-")
            for name in ("x", "n", "estimate", "real", "error")
        }

        self._build_widgets()
        self.update_limits()

    # ---------------- layout ----------------
    def _build_widgets(self):
        # Top: inputs
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Function:").grid(row=0, column=0, padx=(0, 4))
        combo = ttk.Combobox(top, textvariable=self.func_var, state="readonly",
                             values=list(self.label_to_key), width=10)
        combo.grid(row=0, column=1, padx=(0, 12))
        combo.bind("<<ComboboxSelected>>", lambda e: self.update_limits())

        ttk.Label(top, text="x:").grid(row=0, column=2, padx=(0, 4))
        ttk.Entry(top, textvariable=self.x_var, width=8).grid(row=0, column=3, padx=(0, 12))

        ttk.Label(top, text="Terms:").grid(row=0, column=4, padx=(0, 4))
        ttk.Entry(top, textvariable=self.n_var, width=6).grid(row=0, column=5, padx=(0, 12))

        ttk.Button(top, text="Calculate", command=self.on_calculate).grid(row=0, column=6, padx=(0, 12))
        ttk.Checkbutton(top, text="Show partial sums on graph", variable=self.partial_var,
                        command=self.on_calculate).grid(row=0, column=7)

        ttk.Label(top, textvariable=self.hint_var, foreground="gray").grid(
            row=1, column=0, columnspan=8, sticky="w", pady=(6, 0))

        # Bottom: error message area (packed before body so it stays at the bottom)
        ttk.Label(self.root, textvariable=self.error_var, foreground="red",
                  padding=(10, 4)).pack(side="bottom", fill="x")

        # Middle: left (text) and right (graph)
        body = ttk.Frame(self.root, padding=(10, 0))
        body.pack(fill="both", expand=True)
        left = ttk.Frame(body)
        left.pack(side="left", fill="both", expand=True)
        right = ttk.Frame(body)
        right.pack(side="right", fill="both", expand=True)

        # Results
        results = ttk.LabelFrame(left, text="Results", padding=8)
        results.pack(fill="x", pady=(0, 8))
        rows = [("x", "x"), ("Terms", "n"), ("Estimate", "estimate"),
                ("Real value", "real"), ("Error", "error")]
        for i, (text, key) in enumerate(rows):
            ttk.Label(results, text=text + ":").grid(row=i, column=0, sticky="w")
            ttk.Label(results, textvariable=self.result_vars[key]).grid(
                row=i, column=1, sticky="w", padx=10)

        # Series breakdown
        series = ttk.LabelFrame(left, text="Series", padding=8)
        series.pack(fill="x", pady=(0, 8))
        ttk.Label(series, textvariable=self.series_var, font=("Consolas", 10),
                  wraplength=520, justify="left").pack(anchor="w")

        # Term table
        table = ttk.LabelFrame(left, text="Term table", padding=8)
        table.pack(fill="both", expand=True)
        cols = ("k", "formula", "term", "total")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=8)
        for col, head, width in (("k", "k", 40), ("formula", "Term formula", 150),
                                 ("term", "Term value", 120), ("total", "Running total", 120)):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=width, anchor="center")
        scroll = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Graph
        self.fig = Figure(figsize=(6, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Press Calculate to draw the graph")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------- actions ----------------
    def _current_func(self):
        return self.label_to_key[self.func_var.get()]

    def update_limits(self):
        """Update the range / term-limit hint when the function changes."""
        cfg = FUNCTIONS[self._current_func()]
        self.hint_var.set(
            f"x must be from {cfg['x_min']} to {cfg['x_max']}; "
            f"terms from 1 to {cfg['max_terms']}."
        )

    def on_calculate(self):
        """Read inputs, call the controller, update the display."""
        func = self._current_func()
        try:
            result = run_calculation(func, self.x_var.get(), self.n_var.get())
        except ValueError as err:
            self.show_error(str(err))   # app keeps running
            return
        self.show_error("")
        self.show_results(result)
        self.show_table(result)
        self.show_series(result)
        self.show_plot(func, result)

    def show_results(self, result):
        self.result_vars["x"].set(f"{result['x']}")
        self.result_vars["n"].set(f"{result['n']}")
        self.result_vars["estimate"].set(f"{result['approx']:.10f}")
        self.result_vars["real"].set(f"{result['reference']:.10f}")
        self.result_vars["error"].set(f"{result['error']:.10f}")

    def show_table(self, result):
        self.tree.delete(*self.tree.get_children())
        terms, sums = result["terms"], result["sums"]
        formulas = result.get("formulas") or [""] * len(terms)
        for k, (f, t, s) in enumerate(zip(formulas, terms, sums), start=1):
            self.tree.insert("", "end", values=(k, f, f"{t:.6f}", f"{s:.6f}"))

    def show_series(self, result):
        """Fill the Series panel (general, n-term, substituted, evaluated)."""
        lines = [result.get("general", ""), result.get("n_terms_text", ""),
                 result.get("substituted", ""), result.get("evaluated", "")]
        text = "\n".join(line for line in lines if line)
        self.series_var.set(text or "(series text not available yet)")

    def show_plot(self, func, result):
        cfg = FUNCTIONS[func]
        draw_comparison(self.ax, func, result["n"], result["x"], result["approx"])
        if self.partial_var.get():
            draw_partial_curves(self.ax, func, result["n"], cfg["x_min"], cfg["x_max"])
        self.canvas.draw()

    def show_error(self, msg):
        """Display the validation message (empty string clears it)."""
        self.error_var.set(msg)


# Quick standalone test: run `python gui.py`
if __name__ == "__main__":
    window = tk.Tk()
    TaylorApp(window)
    window.mainloop()