import math

_REFERENCE_FUNCTIONS = {
    "exp": math.exp,
    "ln": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
}


def reference_value(func, x):
    return _REFERENCE_FUNCTIONS[func](x)


def absolute_error(approx, reference):
    return abs(approx - reference)