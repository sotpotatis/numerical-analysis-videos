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
    Dot,
    Tex,
    BackgroundRectangle,
    VGroup,
    Line,
    ORANGE,
    Brace,
    RIGHT,
    Create,
    LEFT,
    DOWN,
    MathTex,
    ReplacementTransform,
    WHITE,
    UP,
    always_redraw,
)

from helper_functions.general_utilities import (
    play_multiple,
)
from helper_functions.graph import SYMBOL_X
from helper_functions.point_interpolation import (
    interpolate_over,
    interpolation_coefficients_to_function_template,
)
from helper_functions.graph import AxesAndGraphHelper, X_AXIS_LENGTH, Y_AXIS_LENGTH
from interpolation.shared_constants import (
    evaluated_points,
    add_witch_of_agnesi_points,
    create_logger,
)
from sympy import lambdify


class ErrorCalculationDemonstrationSlide(Slide, MovingCameraScene):
    def construct(self):
        create_logger(self)
        self.camera.frame.set(width=X_AXIS_LENGTH * 1.5, height=Y_AXIS_LENGTH * 1.5)
        self.camera.frame.save_state()
        self.axes = AxesAndGraphHelper(self, interval=[[0, 7], [0, 5]])
        # Add points from the first
        evaluated_point_objects = add_witch_of_agnesi_points(
            self, evaluated_points, animation_run_time=1
        )
        # Change color of point objects to distinguish polynomials
        interpolation_first_two_points = evaluated_points[:2]
        interpolation_first_two_point_objects = evaluated_point_objects[:2]
        interpolation_range = [evaluated_points[0][0], evaluated_points[-1][0]]
        play_multiple(
            self, interpolation_first_two_point_objects, FadeToColor, color=YELLOW
        )
        self.play(FadeToColor(evaluated_point_objects[-1], RED))
        self.next_slide()
        # Construct a linear interpolation polynomial between the first two points
        linear_interpolation = interpolate_over(interpolation_first_two_points)
        linear_interpolation_function_template = (
            interpolation_coefficients_to_function_template(
                linear_interpolation, SYMBOL_X
            )
        )
        linear_interpolation_function_plot = self.axes.plot_function(
            graph_function=linear_interpolation_function_template,
            input_variables=[SYMBOL_X],
            range_to_use_for_function=interpolation_range,
            plot_color=YELLOW,
        )
        # Name the polynomial p_1 and place it on the middle of the graph
        # Kwargs used for get_graph_labels both for the linear and quadratic interpolation
        function_graph_labels_shared_kwargs = {
            "x_val": evaluated_points[-1][0] - 1,
            "dot": False,
        }
        linear_interpolation_function_name_label = (
            self.axes.axes_object.get_graph_label(
                graph=linear_interpolation_function_plot,
                label=MathTex("p_1(x)"),
                color=YELLOW,
                direction=DOWN,
                **function_graph_labels_shared_kwargs,
            )
        )
        self.add(linear_interpolation_function_name_label)
        self.wait(0.5)
        self.next_slide()
        # Construct a quadratic interpolation polynomial and plot it
        quadratic_interpolation = interpolate_over(evaluated_points)
        quadratic_interpolation_function_template = (
            interpolation_coefficients_to_function_template(
                quadratic_interpolation, SYMBOL_X
            )
        )
        quadratic_interpolation_function_plot = self.axes.plot_function(
            graph_function=quadratic_interpolation_function_template,
            input_variables=[SYMBOL_X],
            range_to_use_for_function=interpolation_range,
            plot_color=RED,
        )
        quadratic_interpolation_function_name_label = (
            self.axes.axes_object.get_graph_label(
                graph=quadratic_interpolation_function_plot,
                label=MathTex("p_2(x)"),
                color=RED,
                direction=UP,
                **function_graph_labels_shared_kwargs,
            )
        )
        self.add(quadratic_interpolation_function_name_label)
        self.wait(0.5)
        self.next_slide()
        # Indicate the error at x = 3
        ERROR_COMPARISON_POINT = 3
        # Calculate error for both functions.
        linear_interpolation_function = lambdify(
            [SYMBOL_X], linear_interpolation_function_template, "numpy"
        )
        quadratic_interpolation_function = lambdify(
            [SYMBOL_X], quadratic_interpolation_function_template, "numpy"
        )
        self.axes.plot_line(
            vertical=True, coordinate=ERROR_COMPARISON_POINT, plot_color=WHITE
        )
        error_comparison_line_label = MathTex(f"x={ERROR_COMPARISON_POINT}")
        # The "helper dot" helps to position the label correctly.
        error_comparison_line_label_helper_dot = Dot()
        error_comparison_line_label_helper_dot.move_to(
            self.axes.axes_object.coords_to_point(
                ERROR_COMPARISON_POINT, self.axes.axes_object.y_range[1] - 1, 0
            )
        )
        error_comparison_line_label.next_to(
            error_comparison_line_label_helper_dot, RIGHT
        )
        self.add(error_comparison_line_label)
        _, linear_interpolation_value, _ = linear_interpolation_function(
            ERROR_COMPARISON_POINT
        )
        _, quadratic_interpolation_value, _ = quadratic_interpolation_function(
            ERROR_COMPARISON_POINT
        )
        # The y values indicate the error
        interpolation_error_non_absolute = (
            quadratic_interpolation_value - linear_interpolation_value
        )
        interpolation_error = abs(interpolation_error_non_absolute)
        # Add visualizing dots.
        linear_interpolation_dot = self.axes.add_point(
            [ERROR_COMPARISON_POINT, linear_interpolation_value, 0],
            dot_color=YELLOW,
            return_created_objects=True,
        )[0]
        quadratic_interpolation_dot = self.axes.add_point(
            [ERROR_COMPARISON_POINT, quadratic_interpolation_value, 0],
            dot_color=RED,
            return_created_objects=True,
        )[0]
        interpolation_dots_group = VGroup(
            linear_interpolation_dot, quadratic_interpolation_dot
        )
        # Add question text
        question_text = Tex(
            r'"\textbf{Hur kan vi veta felet vid }$x=%d$\textbf{ om vi använder }$p_1(%d)$\textbf{?}"'
            % (ERROR_COMPARISON_POINT, ERROR_COMPARISON_POINT)
        )
        question_text.scale(1.5)
        question_text_background = BackgroundRectangle(
            question_text, fill_opacity=1, stroke_width=0
        )
        self.add(question_text_background)
        self.play(Create(question_text))
        self.wait(0.5)  # Otherwise the text doesn't render fully
        self.next_slide()
        for object in [question_text, question_text_background]:
            self.remove(object)
        # Add a line indicating the size of the error. Add a brace and a text showing what we're currently calculating
        linear_interpolation_error_comparison_coordinate = [
            ERROR_COMPARISON_POINT,
            linear_interpolation_value,
            0,
        ]
        quadratic_interpolation_error_comparison_coordinate = [
            ERROR_COMPARISON_POINT,
            quadratic_interpolation_value,
            0,
        ]
        starting_point = (
            linear_interpolation_error_comparison_coordinate
            if linear_interpolation_value < quadratic_interpolation_value
            else quadratic_interpolation_error_comparison_coordinate
        )
        error_size_line = Line(
            start=starting_point,
            end=(
                quadratic_interpolation_error_comparison_coordinate
                if starting_point == linear_interpolation_error_comparison_coordinate
                else linear_interpolation_error_comparison_coordinate
            ),
            color=ORANGE,
        )
        error_size_brace = Brace(error_size_line, color=ORANGE)
        error_text = Tex('"Felet"', color=ORANGE)
        error_text.scale(0.75)
        error_text.next_to(error_size_brace, RIGHT)
        play_multiple(self, [error_size_line, error_size_brace], Create)
        self.wait(1)
        self.add(error_text)
        # Zoom to the two dots
        """Previous code: self.play(
            self.camera.frame.animate.scale(0.25).move_to(interpolation_dots_group)
        )"""
        # This covers the width of one x step on the axis. I put this here for reminding me what I want to achieve when I get to fixing this!
        # I don't think this is clean code!
        zoomed_camera_width = X_AXIS_LENGTH / abs(
            self.axes.axes_object.x_range[0] - self.axes.axes_object.x_range[1]
        )
        zoomed_camera_height = (
            interpolation_error
            * 1.25
            * (
                Y_AXIS_LENGTH
                / abs(
                    self.axes.axes_object.y_range[0] - self.axes.axes_object.y_range[1]
                )
            )
        )
        self.logger.info(
            f"""Moving camera to error line by setting width: {zoomed_camera_width},
         height: {zoomed_camera_height}"""
        )
        self.play(
            self.camera.frame.animate.set(
                width=zoomed_camera_width, height=zoomed_camera_height
            ).move_to(error_size_line),
            run_time=2,
        )
        self.wait(1)
        # Zoom out
        self.next_slide()
        # TODO this does not work with Manim-slides, the zoom in slide is not created if
        #  this line is uncommented self.play(Restore(self.camera.frame))
        # Add text for the separate polynomials. Show 16 digits
        linear_interpolation_value_16_floating_points = str(linear_interpolation_value)[
            0:17
        ]
        quadratic_interpolation_value_16_floating_points = str(
            quadratic_interpolation_value
        )[0:17]
        interpolation_error_16_floating_points = str(interpolation_error_non_absolute)[
            0:17
        ]
        interpolation_error_16_floating_points_absolute = str(abs(interpolation_error))[
            0:17
        ]
        linear_interpolation_value_text = MathTex(
            f"p_1({ERROR_COMPARISON_POINT})=",
            linear_interpolation_value_16_floating_points,
            color=YELLOW,
        )
        quadratic_interpolation_value_text = MathTex(
            f"p_2({ERROR_COMPARISON_POINT})=",
            quadratic_interpolation_value_16_floating_points,
            color=RED,
        )
        linear_interpolation_value_text.to_edge(LEFT)
        quadratic_interpolation_value_text.next_to(
            linear_interpolation_value_text, DOWN
        )
        linear_and_quadratic_interpolation_text_groups = VGroup(
            linear_interpolation_value_text, quadratic_interpolation_value_text
        )
        linear_and_quadratic_interpolation_text_background = always_redraw(
            lambda: BackgroundRectangle(
                linear_and_quadratic_interpolation_text_groups,
                fill_opacity=1,
                stroke_width=0,
            )
        )
        self.add(linear_and_quadratic_interpolation_text_background)
        self.play(Create(linear_and_quadratic_interpolation_text_groups))
        self.next_slide()
        # Show the value of the error
        subtraction_text = MathTex(
            r"\left|",
            quadratic_interpolation_value_16_floating_points,
            "-",
            linear_interpolation_value_16_floating_points,
            r"\right|",
        )
        self.play(
            ReplacementTransform(
                linear_and_quadratic_interpolation_text_groups, subtraction_text
            )
        )
        self.next_slide()
        error_value_text = MathTex(
            r"\left|", interpolation_error_16_floating_points, r"\right|"
        )
        self.play(ReplacementTransform(subtraction_text, error_value_text))
        self.next_slide()
        error_value_text_no_borders = MathTex(
            interpolation_error_16_floating_points_absolute
        )
        self.play(ReplacementTransform(error_value_text, error_value_text_no_borders))
        self.next_slide()
        # TODO add background and scale the error number to fill the whole screen.
