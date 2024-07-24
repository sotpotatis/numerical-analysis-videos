"""math_functions.py
Various math functions, such as The Witch of Agnesi"""


def witch_of_agnesi(x: float, radius: float) -> float:
    """Evaluates the witch of Agnesi function for a given radius at the point x.

    :param x: The point x to evaluate Witch of Agnesi at.

    :param radius: The radius of the circle to fit the Witch of Agnesi function to."""
    return 8 * (radius**3) / (x**2 + 4 * (radius**2))
