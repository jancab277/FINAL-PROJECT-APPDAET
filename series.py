# series.py -- core algorithm (student-written)
# No math.exp / log / sin / cos / tan is used here.
# Each term is built from the previous term, so no big factorials are needed.


def exp_terms(x, n):
    """e^x = 1 + x + x^2/2! + x^3/3! + ...   (centered at 0)"""
    terms = []
    term = 1                                   # first term is 1
    terms.append(term)
    for k in range(2, n + 1):
        term = term * x / (k - 1)
        terms.append(term)
    return terms


def sin_terms(x, n):
    """sin(x) = x - x^3/3! + x^5/5! - ...   (centered at 0)"""
    terms = []
    term = x                                   # first term is x
    terms.append(term)
    for k in range(2, n + 1):
        term = term * (-x * x) / ((2 * k - 2) * (2 * k - 1))
        terms.append(term)
    return terms


def cos_terms(x, n):
    """cos(x) = 1 - x^2/2! + x^4/4! - ...   (centered at 0)"""
    terms = []
    term = 1                                   # first term is 1
    terms.append(term)
    for k in range(2, n + 1):
        term = term * (-x * x) / ((2 * k - 3) * (2 * k - 2))
        terms.append(term)
    return terms


def ln_terms(x, n):
    """ln(x) = (x-1) - (x-1)^2/2 + (x-1)^3/3 - ...   (centered at 1)"""
    u = x - 1
    terms = []
    term = u                                   # first term is (x - 1)
    terms.append(term)
    for k in range(2, n + 1):
        term = term * (-u) * (k - 1) / k
        terms.append(term)
    return terms


def tan_terms(x, n):
    """tan(x) = x + x^3/3 + 2x^5/15 + 17x^7/315 + 62x^9/2835  (n is 1 to 5)"""
    coefficients = [1, 1 / 3, 2 / 15, 17 / 315, 62 / 2835]
    terms = []
    for i in range(n):
        power = 2 * i + 1                      # 1, 3, 5, 7, 9
        terms.append(coefficients[i] * x ** power)
    return terms


def generate_terms(func, x, n):
    """Pick the right series function and return the list of n terms."""
    if func == "exp":
        return exp_terms(x, n)
    elif func == "sin":
        return sin_terms(x, n)
    elif func == "cos":
        return cos_terms(x, n)
    elif func == "ln":
        return ln_terms(x, n)
    elif func == "tan":
        return tan_terms(x, n)
    else:
        raise ValueError("Unsupported function: " + str(func))


def partial_sums(terms):
    """Running total after each term: S1 = t1, S2 = t1 + t2, ..."""
    sums = []
    total = 0
    for term in terms:
        total = total + term
        sums.append(total)
    return sums


def approximate(func, x, n):
    """Add up the first n terms and return the approximation."""
    total = 0
    for term in generate_terms(func, x, n):
        total = total + term

# series.py -- core algorithm (student-written)
# No math.exp / log / sin / cos / tan is used here.
# Each term is built from the previous term, so no big factorials are needed.


def exp_terms(x, n):
    """e^x = 1 + x + x^2/2! + x^3/3! + ...   (centered at 0)"""
    terms = []
    term = 1                                   # first term is 1
    terms.append(term)
    for k in range(2, n + 1):
        term = term * x / (k - 1)
        terms.append(term)
    return terms


def sin_terms(x, n):
    """sin(x) = x - x^3/3! + x^5/5! - ...   (centered at 0)"""
    terms = []
    term = x                                   # first term is x
    terms.append(term)
    for k in range(2, n + 1):
        term = term * (-x * x) / ((2 * k - 2) * (2 * k - 1))
        terms.append(term)
    return terms


def cos_terms(x, n):
    """cos(x) = 1 - x^2/2! + x^4/4! - ...   (centered at 0)"""
    terms = []
    term = 1                                   # first term is 1
    terms.append(term)
    for k in range(2, n + 1):
        term = term * (-x * x) / ((2 * k - 3) * (2 * k - 2))
        terms.append(term)
    return terms


def ln_terms(x, n):
    """ln(x) = (x-1) - (x-1)^2/2 + (x-1)^3/3 - ...   (centered at 1)"""
    u = x - 1
    terms = []
    term = u                                   # first term is (x - 1)
    terms.append(term)
    for k in range(2, n + 1):
        term = term * (-u) * (k - 1) / k
        terms.append(term)
    return terms


def tan_terms(x, n):
    """tan(x) = x + x^3/3 + 2x^5/15 + 17x^7/315 + 62x^9/2835  (n is 1 to 5)"""
    coefficients = [1, 1 / 3, 2 / 15, 17 / 315, 62 / 2835]
    terms = []
    for i in range(n):
        power = 2 * i + 1                      # 1, 3, 5, 7, 9
        terms.append(coefficients[i] * x ** power)
    return terms


def generate_terms(func, x, n):
    """Pick the right series function and return the list of n terms."""
    if func == "exp":
        return exp_terms(x, n)
    elif func == "sin":
        return sin_terms(x, n)
    elif func == "cos":
        return cos_terms(x, n)
    elif func == "ln":
        return ln_terms(x, n)
    elif func == "tan":
        return tan_terms(x, n)
    else:
        raise ValueError("Unsupported function: " + str(func))


def partial_sums(terms):
    """Running total after each term: S1 = t1, S2 = t1 + t2, ..."""
    sums = []
    total = 0
    for term in terms:
        total = total + term
        sums.append(total)
    return sums


def approximate(func, x, n):
    """Add up the first n terms and return the approximation."""
    total = 0
    for term in generate_terms(func, x, n):
        total = total + term

    return total