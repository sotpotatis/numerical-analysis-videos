"""interpolation_equations.py
When interpolating, you need to fit data to a set of equations.
This function contains some helpers for illustrating this visually."""

import logging
from typing import Union, List, Tuple, Optional

from manim import (
    Arrow3D,
    ReplacementTransform,
    Create,
    VGroup,
    BackgroundRectangle,
    DR,
    MathTex,
    UP,
    WHITE,
)
from manim_slides.slide import Slide, ThreeDSlide

from helper_functions.color_utilities import cycle_through_color_wheel
from helper_functions.latex_utilities import create_cases, create_matrix


logger = logging.getLogger(__name__)


def generate_interpolation_polynomial_equation(
    point_x: float,
    point_y: float,
    polynomial_degree: int,
    round_points_to_decimals: Optional[int] = None,
) -> str:
    """To create an interpolation polynomial, you could solve an equation system of cases including the x and y points that you want the polynomial to go over.
    This function creates the text for such an equation for a specific point.

    :param point_x: The x value to create the equation for.

    :param point_y: The y value to create the equation for.

    :param polynomial_degree: The degree of the polynomial to interpolate over.

    :param round_points_to_decimals: Set how many decimals to round x and y values to. Defaults to 2 decimals.
    """
    if round_points_to_decimals is None:
        round_points_to_decimals = 2
    equation = f"{round(point_y, round_points_to_decimals)}="
    coefficient_numbers = list(range(1, polynomial_degree + 2))
    # If we have the equation template y=c1*x^2+c2*x+c3, the first coefficient number corresponds to the highest
    # integer we should power x to. Create a list for those
    coefficient_powers = coefficient_numbers[::-1][1:]
    for i in range(len(coefficient_numbers)):
        equation += "c_{%d}" % (coefficient_numbers[i])
        point_x_rounded = round(point_x, round_points_to_decimals)
        point_x_display_text = (
            f"({point_x_rounded})" if point_x < 0 else repr(point_x_rounded)
        )
        if i < len(coefficient_numbers) - 1:
            equation += "\cdot {%s}^{%d}" % (
                point_x_display_text,
                coefficient_powers[i],
            )
            equation += "+" if point_x >= 0 else "-"
    return equation


def illustrate_interpolation_equations(
    scene_reference: Union[Slide, ThreeDSlide],
    points_to_include: List[float],
    polynomial_degree: int,
    round_points_to_decimals: Optional[int] = None,
    play_replacement_animation: Optional[bool] = None,
    generic_equation_system_positioning_function: Optional[callable] = None,
) -> Tuple[MathTex, MathTex]:
    """To create an interpolation polynomial, you could solve an equation system of cases including the x and y points that you want the polynomial to go over.
    This function aims to illustrate this in an intuitive way.

    :param scene_reference: Reference to the scene to add the illustrations to.

    :param points_to_include: A list of points to include in the illustration.

    :param polynomial_degree: The degree of the polynomial to interpolate over.

    :param round_points_to_decimals: Set how many decimals to round x and y values to. Defaults to 2 decimals.

    :param play_replacement_animation: If True, will play a sexy animation which replaces the interpolation-related equation system
    using ReplacementTransform. This is slow, so if False, a faster alternative will be played.

    :param generic_equation_system_positioning_function: An optional function for setting the position of the generic equation system.
    It receives the current equation system and the interation number (0 to number of points-1).
    If not provided, it will be positioned in manim.DR.
    """
    # Illustrate what each of the points tell us, for example (1,2) tell us x=1, y=2.
    if round_points_to_decimals is None:
        round_points_to_decimals = 2
    if play_replacement_animation is None:
        play_replacement_animation = True
    all_equations = []
    generic_equation_system_group = None
    arrow_colors = cycle_through_color_wheel(
        number_of_colors=len(points_to_include), base_saturation=50
    )
    for i in range(len(points_to_include)):
        point_x, point_y = points_to_include[i]
        point_y_rounded = round(point_y, round_points_to_decimals)
        logger.info(
            f"Adding illustrating arrows and equation for point {point_x}, {point_y_rounded}"
        )
        # Add arrow pointing towards point
        arrow_color = arrow_colors[i]
        arrow_to_point = Arrow3D(
            start=scene_reference.axes.axes_object.coords_to_point(
                point_x, point_y + 1 / 2
            ),
            end=scene_reference.axes.axes_object.coords_to_point(point_x, point_y),
            color=arrow_color,
        )
        # Add equation system related to the particular point
        point_equation_system = MathTex(
            create_cases(
                [f"x={point_x}", f"y={point_y_rounded}"],
                include_math_environment_start=False,
            )
        ).scale(1)
        point_equation_system.next_to(arrow_to_point, UP)
        scene_reference.add(arrow_to_point)
        scene_reference.play(Create(point_equation_system))
        # Generate generic equation
        all_equations.append(
            generate_interpolation_polynomial_equation(
                point_x,
                point_y,
                round_points_to_decimals=round_points_to_decimals,
                polynomial_degree=polynomial_degree,
            )
        )
        previous_generic_equation_system_group = generic_equation_system_group
        cases_text = create_cases(all_equations, include_math_environment_start=False)
        generic_equation_system = MathTex(cases_text)
        if generic_equation_system_positioning_function is None:
            generic_equation_system.to_corner(DR)
        else:
            generic_equation_system_positioning_function(generic_equation_system, i)
        generic_equation_system.set_color_by_tex(all_equations[-1], arrow_color)
        generic_equation_system_background = BackgroundRectangle(
            generic_equation_system, fill_opacity=1
        )
        generic_equation_system_group = VGroup(
            generic_equation_system_background, generic_equation_system
        )
        # Bring generic equation system to front
        generic_equation_system_group.set_z_index(point_equation_system.z_index + 1)
        if previous_generic_equation_system_group is None:
            scene_reference.add(generic_equation_system_group)
        else:
            if play_replacement_animation:
                scene_reference.play(
                    ReplacementTransform(
                        previous_generic_equation_system_group,
                        generic_equation_system_group,
                    )
                )
            else:
                scene_reference.remove(previous_generic_equation_system_group)
                scene_reference.play(Create(generic_equation_system_group))
        scene_reference.wait(0.5)
        scene_reference.next_slide()
    return generic_equation_system, point_equation_system


def create_interpolation_matrix(
    points_to_include: List[float],
    polynomial_degree: int,
    round_points_to_decimals: Optional[int] = None,
) -> Tuple[MathTex, List[List[str]]]:
    """To create an interpolation polynomial, you could solve an equation system of cases including the x and y points
    that you want the polynomial to go over.
    This function creates the equation system in the matrix form for that.
    For a general equation system, see illustrate_interpolation_equations.

    :param points_to_include: A list of points to include in the illustration.

    :param polynomial_degree: The degree of the polynomial to interpolate over.

    :param round_points_to_decimals: Set how many decimals to round x and y values to. Defaults to 2 decimals.

    :returns The created MathTex matrix system and the individual matrix entries as a 2D list of strings [[<row 1, col 1>, <row 1, col 2>,
    <row 1, col m>],
    [<row n, col 1>, <row n, col 2>, ..., <row n, col m>]] for an n by m matrix"""
    if round_points_to_decimals is None:
        round_points_to_decimals = 2
    # Play how the general equation system can be rewritten into a matrix
    a_matrix = []
    b_matrix = []
    x_matrix = [["c_{%r}" % (i)] for i in range(1, polynomial_degree + 2)]
    for matrix_row in range(len(points_to_include)):
        point_x, point_y = points_to_include[matrix_row]
        point_x_rounded = round(point_x, round_points_to_decimals)
        a_matrix_new_entries = [str(point_x_rounded)]
        for i in range(1, polynomial_degree + 1):
            a_matrix_new_entries.append("{%r}^{%d}" % (point_x_rounded, i))
        a_matrix_new_entries.reverse()
        a_matrix.append(a_matrix_new_entries)
        b_matrix.append([round(point_y, round_points_to_decimals)])
    a_matrix_latex = create_matrix(a_matrix)
    b_matrix_latex = create_matrix(b_matrix)
    x_matrix_latex = create_matrix(x_matrix)
    matrix_system_latex = MathTex(
        a_matrix_latex, x_matrix_latex, "=" + b_matrix_latex, color=WHITE
    )
    matrix_system_latex.scale(1.5)
    return matrix_system_latex, [a_matrix, x_matrix, b_matrix]
