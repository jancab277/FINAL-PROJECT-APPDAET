import math

_REFERENCE_FUNCTIONS = {
    "e^x": math.exp,
    "sin(x)": math.sin,
    "cos(x)": math.cos,
    "ln(x)": math.log,
    "tan(x)": math.tan,
}


def reference_value(func, x):
    return _REFERENCE_FUNCTIONS[func](x)


def absolute_error(approx, reference):
    return abs(approx - reference)