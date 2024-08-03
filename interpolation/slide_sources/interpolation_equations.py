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
    ScaleInPlace,
    GrowFromCenter,
)
from manim_slides.slide import Slide, ThreeDSlide

from helper_functions.color_utilities import cycle_through_color_wheel
from helper_functions.general_utilities import (
    format_to_parenthesis_if_negative,
    clear_screen,
)
from helper_functions.latex_utilities import (
    create_cases,
    create_matrix,
    create_list,
    ListType,
)
from helper_functions.loading.loading import LoadingSpinner

logger = logging.getLogger(__name__)


def generate_interpolation_polynomial_equation(
    point_x: float,
    point_y: float,
    polynomial_degree: int,
    round_points_to_decimals: Optional[int] = None,
    center_around_point: Optional[float] = None,
    calculate_centering_value: Optional[bool] = None,
) -> str:
    """To create an interpolation polynomial, you could solve an equation system of cases including the x and y points that you want the polynomial to go over.
    This function creates the text for such an equation for a specific point.

    :param point_x: The x value to create the equation for.

    :param point_y: The y value to create the equation for.

    :param polynomial_degree: The degree of the polynomial to interpolate over.

    :param round_points_to_decimals: Set how many decimals to round x and y values to. Defaults to 2 decimals.

    :param center_around_point: If set (not None), format the equation system to be centered around the point with the x coordinate
    according to the passed value

    :param calculate_centering_value: If True and center_around_point is not None, calculate the difference from the center_around_point and show that
    instead of the subtraction needed to do to perform the centering. Default is False.
    """
    if round_points_to_decimals is None:
        round_points_to_decimals = 2
    if calculate_centering_value is None:
        calculate_centering_value = False
    equation = f"{round(point_y, round_points_to_decimals)}="
    coefficient_numbers = list(range(1, polynomial_degree + 2))
    # If we have the equation template y=c1*x^2+c2*x+c3, the first coefficient number corresponds to the highest
    # integer we should power x to. Create a list for those
    coefficient_powers = coefficient_numbers[::-1][1:]
    for i in range(len(coefficient_numbers)):
        equation += "c_{%d}" % (coefficient_numbers[i])
        point_x_rounded = round(point_x, round_points_to_decimals)
        # Show the subtraction from the centered point if centering is applied.
        if center_around_point is not None:
            if not calculate_centering_value:
                point_x_display_text = (
                    f"({point_x_rounded}-"
                    + format_to_parenthesis_if_negative(center_around_point)
                    + ")"
                )
            else:
                point_difference_from_centered_value = round(
                    point_x_rounded - center_around_point, round_points_to_decimals
                )
                point_x_display_text = format_to_parenthesis_if_negative(
                    point_difference_from_centered_value
                )
        else:
            point_x_display_text = format_to_parenthesis_if_negative(point_x_rounded)
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
    center_around_point: Optional[float] = None,
    calculate_centering_value: Optional[bool] = None,
    arrow_length: Optional[int] = None,
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

    :param center_around_point: If set (not None), format the equation system to be centered around the point with the
    x-coordinate according to the passed value

    :param calculate_centering_value: If True and center_around_point is not None, calculate the difference from the center_around_point and show that
    instead of the subtraction needed to do to perform the centering. Default is False.

    :param arrow_length Optionally set the length of the rendered arrow used to point on dots. Default if unset is 1/2. Unit is y "steps".
    """
    # Illustrate what each of the points tell us, for example (1,2) tell us x=1, y=2.
    if round_points_to_decimals is None:
        round_points_to_decimals = 2
    if play_replacement_animation is None:
        play_replacement_animation = True
    if calculate_centering_value is None:
        calculate_centering_value = False
    if arrow_length is None:
        arrow_length = 1 / 2
    all_equations = []
    generic_equation_system_group = None
    arrow_colors = cycle_through_color_wheel(
        number_of_colors=len(points_to_include), base_saturation=50
    )
    for i in range(len(points_to_include)):
        point = points_to_include[i]
        logger.info(f"Adding illustrating arrows and equation for point {point}")
        point_x, point_y = point
        point_y_rounded = round(point_y, round_points_to_decimals)
        # Add arrow pointing towards point
        arrow_color = arrow_colors[i]
        arrow_to_point = Arrow3D(
            start=scene_reference.axes.axes_object.coords_to_point(
                point_x, point_y + arrow_length
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
                center_around_point=center_around_point,
                calculate_centering_value=calculate_centering_value,
            )
        )
        previous_generic_equation_system_group = generic_equation_system_group
        cases_text = create_cases(all_equations, include_math_environment_start=False)
        generic_equation_system = MathTex(cases_text)
        if generic_equation_system_positioning_function is None:
            generic_equation_system.to_corner(DR)
        else:
            generic_equation_system_positioning_function(generic_equation_system, i)
        # Set colors to match arrow color
        for equation_index in range(len(all_equations)):
            generic_equation_system.set_color_by_tex(
                all_equations[equation_index], arrow_colors[equation_index]
            )
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
    center_around_point: Optional[float] = None,
    calculate_centering_value: Optional[bool] = None,
) -> Tuple[MathTex, List[List[str]]]:
    """To create an interpolation polynomial, you could solve an equation system of cases including the x and y points
    that you want the polynomial to go over.
    This function creates the equation system in the matrix form for that.
    For a general equation system, see illustrate_interpolation_equations.

    :param points_to_include: A list of points to include in the illustration.

    :param polynomial_degree: The degree of the polynomial to interpolate over.

    :param round_points_to_decimals: Set how many decimals to round x and y values to. Defaults to 2 decimals.

    :param center_around_point: If set (not None), format the equation system to be centered around the point with the
    x-coordinate according to the passed value

    :param calculate_centering_value: If True and center_around_point is not None, calculate the difference from the center_around_point and show that
    instead of the subtraction needed to do to perform the centering. Default is False.

    :returns The created MathTex matrix system and the individual matrix entries as a 2D list of strings [[<row 1, col 1>, <row 1, col 2>,
    <row 1, col m>],
    [<row n, col 1>, <row n, col 2>, ..., <row n, col m>]] for an n by m matrix"""
    if round_points_to_decimals is None:
        round_points_to_decimals = 2
    if calculate_centering_value is None:
        calculate_centering_value = True
    # Play how the general equation system can be rewritten into a matrix
    a_matrix = []
    b_matrix = []
    x_matrix = [["c_{%r}" % (i)] for i in range(1, polynomial_degree + 2)]
    for matrix_row in range(len(points_to_include)):
        point_x, point_y = points_to_include[matrix_row]
        point_x_rounded = round(point_x, round_points_to_decimals)
        # Display in a special, intuitive way if centering has been applied
        if center_around_point is not None:
            center_around_point_rounded = round(
                center_around_point, round_points_to_decimals
            )
            if calculate_centering_value:
                point_x_display = repr(point_x_rounded - center_around_point_rounded)
            else:
                point_x_display = "{%r}-{%r}" % (
                    point_x_rounded,
                    center_around_point_rounded,
                )
        else:
            point_x_display = repr(point_x_rounded)
        point_x_display = format_to_parenthesis_if_negative(point_x_display)
        a_matrix_new_entries = [1]
        for i in range(1, polynomial_degree + 1):
            a_matrix_new_entries.append("{%s}^{%d}" % (point_x_display, i))
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


def illustrate_solving_interpolation_equation_system(
    scene_reference: Union[Slide, ThreeDSlide],
    points_to_include: List[List[float]],
    polynomial_degree: int,
    generic_equation_system: MathTex,
    center_around_point: Optional[float] = None,
    calculate_centering_value: Optional[bool] = None,
) -> MathTex:
    """Illustrates converting a system of equations to matrix format, then highlights the solution,
    given points to interpolate over.

    :param scene_reference: A reference to the source scene to illustrate in.

    :param points_to_include: A list of polynomials that have been interpolated over.

    :param polynomial_degree: The degree of the interpolating polynomial.

    :param generic_equation_system: Output from illustrate_interpolation_equations.
    The equation system to highlight.

    :param center_around_point: See the docstring of create_interpolation_matrix.

    :param calculate_centering_value: See the docstring of create_interpolation_matrix.
    """
    generic_equation_system.set_color(WHITE)
    clear_screen(scene_reference, [generic_equation_system])
    generic_equation_system.move_to([0, 0, 0])  # Move to center of screen
    scene_reference.play(ScaleInPlace(generic_equation_system, 2))
    scene_reference.next_slide()
    matrix_system_latex, _ = create_interpolation_matrix(
        points_to_include,
        polynomial_degree=polynomial_degree,
        center_around_point=center_around_point,
        calculate_centering_value=calculate_centering_value,
    )
    scene_reference.remove(generic_equation_system)
    scene_reference.play(GrowFromCenter(matrix_system_latex))
    scene_reference.next_slide()
    # Play animation of solving the system
    loading_spinner = LoadingSpinner(
        scene_reference,
        before_addition_function=lambda object: object.move_to([0, 0, 0]),
    )
    loading_spinner.spin(duration=3)
    scene_reference.remove(*loading_spinner.created_objects)
    return matrix_system_latex


def create_interpolation_general_method_tex_string(centering: bool) -> str:
    """Returns a LaTeX string for explaining the general method of interpolation. This can be used to highlight generally how
    to perform polynomial interpolation.

    :param centering: If True, returns the method that should be applied if you're centering a polynomial.
    If False, returns the "standard" interpolation polynomial creation method.
    """
    # We're using just a standard set of strings but with some simple conditions.
    latex_strings = [
        r"Givet $n+1$ datapunkter, konstruera ett interpolationspolynom $y_n(x)$ av grad $n$"
        + (" centrerat kring punkten med x-värde $m$ " if centering else "")
        + " genom:\n",
        r"För varje punkt $(x_i, y_i)$ i ditt dataset:" + "\n",
        create_list(
            [
                (
                    r"Infoga ekvationen $y_i=c_1"
                    + (
                        r"x_i^{n}+c_2x_i^{n-1}"
                        if not centering
                        else r"\underline{(x_i-m)}^{n}+c_2\underline{(x_i-m)}^{n-1}"
                    )
                    + r"+...+c_{n+1}$ i ett ekvationssystem"
                ),
                r"Lös ekvationssystemet för $c_1$, $c_2$, $...$, $c_{n+1}$. ",
                "Ditt interpolerade polynom ges nu av funktionen $y_n(x)=c_1"
                + (
                    "x^n+c_2x"
                    if not centering
                    else r"\underline{(x-m)}^n+c_2\underline{(x-m)}"
                )
                + "^{n-1}+...+c_{n+1}$",
            ],
            list_type=ListType.NUMBERED_LIST,
        ),
    ]
    return "".join(latex_strings)
