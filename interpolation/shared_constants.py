"""shared_constants.py
Constants that are shared across multiple scenes
in the interpolation lesson."""

import logging
from typing import Optional, List, Union

from manim_slides.slide import ThreeDSlide, Slide
from manim import (
    GRAY,
    Mobject,
)

from helper_functions.general_utilities import (
    clear_screen,
    format_to_parenthesis_if_negative,
)
from helper_functions.premade_slides import create_title_frame
from helper_functions.graph import DEFAULT_AXES_INTERVALS
from helper_functions.math_functions import witch_of_agnesi


def get_witch_of_agnesi_points_from_interval(
    x_start: int,
    x_end: int,
    x_spacing: Optional[float] = None,
    witch_of_agnesi_radius: Optional[int] = None,
) -> List[List[float]]:
    """Gets output of the witch of Agnesi function for a certain interval and spacing.

    :param x_start: The starting x value for the interval.

    :param x_end: The ending x value for the interval.

    :param x_spacing: The spacing between each x value. Default is 1.

    :param witch_of_agnesi_radius: The radius to use for the Witch of Agnesi function. Default is 1.

    :returns The witch of agnesi values in format [x,y] as lists.
    """
    if x_spacing is None:
        x_spacing = 1
    if witch_of_agnesi_radius is None:
        witch_of_agnesi_radius = 1
    evaluated_points = []
    for x_value in range(x_start, x_end + x_spacing, x_spacing):
        agnesi_value = witch_of_agnesi(x_value, witch_of_agnesi_radius)
        point_to_draw = [x_value, agnesi_value, 0]
        evaluated_points.append(point_to_draw[0:2])
    return evaluated_points


def add_witch_of_agnesi_points(
    scene_reference: Union[Slide, ThreeDSlide],
    points: List[List[float]],
    animation_run_time: Optional[float] = None,
) -> List[Mobject]:
    """Adds points from get_witch_of_agnesi_points_from_interval.
    More generic actually but it has the color settings we want for the witch of agnesi function

    :param scene_reference: Self reference to the current slide.

    :param points: A list of the points in format (x,y) to plot.

    :param animation_run_time: How long to show the animation of the points being added.
    """
    all_created_point_objects = []
    for x_value, y_value in points:
        point_to_draw = [x_value, y_value, 0]
        created_objects = scene_reference.axes.add_point(
            point_to_draw,
            dot_color=GRAY,
            show_coordinates=True,
            round_coordinates_to_decimals=2,
            animation_run_time=animation_run_time,
            return_created_objects=True,
            show_z_coordinate=False,
        )
        # created_objects[0] will always give us the dot object
        all_created_point_objects.append(created_objects[0])
    return all_created_point_objects


def set_title_heading_to(
    scene_reference: Union[Slide, ThreeDSlide],
    title: str,
    subtitle: Optional[str] = None,
    title_scale: Optional[float] = None,
    subtitle_scale: Optional[float] = None,
) -> None:
    """Adds a title slide as a new separate slide
    based on a passed text.

    :param scene_reference: Self reference to the current slide.

    :param title: The title heading to set.

    :param subtitle: Subtitle text if any.

    :param title_scale: Optionally scale down (or up!) the title. By default the scale is 1.

    :param title_scale: Optionally scale down (or up!) the subtitle. By default the scale is 1.
    """
    old_mobjects = scene_reference.mobjects
    clear_screen(scene_reference)
    scene_reference.next_slide()
    title_frame = create_title_frame(
        scene_reference,
        title,
        subtitle,
        title_scale=title_scale,
        subtitle_scale=subtitle_scale,
    )
    scene_reference.add(title_frame)
    scene_reference.next_slide()
    scene_reference.remove(title_frame)
    # Get old mobjects back
    for old_mobject in old_mobjects:
        scene_reference.add(old_mobject)


def create_logger(scene_reference: Union[Slide, ThreeDSlide]) -> None:
    """Initializes a logger on scene_reference.

    :param scene_reference: Self reference to the current slide.
    """
    scene_reference.logger = logging.getLogger(type(scene_reference).__name__)


def generate_generic_polynomial_equation(
    degree: int,
    centered_point: Optional[float] = None,
    show_implicit_powers: Optional[bool] = None,
) -> List[str]:
    """Generate the TeX equation for a generic polynomial equation
    (y=c_1x^{degree}...). This is not used in the code that much, a TODO is to make more places in the code use it!


    :param degree: The degree of the polynomial.

    :param centered_point: If not None, will generate a centering generic polynomial centered around the point
    with this passed value.

    :param show_implicit_powers: If True, will explicitly print out the x^0 and x^1 which is part of the generic equation even if
    it is implicit. Default is False.

    :returns A list of TeX strings that can be passed to MathTex() as args for example.
    """
    if show_implicit_powers is None:
        show_implicit_powers = False
    if centered_point is None:
        x_string = "x"
    else:
        x_string = f"(x-{format_to_parenthesis_if_negative(centered_point)})"
    latex_strings_list = ["y="]
    x_powers = list(range(1, degree + 1))
    x_powers.reverse()
    for i in range(degree - 1 if not show_implicit_powers else len(x_powers)):
        latex_strings_list.extend(
            ["c_{%d}{%s}^{%d}" % (i + 1, x_string, x_powers[i]), "+"]
        )
    # Remove the x^0 and x^1 that are implicit if not specifically told to do so
    if not show_implicit_powers:
        latex_strings_list.extend(["c_{%d}%s" % (degree, x_string), "+"])
    # Add the last variable representing the coefficient
    latex_strings_list.extend(
        ["c_{%d} %s" % (degree + 1, r"x^0" if show_implicit_powers else "")]
    )
    return latex_strings_list


# Constants not used in the code that much, a TODO is to make more places in the code use it!
GENERIC_POLYNOMIAL_EQUATION_DEGREE_1 = generate_generic_polynomial_equation(degree=1)
GENERIC_POLYNOMIAL_EQUATION_DEGREE_2 = generate_generic_polynomial_equation(degree=2)
GENERIC_POLYNOMIAL_EQUATION_DEGREE_3 = generate_generic_polynomial_equation(degree=3)


# Different scenes will use points generated by the Witch of Agnesi function to demonstrate different aspects of interpolation
# We therefore create the points here.
WITCH_OF_AGNESI_RADIUS = 2
X_SPACING = 2
evaluated_points = get_witch_of_agnesi_points_from_interval(
    2, 6, witch_of_agnesi_radius=WITCH_OF_AGNESI_RADIUS, x_spacing=X_SPACING
)
more_evaluated_points = get_witch_of_agnesi_points_from_interval(
    -10, 0, witch_of_agnesi_radius=WITCH_OF_AGNESI_RADIUS, x_spacing=X_SPACING
)
even_more_evaluated_points = get_witch_of_agnesi_points_from_interval(
    8, 10, witch_of_agnesi_radius=WITCH_OF_AGNESI_RADIUS, x_spacing=X_SPACING
)
all_evaluated_points = (
    evaluated_points + more_evaluated_points + even_more_evaluated_points
)
all_evaluated_points_x = [point[0] for point in all_evaluated_points]
all_evaluated_points_x_interval = [
    min(all_evaluated_points_x),
    max(all_evaluated_points_x),
]
# Sort all evaluated points by X
sorted_all_evaluated_points = all_evaluated_points.copy()
sorted_all_evaluated_points.sort(key=lambda point: point[0])
INTERPOLATION_DEFAULT_AXES_INTERVAL = DEFAULT_AXES_INTERVALS
INTERPOLATION_DEFAULT_AXES_INTERVAL[0] = INTERPOLATION_DEFAULT_AXES_INTERVAL[1] = [
    0,
    12,
]

# When we move a polynomial to the corner of the graph, we want to scale it down
# This scale is used across multiple files so it is for convenience defined here
CORNER_EQUATIONS_SCALE = 0.8
