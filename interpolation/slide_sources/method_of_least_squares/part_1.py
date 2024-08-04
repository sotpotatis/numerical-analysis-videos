"""method_of_least_squares/part_1.py
Briefly explains the method of least squares for interpolation.
Part one includes graphically introducing the method of least squares."""

from manim_slides.slide import ThreeDSlide
import logging
from typing import Optional, List, Union

from manim import (
    Create,
    ValueTracker,
    Mobject,
    Arrow3D,
    RED,
    YELLOW,
    Tex,
    DR,
    VGroup,
    BackgroundRectangle,
    FadeIn,
    Line,
    DOWN,
    SurroundingRectangle,
    BLACK,
    MED_SMALL_BUFF,
    DrawBorderThenFill,
    DL,
    Line3D,
)
from sympy import lambdify

from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.graph import SYMBOL_X
from helper_functions.point_interpolation import (
    interpolation_coefficients_to_function_template,
)
from helper_functions.graph import AxesAndGraphHelper
from interpolation.shared_constants import (
    sorted_all_evaluated_points,
    set_title_heading_to,
    add_witch_of_agnesi_points,
    create_logger,
)
from interpolation.value_tracker_plotting import (
    generate_updater_for_plot_graph_according_to_constant_values,
    generate_updater_for_equation_related_to_constant_values,
)
from interpolation.slide_sources.method_of_least_squares.shared_constants import (
    c1_real,
    c2_real,
    c3_real,
)


class MethodOfLeastSquaresPartOne(ThreeDSlide):
    def construct(self):
        create_logger(self)
        set_title_heading_to(self, "Minsta kvadratmetoden")
        self.axes = AxesAndGraphHelper(
            self, interval=[[-11, 11], [-3, 5]], use_2d_axes_class=True
        )
        # Use the same points as splines when demonstrating least squares
        add_witch_of_agnesi_points(
            self, sorted_all_evaluated_points, animation_run_time=1
        )
        # Fit a 2nd degree polynomial to the 11 datapoints
        self.next_slide()
        (
            generic_polynomial_equation,
            generic_polynomial_equation_rectangle,
        ) = create_equation_with_border("y=c_1x^2+c_2x+c_3")
        generic_polynomial_equation_rectangle.set_fill(color=BLACK, opacity=1)
        self.add(generic_polynomial_equation_rectangle)
        self.play(Create(generic_polynomial_equation))
        self.wait(0.5)
        self.next_slide()
        self.logger.info(
            f"Fit a second degree polynomial to datapoints with coefficients: {c1_real}, {c2_real} and {c3_real}"
        )
        for object in [
            generic_polynomial_equation_rectangle,
            generic_polynomial_equation,
        ]:
            self.remove(object)
        # Add value trackers for the different coefficients
        c1_min = c1_real * 3 / 4
        c1_max = c1_real * 3 / 2
        c2_min = c2_max = c2_real  # c2 is not animated
        c3_min = c3_real * 1 / 2
        c3_max = c3_real * 3 / 2
        c1 = ValueTracker(c1_real)
        c2 = ValueTracker(c2_real)
        c3 = ValueTracker(c3_real)
        self.value_trackers = [c3, c2, c1]
        # Add function plot
        least_squares_polynomial_value_updater = (
            generate_updater_for_plot_graph_according_to_constant_values(
                self, self.value_trackers, SYMBOL_X, RED
            )
        )
        least_squares_polynomial_value_plot = least_squares_polynomial_value_updater(
            return_new_plot=True
        )
        # Save the plot that has the smallest residual for later addition
        original_least_squares_polynomial_value_plot = (
            least_squares_polynomial_value_plot.copy()
        )
        least_squares_polynomial_value_plot.add_updater(
            least_squares_polynomial_value_updater
        )
        self.add(least_squares_polynomial_value_plot)
        self.wait(0.5)
        self.next_slide()
        # Add plots for the residuals. Do this by creating their updater and calling it to get
        # the initial lines
        residual_line_updaters = [
            self.create_residual_lines_updater(point)
            for point in sorted_all_evaluated_points
        ]
        residual_lines = [
            residual_line_updater(return_new_line=True)
            for residual_line_updater in residual_line_updaters
        ]
        for i in range(len(residual_lines)):
            residual_line = residual_lines[i]
            residual_line_updater = residual_line_updaters[i]
            residual_line.add_updater(residual_line_updater)
        self.axes.axes_object.add(*residual_lines)
        self.wait(0.5)
        self.next_slide()
        # Add a rectangle to each of the residual lines to show the residual lines
        residual_line_rectangles = []
        for residual_line in residual_lines:
            residual_line_rectangle = SurroundingRectangle(
                residual_line, color=YELLOW, buff=MED_SMALL_BUFF
            )
            self.play(
                DrawBorderThenFill(residual_line_rectangle),
                run_time=1 / (len(residual_lines)),
            )
            residual_line_rectangles.append(residual_line_rectangle)
        # Add text explaining that "these are called the residuals"
        residuals_text = Tex("Residualer", color=YELLOW)
        residuals_text.scale(1.5)
        residuals_text.to_edge(DOWN)
        residuals_text_background = BackgroundRectangle(
            residuals_text, fill_opacity=1, stroke_width=0
        )
        # Add two arrows
        residual_arrow_1 = Arrow3D(
            start=residuals_text.get_corner(DR),
            end=residual_line_rectangles[-1].get_corner(DL),
            color=YELLOW,
        )
        residual_arrow_2 = Arrow3D(
            start=residuals_text.get_corner(DL),
            end=residual_line_rectangles[0].get_corner(DR),
            color=YELLOW,
        )
        residuals_text_group = VGroup(
            residual_arrow_1,
            residual_arrow_2,
            residuals_text_background,
            residuals_text,
        )
        self.play(FadeIn(residuals_text_group))
        self.next_slide()
        # Add the purpose of the method of least squares
        residuals_explanation_text = Tex(
            r"""Minstakvadratmetoden minimerar \textit{storleken} av \textit{summan} av 
        alla individuella \textit{residualer} i \textit{kvadrat}.
        """
        )
        residuals_explanation_text.scale(0.75)
        residuals_explanation_text.next_to(residuals_text, DOWN)
        residuals_explanation_text_background = BackgroundRectangle(
            residuals_explanation_text, fill_opacity=1, stroke_width=0
        )
        self.add(residuals_explanation_text_background)
        self.play(Create(residuals_explanation_text))
        self.wait(0.5)
        self.next_slide()
        # Remove residual arrows and text
        objects_to_remove = residual_line_rectangles.copy()
        objects_to_remove.extend(
            [
                residuals_text,
                residuals_text_background,
                residuals_explanation_text,
                residuals_explanation_text_background,
                residual_arrow_1,
                residual_arrow_2,
            ]
        )
        for object in objects_to_remove:
            self.remove(object)
        self.wait(0.5)
        self.next_slide()
        # Add equation updater that animates the different values of the coefficients
        polynomial_equation_value_updater = (
            generate_updater_for_equation_related_to_constant_values(
                self, self.value_trackers
            )
        )
        polynomial_equation = polynomial_equation_value_updater(
            return_generic_equation=True
        )
        polynomial_equation.add_updater(polynomial_equation_value_updater)
        self.remove(generic_polynomial_equation)
        self.add(polynomial_equation)
        # Animate the fitting of the polynomial
        coefficients_change_run_time = 1 / 2  # Totally this will run for 2 seconds
        self.play(c3.animate.set_value(c3_min), run_time=coefficients_change_run_time)
        self.play(c1.animate.set_value(c1_min), run_time=coefficients_change_run_time)
        self.play(c1.animate.set_value(c1_max), run_time=coefficients_change_run_time)
        self.play(c3.animate.set_value(c3_max), run_time=coefficients_change_run_time)
        self.next_slide()
        # Remove the objects with updaters that were previously used, because the updaters slow down the code.
        # The least_squares_polynomial_value_plot is re-added without updaters
        polynomial_equation.clear_updaters()
        least_squares_polynomial_value_plot.clear_updaters()
        self.remove(polynomial_equation)
        for submobject in polynomial_equation.submobjects:
            self.remove(submobject)
        self.remove(least_squares_polynomial_value_plot)
        for submobject in least_squares_polynomial_value_plot.submobjects:
            self.remove(submobject)
        for residual_line in residual_lines:
            residual_line.clear_updaters()
            for submobject in residual_line.submobjects:
                self.remove(submobject)
            self.remove(residual_line)
        self.add(original_least_squares_polynomial_value_plot)
        self.wait(0.5)
        self.next_slide()

    def create_residual_lines_updater(self, point: List[float]) -> callable:
        """Creates a value tracker that plot residual "lines" to the graph.

        :param point: This function creates only one value tracker, and it will be for the point that you pass to it.
        Pass it via this argument.
        """

        def residual_line_updater(
            object: Optional[Mobject] = None,
            dt: Optional[float] = None,
            return_new_line: Optional[bool] = None,
        ) -> Optional[Union[Line, VGroup]]:
            """A value tracker updater that plots a residual "lines" to the graph.

            :param object: Internal parameter passed by Manim. The current instance of the same object type that the updater was added to.

            :param dt: The current change in time. Provided by Manim.

            :param return_new_line If True, will return the new lines as a function return.
            This can be used to create the first instance of the graph, and then subscribe to the updater_function
            """
            if return_new_line is None:
                return_new_line = False
            logger = logging.getLogger(__name__)
            # Get a function representing the current value tracker values
            value_tracker_values = [
                value_tracker.get_value() for value_tracker in self.value_trackers
            ]
            current_function_template = interpolation_coefficients_to_function_template(
                value_tracker_values, SYMBOL_X
            )
            current_function = lambdify([SYMBOL_X], current_function_template, "numpy")
            # Plot the residuals by evaluating the function at the known datapoints
            point_x, point_y = point
            function_x, function_y, function_z = current_function(point_x)
            function_value_coordinates = self.axes.axes_object.coords_to_point(
                point_x, function_y, 0
            )
            point_coordinates = self.axes.axes_object.coords_to_point(
                point_x, point_y, 0
            )
            function_value_is_start = function_y < point_y
            logger.debug(
                f"""Updating residual lines, object is {object} and dt={dt}, value tracker values: {value_tracker_values},
               function value at point ({point_x, point_y}) is ({function_x}, {function_y}, {function_z}),
               line starts at function value? {function_value_is_start}"""
            )
            graph_line = Line3D(
                start=(
                    function_value_coordinates
                    if function_value_is_start
                    else point_coordinates
                ),
                end=(
                    point_coordinates
                    if function_value_is_start
                    else function_value_coordinates
                ),
                color=YELLOW,
            )
            if object is not None:
                object.become(graph_line)
            if return_new_line:
                return graph_line

        return residual_line_updater
