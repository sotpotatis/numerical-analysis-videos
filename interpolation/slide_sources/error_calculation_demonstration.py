"""error_calculation_demonstration.py
Renders a slide used to show how to calculate errors.
Because we need to use a zoomed slide, we need to define the error calculation
slide(s) separately from the others."""

from manim_slides.slide import Slide

from helper_functions.premade_slides import create_bullet_list_and_title_frame
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
    ScaleInPlace,
    UR,
    BLUE,
    SurroundingRectangle,
    BLACK,
    Write,
)

from helper_functions.general_utilities import (
    play_multiple,
    clear_screen,
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
    set_title_heading_to,
)
from sympy import lambdify


class ErrorCalculationDemonstrationSlide(Slide, MovingCameraScene):
    def construct(self):
        create_logger(self)
        set_title_heading_to(self, "Felskattning")
        self.initial_camera_width = X_AXIS_LENGTH * 1.5
        self.initial_camera_height = Y_AXIS_LENGTH * 1.5
        self.camera.frame.set(
            width=self.initial_camera_width, height=self.initial_camera_height
        )
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
        error_comparison_line = self.axes.plot_line(
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
        self.next_slide()
        # Add question text
        question_text = Tex(
            r'"\textbf{Hur kan vi veta hur stort fel vi har vid }$x=%d$\textbf{ om vi använder oss av förstagradspolynomet? (}$p_1(%d)$\textbf{)}"'
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
        # A little hacky to hardcode the zoom factor, but could not get it to work with a dynamic
        # zoom.
        ERROR_SIZE_LINE_ZOOM_FACTOR = 1 / 40
        ERROR_SIZE_LINE_ZOOM_FACTOR_SLIGHTLY_ZOOMED_OUT = (
            ERROR_SIZE_LINE_ZOOM_FACTOR + 1 / 10
        )
        # Add a line indicating the size of the error. Add a brace and a text showing what we're currently calculating
        linear_interpolation_value_is_smallest = (
            linear_interpolation_value < quadratic_interpolation_value
        )
        error_size_line_starting_point = (
            linear_interpolation_dot
            if linear_interpolation_value_is_smallest
            else quadratic_interpolation_dot
        )
        error_size_line_endpoint = (
            quadratic_interpolation_dot
            if linear_interpolation_value_is_smallest
            else linear_interpolation_dot
        )
        self.logger.info(
            f"Drawing error displaying line from point {error_size_line_starting_point} to {error_size_line_endpoint}"
        )
        error_size_line = Line(
            start=error_size_line_starting_point.get_center(),
            end=error_size_line_endpoint.get_center(),
            color=ORANGE,
        )
        error_size_brace = Brace(error_size_line, color=ORANGE, direction=RIGHT)
        error_text = Tex('"Felet"', color=ORANGE)
        error_text.scale(2 * ERROR_SIZE_LINE_ZOOM_FACTOR_SLIGHTLY_ZOOMED_OUT)
        error_text.next_to(
            error_size_brace,
            RIGHT,
            buff=ERROR_SIZE_LINE_ZOOM_FACTOR_SLIGHTLY_ZOOMED_OUT,
        )
        self.play(Create(error_size_line))
        # Previous dynamic code. This was removed because I could not make it work.
        # Since the current code depends on manually setting the zoom level, I saved this
        # because dynamic stuff is nice :cool:
        """# Zoom to the two dots
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
        )"""
        self.play(self.camera.frame.animate.move_to(error_size_line))
        # Zoom in.
        self.zoom_camera_to_scale(ERROR_SIZE_LINE_ZOOM_FACTOR)
        self.wait(1)
        self.next_slide()
        # Zoom out - a little - to highlight the error
        self.zoom_camera_to_scale(ERROR_SIZE_LINE_ZOOM_FACTOR_SLIGHTLY_ZOOMED_OUT)
        self.play(Create(error_size_brace))
        self.add(error_text)
        self.wait(0.1)  # To ensure the slide is detected
        self.next_slide()
        # Zoom out - fully
        self.zoom_camera_to_scale(1)
        error_value_text_scale = 1.5
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
        ).scale(error_value_text_scale)
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
        ).scale(error_value_text_scale)
        subtraction_text.set_color_by_tex(
            quadratic_interpolation_value_16_floating_points, RED
        )
        subtraction_text.set_color_by_tex(
            linear_interpolation_value_16_floating_points, YELLOW
        )
        self.play(
            ReplacementTransform(
                linear_and_quadratic_interpolation_text_groups, subtraction_text
            )
        )
        self.next_slide()
        error_value_text = MathTex(
            r"\left|", interpolation_error_16_floating_points, r"\right|", color=ORANGE
        ).scale(error_value_text_scale)
        self.play(ReplacementTransform(subtraction_text, error_value_text))
        self.next_slide()
        error_value_text_no_borders = MathTex(
            interpolation_error_16_floating_points_absolute, color=ORANGE
        ).scale(error_value_text_scale)
        self.play(ReplacementTransform(error_value_text, error_value_text_no_borders))
        self.next_slide()
        mobjects_before_error_highlight = self.mobjects.copy()
        mobjects_before_error_highlight.remove(error_value_text_no_borders)
        mobjects_before_error_highlight.remove(
            linear_and_quadratic_interpolation_text_background
        )
        # Highlight error.
        clear_screen(self, [error_value_text_no_borders])
        error_value_text_no_borders.move_to([0, 0, 0])
        self.play(ScaleInPlace(error_value_text_no_borders, 3))
        self.next_slide()
        clear_screen(self)
        # Add instructions how to interpolate
        create_bullet_list_and_title_frame(
            self,
            "Felskattning, interpolation",
            [
                "Konstruera ett interpolationspolynom anpassat till $n$ antal punkter.",
                "För att skatta felet i punkten $x$, räkna ut polynomets (från steg 1) värde i denna punkt. Kalla detta värde för $p_1(x)$.",
                "Konstruera ett till interpolationspolynom av en grad högre än steg 1. Detta polynom kommer då behöva baseras på en extra datapunkt jämfört med det i steg 1: $n+1$ datapunkter.",
                "För att skatta felet i punkten $x$, räkna även ut polynomets (från steg 3) värde i denna punkt. Kalla detta värde för $p_2(x)$.",
                "Nu ges en uppskattning av felet i punkten x av $|p_1(x)-p_2(x)|$",
            ],
            show_numbers_instead_of_bullets=True,
            fade_in=True,
        )
        self.wait(0.5)  # Otherwise screen will not show
        self.next_slide()
        clear_screen(self)
        # Restore previous Mobjects
        for previous_mobjects in mobjects_before_error_highlight:
            self.add(previous_mobjects)
        # Add error formulas again, in a different format
        error_formulas_text_size = 0.75
        error_formulas_group = VGroup(
            Tex(r"Absolut fel i y-värde, i punkten $x$ (uppskattning)").scale(
                error_formulas_text_size
            ),
            MathTex(r"\left|p_1(x)-p_2(x)\right|"),
            Tex(r"Relativt fel i y-värde, i punkten $x$ (uppskattning)").scale(
                error_formulas_text_size
            ),
            MathTex(r"\frac{\text{Absolut fel}}{\left|p_2(x)\right|}"),
        )
        error_formulas_group.arrange_in_grid(rows=2, cols=2)
        error_formulas_group.to_corner(UR, buff=0)
        error_formulas_border = SurroundingRectangle(
            error_formulas_group,
            color=BLUE,
            fill_color=BLACK,
            fill_opacity=1,
            corner_radius=0.2,
        )
        error_formulas_and_border = VGroup(error_formulas_border, error_formulas_group)
        self.play(Create(error_formulas_and_border))
        self.wait(0.5)  # Needed for equations to finish rendering
        self.next_slide()
        # Highlight error equations full screen. Move them to the center of the scene
        clear_screen(self, [error_formulas_and_border])
        error_formulas_and_border.move_to([0, 0, 0])
        self.play(ScaleInPlace(error_formulas_and_border, 2))
        # Explain the notation used
        notation_explaining = Tex(
            """där $p_1$ är ett polynom av gradtal $n$, $p_2$ är ett polynom av gradtal $n+1$, 
        och $x$ är en punkt du vill veta felet i"""
        )
        notation_explaining.scale(0.75)
        notation_explaining.next_to(error_formulas_and_border, DOWN)
        self.play(Write(notation_explaining))

    def zoom_camera_to_scale(self, zoom_scale: float) -> None:
        """Zooms the camera to a set zoom scale."""
        self.play(
            self.camera.frame.animate.set(
                width=self.initial_camera_width * zoom_scale,
                height=self.initial_camera_height * zoom_scale,
            ),
            run_time=2,
        )
