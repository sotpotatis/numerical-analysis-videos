"""equation_displaying.py
Utilities related to displaying equations on the screen."""

from manim import Mobject, MathTex, SurroundingRectangle, BLUE, always_redraw
from typing import List, Optional, Union


def create_equation_with_border(
    equation: Union[str, List],
    border_color: Optional[str] = None,
    border_radius: Optional[float] = None,
    scale: Optional[float] = None,
) -> List[Mobject]:
    """Creates an equation with a border around it.

    :param equation: The equation to display. If passed in list format, the list will be provided as args to the MathTex object.

    :param border_color: The color of the border. Optional, default is white.

    :param border_radius: The radius of the border. Optional, default is 0.2.

    :param scale: Optionally scale the equation. Default is 2.0.
    """
    if border_color is None:
        border_color = BLUE
    if border_radius is None:
        border_radius = 0.2
    if scale is None:
        scale = 2
    # See docstring. Allow passing both a list and a "raw" equation.
    if isinstance(equation, list):
        mathtex_args = equation
    else:
        mathtex_args = [equation]
    generic_polynomial_equation = MathTex(*mathtex_args)
    generic_polynomial_equation.scale(scale)
    equation_rectangle = always_redraw(
        lambda: SurroundingRectangle(
            generic_polynomial_equation, color=border_color, corner_radius=border_radius
        )
    )
    return [generic_polynomial_equation, equation_rectangle]
