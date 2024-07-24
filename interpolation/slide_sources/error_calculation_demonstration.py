"""error_calculation_demonstration.py
Renders a slide used to show how to calculate errors.
Because we need to use a zoomed slide, we need to define the error calculation
slide(s) separately from the others."""

from manim_slides.slide import Slide
from manim import (
    RED,
    YELLOW,
    FadeToColor,
    MovingCameraScene,
)

from helper_functions.general_utilities import (
    play_multiple,
)
from helper_functions.graph import SYMBOL_X
from helper_functions.point_interpolation import (
    interpolate_over,
    interpolation_coefficients_to_function_template,
)
from helper_functions.graph import AxesAndGraphHelper
from interpolation.shared_constants import evaluated_points, add_witch_of_agnesi_points
from sympy import lambdify


class ErrorCalculationDemonstrationSlide(Slide, MovingCameraScene):
    def construct(self):
        return
        self.axes = AxesAndGraphHelper(self, interval=[[0, 4], [0, 5], [0, 4]])
        # Add points from previous interpolation polynomial
        evaluated_point_objects = add_witch_of_agnesi_points(self, evaluated_points)
        # Change color of point objects to distinguish polynomials
        interpolation_first_two_points = evaluated_points[:2]
        interpolation_first_two_point_objects = evaluated_point_objects[:2]
        play_multiple(
            self, interpolation_first_two_point_objects, FadeToColor, color=YELLOW
        )
        self.play(FadeToColor(evaluated_point_objects[-1], RED))
        # Construct a linear interpolation polynomial between the first two points
        linear_interpolation = interpolate_over(interpolation_first_two_points)
        linear_interpolation_function_template = (
            interpolation_coefficients_to_function_template(
                linear_interpolation, SYMBOL_X
            )
        )
        self.axes.plot_function(
            graph_function=linear_interpolation_function_template,
            input_variables=[SYMBOL_X],
            range_to_use_for_function=[
                interpolation_first_two_points[0][0],
                interpolation_first_two_points[-1][0],
            ],
            plot_color=YELLOW,
        )
        # Construct a quadratic interpolation polynomial and plot it
        quadratic_interpolation = interpolate_over(interpolation_first_two_points)
        quadratic_interpolation_function_template = (
            interpolation_coefficients_to_function_template(
                quadratic_interpolation, SYMBOL_X
            )
        )
        self.axes.plot_function(
            graph_function=quadratic_interpolation_function_template,
            input_variables=[SYMBOL_X],
            range_to_use_for_function=[evaluated_points[0][0], evaluated_points[-1][0]],
            plot_color=RED,
        )
        # Shrink axes
        self.axes.create_axes([[0, 3.5], [0, 5], [-10, 10]])
        # Add points for both functions.
        # Indicate the error at x = 3/2 (1.5)
        ERROR_COMPARISON_POINT = 3 / 2
        linear_interpolation_function = lambdify(linear_interpolation_function_template)
        quadratic_interpolation_function = lambdify(
            quadratic_interpolation_function_template
        )
        self.axes.plot_line(vertical=True, coordinate=ERROR_COMPARISON_POINT)
        linear_interpolation_value = linear_interpolation_function(
            ERROR_COMPARISON_POINT
        )
        quadratic_interpolation_value = quadratic_interpolation_function(
            ERROR_COMPARISON_POINT
        )
        # The y values indicate the error
        interpolation_error = abs(
            quadratic_interpolation_value[1] - linear_interpolation_value[1]
        )
        # Zoom to the two points
        self.play(self.camera.frame.animate.scale(0.25).move_to())
