"""method_of_least_squares.py
Briefly explains the method of least squares for interpolation."""

from manim_slides.slide import ThreeDSlide
import logging
from typing import Optional, List, Union

from manim import (
    MathTex,
    Create,
    RIGHT,
    UP,
    ReplacementTransform,
    ValueTracker,
    Mobject,
    Arrow3D,
    ScaleInPlace,
    RED,
    YELLOW,
    Tex,
    WHITE,
    GrowFromCenter,
    DR,
    VGroup,
    BackgroundRectangle,
    FadeIn,
    Line,
    ORANGE,
)
from sympy import lambdify

from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.general_utilities import (
    clear_screen,
    play_multiple,
)
from helper_functions.graph import SYMBOL_X
from helper_functions.latex_utilities import (
    create_cases,
    create_matrix,
)
from helper_functions.loading.loading import LoadingSpinner
from helper_functions.point_interpolation import (
    interpolate_over,
    interpolation_coefficients_to_function_template,
)
from helper_functions.graph import AxesAndGraphHelper
from interpolation.shared_constants import (
    all_evaluated_points,
    set_title_heading_to,
    add_witch_of_agnesi_points,
    create_logger,
    CORNER_EQUATIONS_SCALE,
)
from interpolation.slide_sources.interpolation_equations import (
    illustrate_interpolation_equations,
    create_interpolation_matrix,
)
from interpolation.value_tracker_plotting import (
    generate_updater_for_plot_graph_according_to_constant_values,
    generate_updater_for_equation_related_to_constant_values,
)
from helper_functions.matrix_utilities import transpose_matrix


class MethodOfLeastSquares(ThreeDSlide):
    def construct(self):
        create_logger(self)
        set_title_heading_to(self, "Minsta kvadratmetoden")
        self.axes = AxesAndGraphHelper(
            self, interval=[[-10, 10], [0, 5]], use_2d_axes_class=True
        )
        # Use the same points as splines when demonstrating least squares
        add_witch_of_agnesi_points(self, all_evaluated_points, animation_run_time=1)
        # Fit a 2nd degree polynomial to the 11 datapoints
        self.next_slide()
        generic_polynomial_equation, generic_polynomial_equation_rectangle = (
            create_equation_with_border("y=c_1x^2+c_2x+c_3")
        )
        generic_polynomial_equation.to_edge(RIGHT)
        self.add(generic_polynomial_equation_rectangle)
        self.play(Create(generic_polynomial_equation))
        self.next_slide()
        self.play(ScaleInPlace(generic_polynomial_equation, CORNER_EQUATIONS_SCALE))
        self.next_slide()
        # Calculate the real, true, best, whatever, line of best fit solution
        c3_real, c2_real, c1_real = interpolate_over(
            all_evaluated_points, polynomial_degree=2, line_of_best_fit=True
        )
        self.logger.info(
            f"Fit a second degree polynomial to datapoints with coefficients: {c1_real}, {c2_real} and {c3_real}"
        )
        # Add value trackers for the different coefficients
        c1_real * 3 / 4
        c1_real * 3 / 2
        c2_min = c2_max = c2_real  # c2 is not animated
        c3_real * 1 / 2
        c3_real * 3 / 2
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
        least_squares_polynomial_value_plot.add_updater(
            least_squares_polynomial_value_updater
        )
        self.add(least_squares_polynomial_value_plot)
        self.next_slide()
        # Add plots for the residuals. Do this by creating their updater and calling it to get
        # the initial lines
        residual_line_updaters = [
            self.create_residual_lines_updater(point) for point in all_evaluated_points
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
        self.next_slide()
        # Add an arrow next to each of the residual lines
        residual_line_arrows = []
        for residual_line in residual_lines:
            residual_line_start = residual_line.get_start()
            residual_line_middle = residual_line_start
            # Get middle Y point of residual line
            residual_line_middle[1] = residual_line_middle[1] / 2
            # Specify start and endpoints for the arrow. Make it start a little to the left of the residual
            # and end a little to the right of the residual
            arrow_start = residual_line_middle
            arrow_start[0] += 1
            arrow_end = arrow_start.copy()
            arrow_end[0] += 1
            arrow = Arrow3D(
                start=self.axes.axes_object.coords_to_point(*arrow_start),
                end=self.axes.axes_object.coords_to_point(*arrow_end),
                color=YELLOW,
            )
            self.add(arrow)
            residual_line_arrows.append(arrow)
        # Add text explaining that "these are called the residuals"
        residuals_text = Tex("Residualer", color=YELLOW)
        residuals_text.scale(2.5)
        residuals_text.to_corner(DR)
        residuals_text_background = BackgroundRectangle(
            residuals_text, fill_opacity=1, stroke_width=0
        )
        residuals_text_group = VGroup(residuals_text_background, residuals_text)
        self.play(FadeIn(residuals_text_group))
        self.next_slide()
        # Remove residual arrows and text
        objects_to_remove = residual_lines.copy()
        objects_to_remove.extend([residuals_text, residuals_text_background])
        for object in objects_to_remove:
            self.remove(object)
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
        # Animate the fitting of the polynomial TODO readd, commented out for speed
        # self.play(c3.animate.set_value(c3_min), run_time=COEFFICIENTS_CHANGE_RUN_TIME)
        # self.play(c1.animate.set_value(c1_min), run_time=COEFFICIENTS_CHANGE_RUN_TIME)
        # self.play(c1.animate.set_value(c1_max), run_time=COEFFICIENTS_CHANGE_RUN_TIME)
        # self.play(c3.animate.set_value(c3_max), run_time=COEFFICIENTS_CHANGE_RUN_TIME)
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
        self.add(least_squares_polynomial_value_plot)
        self.logger.info("Rendering slides highlighting the calculations...")
        # Show how to fit the polynomial
        generic_equation_system, point_equation_system = (
            illustrate_interpolation_equations(self, all_evaluated_points, 2)
        )
        self.next_slide()
        clear_screen(self)
        # Show the generic equation
        generic_equation_system.move_to([0, 0, 0])
        generic_equation_system.set_color(WHITE)
        generic_equation_system.scale(2)
        self.play(GrowFromCenter(generic_equation_system))
        self.next_slide()
        # Show how to rewrite the equation system in latex format
        matrix_equation_system, matrix_equation_strings = create_interpolation_matrix(
            all_evaluated_points, 2
        )
        a_matrix_values, x_matrix_values, b_matrix_values = matrix_equation_strings
        self.play(ReplacementTransform(generic_equation_system, matrix_equation_system))
        self.next_slide()
        a_matrix_string = create_matrix(a_matrix_values)
        x_matrix_string = create_matrix(x_matrix_values)
        b_matrix_string = create_matrix(b_matrix_values)
        # Highlight the names of the matricies
        a_matrix_string = r"\underbrace{%s}_{\vec A}" % (a_matrix_string)
        x_matrix_string = r"\underbrace{%s}_{\vec x}" % (x_matrix_string)
        b_matrix_string = r"\underbrace{%s}_{\vec b}" % (b_matrix_string)
        matrix_equation_system_with_highlighted_names = MathTex(
            a_matrix_string + x_matrix_string + "=" + b_matrix_string
        )
        self.play(
            ReplacementTransform(
                matrix_equation_system, matrix_equation_system_with_highlighted_names
            )
        )
        self.next_slide()
        # Now, indicate that we multiply the left side with A transponse
        matrix_equation_system_with_transpose_indication = MathTex(
            "A^T" + a_matrix_string + x_matrix_string + "= A^T" + b_matrix_string
        )
        self.play(
            ReplacementTransform(
                matrix_equation_system_with_highlighted_names,
                matrix_equation_system_with_transpose_indication,
            )
        )
        self.next_slide()
        # Now, write out the values of A transpose
        a_matrix_transpose = transpose_matrix(a_matrix_values)
        a_matrix_transpose_string = create_matrix(a_matrix_transpose)
        a_matrix_transpose_string = r"\underbrace{%s}_{\vec A^T}" % (
            a_matrix_transpose_string
        )
        matrix_equation_system_with_transpose_values = MathTex(
            a_matrix_transpose_string
            + a_matrix_string
            + x_matrix_string
            + f"= {a_matrix_transpose_string}"
            + b_matrix_string
        )
        self.play(
            ReplacementTransform(
                matrix_equation_system_with_highlighted_names,
                matrix_equation_system_with_transpose_values,
            )
        )
        # Play animation of solving the system
        loading_spinner = LoadingSpinner(
            self, before_addition_function=lambda object: object.move_to([0, 0, 0])
        )
        loading_spinner.spin(duration=3)
        self.remove(*loading_spinner.created_objects)
        solution_equation_system = MathTex(
            create_cases(
                [f"c_1={c1_real}", f"c_2={c2_real}", f"c_3={c3_real}"],
                include_math_environment_start=False,
            )
        )
        self.play(
            ReplacementTransform(
                matrix_equation_system_with_transpose_values, solution_equation_system
            )
        )
        self.next_slide()
        clear_screen(self)
        self.next_slide()
        # Plot the resulting interpolating polynomial
        self.axes.create_axes(self)
        self.axes.plot_function(
            graph_function=interpolation_coefficients_to_function_template(
                [c3_real, c2_real, c1_real], SYMBOL_X
            ),
            range_to_use_for_function=[-10, 10],
            input_variables=[SYMBOL_X],
        )
        rounded_coefficients = [
            round(coefficient, 2) for coefficient in [c1_real, c2_real, c3_real]
        ]
        interpolation_polynomial_equation, interpolation_polynomial_equation_border = (
            create_equation_with_border(
                "y={}x^2+{}x+{}".format(*rounded_coefficients),
                scale=CORNER_EQUATIONS_SCALE,
            )
        )
        self.add(interpolation_polynomial_equation_border)
        self.play(Create(interpolation_polynomial_equation))
        self.next_slide()
        # Show the general equation for least squares
        clear_screen(self)
        general_matrix_equation, general_matrix_equation_border = (
            create_equation_with_border(r"\vec A\vec x =  \vec b", scale=1.5)
        )
        general_matrix_equation_group = VGroup(
            general_matrix_equation, general_matrix_equation_border
        )
        self.play(GrowFromCenter(general_matrix_equation_group))
        self.next_slide()
        # Fade the general matrix equation into general least squares equation
        general_least_squares_equation, general_least_squares_border = (
            create_equation_with_border(
                r"\vec A^T\vec A\vec x =  \vec A^T \vec b", scale=1.5
            )
        )
        general_least_squares_equation_group = VGroup(
            general_least_squares_equation, general_least_squares_border
        )
        self.play(
            ReplacementTransform(
                general_matrix_equation_group, general_least_squares_equation_group
            )
        )
        self.next_slide()
        # Add heading and explanation about how the method of least squares works
        heading = Tex("Minsta kvadratmetoden", color=ORANGE)
        heading.scale(1.5)
        least_squares_explanation = Tex(
            r"""Konstruera ett system av ekvationer för att interpolera över önskat antal punkter.
        (se tidigare i videon)
        Skriv om systemet på matrisform, där $\vec A$ är koefficientmatris och $\vec b$ är högerledsmatris. 
        Låt $\vec x$ representera de sökta koefficienterna för interpolationspolynomet du vill skapa.
        Ekvationssystemet som ska lösas ges då av:"""
        )
        least_squares_explanation.next_to(general_least_squares_equation, UP)
        heading.next_to(least_squares_explanation, UP)
        play_multiple(self, [least_squares_explanation, heading], Create)

    def create_residual_lines_updater(self, point: List[float]) -> callable:
        """Creates a value tracker that plot residual "lines" to the graph.

        :param point: This function creates only one value tracker, and it will be for the point that you pass to it.
        Pass it via this argument.
        """

        def residual_line_updater(
            object: Optional[Mobject] = None,
            dt: Optional[float] = None,
            return_new_line: Optional[bool] = None,
            include_residual_value: Optional[bool] = False,
        ) -> Optional[Union[Line, VGroup]]:
            """A value tracker updater that plots a residual "lines" to the graph.

            :param object: Internal parameter passed by Manim. The current instance of the same object type that the updater was added to.

            :param dt: The current change in time. Provided by Manim.

            :param return_new_lines If True, will return the new lines as a function return.
            This can be used to create the first instance of the graph, and then subscribe to the updater_function

            :param include_residual_value: If True, will include the residual value
            by adding it next to the line."""
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
            graph_line = Line(
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
