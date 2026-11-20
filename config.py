# config.py -- Settings and limits for the math functions
# This file holds the boundaries, labels, and text formulas to prevent the app 
# from crashing and to help the graphical interface display the right information.

FUNCTIONS = {
    "exp": {
        "label": "e^x",
        "x_min": -2.0,
        "x_max": 2.0,
        "max_terms": 12,
        "center": 0,
        "expansion": "Maclaurin Series (centered at 0)",
        "general_series": "e^x = 1 + x + x^2/2! + x^3/3! + ..."
    },
    "ln": {
        "label": "ln(x)",
        "x_min": 0.5,
        "x_max": 1.5,
        "max_terms": 20,
        "center": 1,
        "expansion": "Taylor Series (centered at 1)",
        "general_series": "ln(x) = (x-1) - (x-1)^2/2 + (x-1)^3/3 - ..."
    },
    "sin": {
        "label": "sin(x)",
        "x_min": -2.0,
        "x_max": 2.0,
        "max_terms": 12,
        "center": 0,
        "expansion": "Maclaurin Series (centered at 0)",
        "general_series": "sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ..."
    },
    "cos": {
        "label": "cos(x)",
        "x_min": -2.0,
        "x_max": 2.0,
        "max_terms": 12,
        "center": 0,
        "expansion": "Maclaurin Series (centered at 0)",
        "general_series": "cos(x) = 1 - x^2/2! + x^4/4! - x^6/6! + ..."
    },
    "tan": {
        "label": "tan(x)",
        "x_min": -1.0,
        "x_max": 1.0,
        "max_terms": 5,
        "center": 0,
        "expansion": "Maclaurin Series (centered at 0)",
        "general_series": "tan(x) = x + x^3/3 + 2x^5/15 + 17x^7/315 + ..."
    }
}
