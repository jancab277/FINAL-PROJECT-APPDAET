# validation.py -- Input safety module (Cabrera, Janis)
# This file acts as the "bouncer". It checks what the user typed in the GUI
# and stops the math engine from running if the numbers are unsafe or invalid.

from config import FUNCTIONS


def parse_x(text):
    """
    Try to turn the user's text for 'x' into a decimal number (float).
    Raises a ValueError if they typed letters or symbols instead of a number.
    """
    try:
        x_value = float(text)
        return x_value
    except ValueError:
        raise ValueError("Error: 'x' must be a valid number (e.g., 1.5 or -0.5).")


def parse_n(text):
    """
    Try to turn the user's text for 'Terms' into a whole number (int).
    Raises a ValueError if they typed letters, symbols, or decimals.
    """
    try:
        n_value = int(text)
        return n_value
    except ValueError:
        raise ValueError("Error: The number of terms must be a whole number (e.g., 3 or 5).")


def validate_inputs(func, x_text, n_text):
    """
    Takes the raw text from the user, converts it, and checks it against 
    the safe boundaries defined in config.py.
    Returns the clean numbers (x, n) if safe, or raises an Error if not.
    """
    # 1. Make sure the math function actually exists in our config file
    if func not in FUNCTIONS:
        raise ValueError("Error: Unsupported function selected.")

    # 2. Get the specific rules for the chosen function
    rules = FUNCTIONS[func]

    # 3. Convert the text inputs into actual Python numbers
    x = parse_x(x_text)
    n = parse_n(n_text)

    # 4. Check if the 'x' value is inside the safe minimum and maximum boundaries
    if x < rules["x_min"] or x > rules["x_max"]:
        error_msg = "Error: For " + rules["label"] + ", 'x' must be between " + str(rules["x_min"]) + " and " + str(rules["x_max"]) + "."
        raise ValueError(error_msg)

    # 5. Check if the number of terms is safe (at least 1, and not too high)
    if n < 1 or n > rules["max_terms"]:
        error_msg = "Error: For " + rules["label"] + ", terms must be between 1 and " + str(rules["max_terms"]) + "."
        raise ValueError(error_msg)

    # 6. If everything is correct, return the final numbers for calculation.
    return x, n
