# formatter.py -- turns numbers into text for the GUI table and result labels.
# No calculations about the series happen here, only formatting.


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
    """result is the dictionary from the controller:
    {x, n, approx, reference, error, terms, sums}
    Returns a dictionary of display strings for the result labels."""
    return {
        "x": str(result["x"]),
        "n": str(result["n"]),
        "approx": format_number(result["approx"]),
        "reference": format_number(result["reference"]),
        "error": format_error(result["error"]),
    }