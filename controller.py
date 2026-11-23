from validation import validate_inputs
from series import generate_terms, partial_sums
from reference import reference_value, absolute_error
from formatter import (term_formulas, series_general, series_n_terms,
                       series_substituted, series_evaluated)


def build_term_rows(terms, sums, formulas):
    return [(i, f, t, s) for i, (f, t, s) in enumerate(zip(formulas, terms, sums), start=1)]


def run_calculation(func, x_text, n_text):
    x, n = validate_inputs(func, x_text, n_text)   # 1. check inputs
    terms = generate_terms(func, x, n)             # 2. first n nonzero terms
    sums = partial_sums(terms)                     # 3. running partial sums
    approx = sums[-1]                              # 4. final approximation
    reference = reference_value(func, x)           # 5. math-library value
    return {
        "x": x,
        "n": n,
        "approx": approx,
        "reference": reference,
        "error": absolute_error(approx, reference),
        "terms": terms,
        "sums": sums,
        "formulas": term_formulas(func, n),
        "general": series_general(func),
        "n_terms_text": series_n_terms(func, n),
        "substituted": series_substituted(func, x, n),
        "evaluated": series_evaluated(terms, approx),
    }