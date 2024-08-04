"""value_tracker_plotting.py
Contains utilities to plot a graph based on the values of value trackers which are related to the coefficients.
This is used in the introduction slide and also the method of least squares demonstration slide.
"""

import logging
from typing import Optional, List

from manim_slides.slide import ThreeDSlide, Slide
from manim import (
    ValueTracker,
    Mobject,
    UR,
    VGroup,
)
from sympy import Symbol

from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.point_interpolation import (
    interpolation_coefficients_to_function_template,
)
from interpolation.shared_constants import (
    CORNER_EQUATIONS_SCALE,
)
from typing import Union


def generate_updater_for_plot_graph_according_to_constant_values(
    scene_reference: Union[Slide, ThreeDSlide],
    value_trackers: List[ValueTracker],
    input_variable: Symbol,
    plot_color: Optional[int] = None,
) -> callable:
    """Generates an updater function for plot_graph_according_to_constant_values that can be used with a value tracker.

    :param value_trackers: The value trackers to get coefficients, in order  in order lowest degree - highest.

    :param input_variable The Sympy input variable/symbol.

    :param plot_color The color of the graph, if any"""

    def updater_function(
        object: Optional[Mobject] = None,
        dt: Optional[float] = None,
        return_new_plot: Optional[bool] = None,
    ):
        """An updater function that can be added to a previously existing graph to render a new graph on the screen.

        :param object: Internal parameter passed by Manim. The current instance of the same object type that the updater was added to.

        :param dt: The current change in time. Provided by Manim.

        :param return_new_plot If True, will return the new plot as a function return.
        This can be used to create the first instance of the graph, and then subscribe to the updater_function.
        (see the construct() function for an example of how this is done)"""
        if return_new_plot is None:
            return_new_plot = False
        logger = logging.getLogger(__name__)
        logger.debug(f"Updating graph value tracker, object is {object} and dt={dt}")
        value_tracker_values = [
            value_tracker.get_value() for value_tracker in value_trackers
        ]
        new_plot = plot_graph_according_to_constant_values(
            scene_reference,
            value_tracker_values,
            input_variable,
            plot_color,
            add_function_plot_to_scene=False,
        )
        logger.info(f"New graph: {new_plot}")
        if object is not None:
            object.become(new_plot)
        if return_new_plot:
            return new_plot

    return updater_function


def generate_updater_for_equation_related_to_constant_values(
    scene_reference: Union[Slide, ThreeDSlide],
    value_trackers: List[ValueTracker],
    scale: Optional[float] = None,
    border_color: Optional = None,
) -> callable:
    """Generates an updater function for the polynomial equation display that can be used with a value tracker.

    :param value_trackers: The value trackers to get coefficients, in order lowest degree - highest.

    :param scale: The scale of the equation display. Default is CORNER_EQUATIONS_SCALE.

    :param border_color: The color of the border of the equation display. Default is None so the default of
    create_equation_with_border will be applied.
    """
    if scale is None:
        scale = CORNER_EQUATIONS_SCALE

    def updater_function(
        object: Optional[Mobject] = None,
        dt: Optional[float] = None,
        return_generic_equation: Optional[bool] = None,
    ) -> Optional[VGroup]:
        """An updater function that can be added to a previously existing graph to render a new graph on the screen.

        :param object: Internal parameter passed by Manim. The current instance of the same object type that the updater was added to.

        :param dt: The current change in time. Provided by Manim.

        :param return_generic_equation If True, will return a generic polynomial equation as a function return.
        This can be used to create the first instance of the equation display, and then subscribe to the updater_function.
        (see the construct() function for an example of how this is done)"""
        if return_generic_equation is None:
            return_generic_equation = False
        value_tracker_values = [
            value_tracker.get_value() for value_tracker in value_trackers
        ]
        # Get the coefficient names: c1, c2, c3 etc.
        coefficient_names = [f"c_{i}" for i in range(1, len(value_tracker_values) + 1)]
        # Reverse lists to get highest degree to lowest since that is what we're displaying in
        value_tracker_values.reverse()
        # We have to scenarios: return an equation like c1x^2+c2x+c3 (generic equation) or the values
        # of the coefficients.
        equation_result = ["y="]
        number_of_coefficients = len(coefficient_names)
        for i in range(number_of_coefficients):
            coefficient_name = coefficient_names[i]
            coefficient_value = value_tracker_values[i]
            # Add the value that x is powered to if applicable.
            if i < number_of_coefficients - 2:
                power_to_string = f"x^{number_of_coefficients - 1 - i}"
            elif i == number_of_coefficients - 2:
                power_to_string = "x"
            else:
                power_to_string = ""
            if return_generic_equation:
                equation_result.append(coefficient_name + power_to_string + "+")
            else:
                equation_result.append(
                    r"\underbrace{%.2f}_{%s}%s+"
                    % (coefficient_value, coefficient_name, power_to_string)
                )
        # Remove the + from the last part of the equation
        equation_result[-1] = equation_result[-1][:-1]
        # Generate new object
        equation, equation_rectangle = create_equation_with_border(
            equation_result, scale=scale, border_color=border_color
        )
        equation_group = VGroup(equation_rectangle, equation)
        equation_group.to_edge(UR)
        if object is not None:
            object.become(equation_group)
        if return_generic_equation:
            return equation_group

    return updater_function


def plot_graph_according_to_constant_values(
    scene_reference: Union[Slide, ThreeDSlide],
    constants: List[float],
    input_variable: Symbol,
    plot_color: Optional[int] = None,
    add_function_plot_to_scene: Optional[bool] = None,
):
    """Plots a graph given a list of constants.

    :param constants A list of constants in order lowest degree - highest.

    :param input_variable The Sympy input variable/symbol.

    :param plot_color The color of the graph, if any.

    :param add_function_plot_to_scene: See AxesAndGraphHelper."""
    constant_function_graph = scene_reference.axes.plot_function(
        graph_function=interpolation_coefficients_to_function_template(
            constants, input_variable
        ),
        input_variables=[input_variable],
        plot_color=plot_color,
        add_function_plot_to_scene=add_function_plot_to_scene,
    )
    return constant_function_graph
