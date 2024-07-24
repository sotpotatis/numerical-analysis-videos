"""latex_utilities.py
Various utilities related to LaTeX code generation."""

from enum import Enum
from typing import Optional, Union, List
from manim import RED, YELLOW, GREEN, BLUE, TexTemplate


def manim_color_to_latex_color(color) -> str:
    """Convert Manim color constants to LaTeX (xcolor) color names.

    :param color: The Manim color constant to convert."""
    if color == RED:
        return "red"
    elif color == YELLOW:
        return "yellow"
    elif color == GREEN:
        return "green"
    elif color == BLUE:
        return "blue"


def create_cases(
    equations: Union[str, List[str]],
    include_math_environment_start: Optional[bool] = None,
    return_list: Optional[bool] = None,
):
    """Creates a \begin{cases} part with a given list of equations.

    :param equations: The equations to include inside the cases.

    :param include_math_environment_start: Optionally include the math environment start and end. Default is True.
    This is needed for TeX but not MathTex.

    :param return_list: Optionally return the equations as a list. Default is False. Note that this option is incompatible with
    include_math_environment_start=True."""
    if include_math_environment_start is None:
        include_math_environment_start = True
    if return_list is None:
        return_list = False
    if not isinstance(equations, list):
        equations = [equations]  # Allow passing one single equation
    all_latex_equations = []
    latex_code = r"\begin{cases}"
    all_latex_equations.append(latex_code)
    for equation in equations:
        latex_code_to_append = equation + r"\\"
        latex_code += latex_code_to_append
        all_latex_equations.append(latex_code_to_append)
    environment_close = r"\end{cases}"
    latex_code += environment_close  # Close environment
    all_latex_equations.append(environment_close)
    if include_math_environment_start:
        latex_code = f"$${latex_code}$$"
    if return_list:
        return all_latex_equations
    return latex_code


class MatrixStyle(Enum):
    """A set of matrix styles that can be used with create_matrix.
    See https://latex-programming.fandom.com/wiki/Matrix_(LaTeX_environment) for a visualization
    of the different choices"""

    NO_BORDERS = "matrix"
    BRACKETS_BORDERS = "bmatrix"
    BRACES_BORDERS = "Bmatrix"
    PARENTHESES_BORDERS = "pmatrix"
    VERTICAL_BARS_BORDERS = "vmatrix"
    DOUBLE_VERTICAL_BARS_BORDERS = "Vmatrix"
    NO_BORDERS_SMALL = "smallmatrix"


def create_matrix(
    coordinates: List[List[Union[int, float, str]]],
    matrix_style: Optional[MatrixStyle] = None,
) -> str:
    """Create a string for a LaTeX matrix.

    :param coordinates: The coordinates in the matrix as a two-dimensional list in the format
    [<row 1 entries>, <row 2 entries>, ..., <row n entries>]. for an nxm matrix,
    <row i entries> would have the format [<row i, column 1>,<row i, column 2>, ..., <row i, column m>]
    The column entries will be converted to a string if they are not already via their str() function.


    :param matrix_style: The style of the matrix, see MATRIX_TYPE. Defaults to a pmatrix.
    """
    if matrix_style is None:
        matrix_style = MatrixStyle.PARENTHESES_BORDERS
    latex_string = r"\begin{%s}" % (matrix_style.value)
    for row in coordinates:
        for column in row:
            latex_string += str(column) + "&"
        latex_string = latex_string.strip("&") + r"\\"
    latex_string += r"\end{%s}" % (matrix_style.value)
    print(latex_string)
    return latex_string


def generate_tex_template_for_packages(package_list: List[str]) -> TexTemplate:
    """In Manim, to use external TeX packages inside a Tex Mobject, you need to include a
    TexTemplate. This function helps you generate a TeX template based on a list of packages.

    :param package_list: The package list you want to include in your LaTeX environment.
    """
    template = TexTemplate()
    for package in package_list:
        template.add_to_preamble(r"\usepackage{%s}" % (package) + "\n")
    return template


# Some precooked templates for use in code
TEX_TEMPLATE_COLORS = generate_tex_template_for_packages(
    ["xcolor"]
)  # TeX template for using colors
