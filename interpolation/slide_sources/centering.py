"""centering.py
Demonstrates polynomial interpolation with centering.
"""

from manim import (
    ReplacementTransform,
    WHITE,
    MathTex,
    Text,
    DOWN,
    Write,
    GRAY,
    RED,
    SurroundingRectangle,
    Create,
    Arrow3D,
    UR,
    DR,
    Tex,
)
from manim.utils.color.X11 import BROWN
from manim_slides.slide import ThreeDSlide

# Next step is to add centering equation support to the interpolation_equations helper
# See Kompendium i numeriska metoder sida 43.
# OBS!!! Mention sources!
from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.general_utilities import (
    clear_screen,
    format_to_parenthesis_if_negative,
)
from helper_functions.graph import AxesAndGraphHelper, SYMBOL_X
from helper_functions.latex_utilities import create_cases
from helper_functions.point_interpolation import (
    interpolation_coefficients_to_function_template,
    interpolate_over,
)
from helper_functions.premade_slides import create_method_explanatory_slide
from interpolation.shared_constants import (
    create_logger,
    set_title_heading_to,
    CORNER_EQUATIONS_SCALE,
)

from helper_functions.text_scales import DISCLAIMER_TEXT_SCALE

from interpolation.slide_sources.interpolation_equations import (
    illustrate_interpolation_equations,
    illustrate_solving_interpolation_equation_system,
    generate_interpolation_polynomial_equation,
    create_interpolation_general_method_tex_string,
)


class CenteringExampleSlide(ThreeDSlide):
    # Add a set of points that will be used to
    # illustrate the concept of centering
    CENTERING_POINTS = [[1568, 20], [1570, 24], [1572, 22]]
    CENTERING_POINTS_X = [x_value for x_value, _ in CENTERING_POINTS]
    CENTERING_POINTS_Y = [y_value for _, y_value in CENTERING_POINTS]
    CENTERING_POINTS_X_INTERVAL = [min(CENTERING_POINTS_X), max(CENTERING_POINTS_X)]
    CENTERING_POINTS_Y_INTERVAL = [min(CENTERING_POINTS_Y), max(CENTERING_POINTS_Y)]
    # Point that is centered around
    CENTERED_POINT = CENTERING_POINTS[1][0]

    def construct(self):
        create_logger(self)
        set_title_heading_to(self, "Centrering")
        self.next_slide()
        axes_interval = [
            [
                self.CENTERING_POINTS_X_INTERVAL[0] - 5,
                self.CENTERING_POINTS_X_INTERVAL[1] + 5,
            ],
            [
                self.CENTERING_POINTS_Y_INTERVAL[0] - 5,
                self.CENTERING_POINTS_Y_INTERVAL[1] + 5,
            ],
        ]
        self.axes = AxesAndGraphHelper(
            self, interval=axes_interval, use_2d_axes_class=True
        )
        # Plot points
        for point in self.CENTERING_POINTS:
            self.axes.add_point(
                point,
                show_coordinates=True,
                show_z_coordinate=False,
                dot_color=GRAY,
                round_coordinates_to_decimals=2,
            )
        self.next_slide()
        # Indicate centered point. Start at the bottom of the screen
        centered_point_indication_arrow_start_y = axes_interval[1][0] + 2
        centered_point_indication_arrow = Arrow3D(
            start=self.axes.axes_object.coords_to_point(
                self.CENTERED_POINT, centered_point_indication_arrow_start_y, 0
            ),
            end=self.axes.axes_object.coords_to_point(
                self.CENTERED_POINT, centered_point_indication_arrow_start_y - 2, 0
            ),
            color=RED,
        )
        self.play(Create(centered_point_indication_arrow))
        # Add a rectangle around the middle point.
        middle_point_mobject = self.axes.axes_object.x_axis.get_number_mobject(
            self.CENTERED_POINT
        )
        centered_point_indication_rectangle = SurroundingRectangle(
            middle_point_mobject, color=RED
        )
        self.play(Create(centered_point_indication_rectangle))
        self.next_slide()
        # Solve interpolation coefficients
        interpolation_coefficients = interpolate_over(
            self.CENTERING_POINTS, center_around_point=self.CENTERED_POINT
        )
        # Show the same illustration used in interpolation_example_and_runges_phenomenon
        generic_equation_system, _ = illustrate_interpolation_equations(
            self,
            self.CENTERING_POINTS,
            2,
            center_around_point=self.CENTERED_POINT,
            arrow_length=1,
            generic_equation_system_positioning_function=lambda mobject, _: mobject.to_corner(
                DR
            ),
        )
        self.next_slide()
        clear_screen(self)
        # Scale up equation system and calculate the differences
        generic_equation_system.move_to([0, 0, 0])
        generic_equation_system.set_color(WHITE)
        self.add(generic_equation_system)
        self.wait(0.5)  # Needed for slide to render
        self.next_slide()
        # Show a second equation system with the differences now calculated
        all_centering_equations = []
        for point_x, point_y in self.CENTERING_POINTS:
            all_centering_equations.append(
                generate_interpolation_polynomial_equation(
                    point_x,
                    point_y,
                    round_points_to_decimals=2,
                    polynomial_degree=2,
                    center_around_point=self.CENTERED_POINT,
                    calculate_centering_value=True,
                )
            )
        generic_equation_system_with_differences = MathTex(
            create_cases(all_centering_equations, include_math_environment_start=False)
        )
        self.play(
            ReplacementTransform(
                generic_equation_system, generic_equation_system_with_differences
            )
        )
        self.next_slide()
        # Illustrate solving the equations
        matrix_system_latex = illustrate_solving_interpolation_equation_system(
            self,
            self.CENTERING_POINTS,
            2,
            generic_equation_system_with_differences,
            center_around_point=self.CENTERED_POINT,
            calculate_centering_value=True,
        )
        coefficients_solutions_equation_system = create_cases(
            [
                f"c_1={round(interpolation_coefficients[0], 2)}",
                f"c_2={round(interpolation_coefficients[1], 2)}",
                f"c_3={round(interpolation_coefficients[2], 2)}",
            ],
            include_math_environment_start=False,
        )
        coefficients_solutions_equation_system = MathTex(
            coefficients_solutions_equation_system
        )
        solution_disclaimer = Text(
            "*värden på koefficienter har avrundats till 2 decimaler"
        )
        solution_disclaimer.scale(DISCLAIMER_TEXT_SCALE)
        solution_disclaimer.next_to(coefficients_solutions_equation_system, DOWN)
        self.play(
            ReplacementTransform(
                matrix_system_latex, coefficients_solutions_equation_system
            )
        )
        self.play(Write(solution_disclaimer))
        self.next_slide()
        clear_screen(self)
        self.axes.create_axes(interval=axes_interval)
        # Plot the polynomial
        result_demonstration = self.axes.plot_function(
            graph_function=interpolation_coefficients_to_function_template(
                interpolation_coefficients,
                SYMBOL_X,
                center_around_point=self.CENTERED_POINT,
            ),
            input_variables=[SYMBOL_X],
            range_to_use_for_function=self.axes.axes_object.x_range,
        )
        # Format the equation of the resulting polynomial
        resulting_polynomial_equation_string = "y="
        interpolation_coefficients_rounded = [
            round(interpolation_coefficient, 2)
            for interpolation_coefficient in interpolation_coefficients
        ]
        # The polynomial equation will contain powers of x. For a second degree polynomial, we have
        # three coefficients and the powers 2, 1, and 0.
        # We know we'll be dealing with a second degree polynomial, so we can just add it right here
        x_powers = [2, 1, 0]
        for i in range(len(interpolation_coefficients_rounded) - 1):
            rounded_coefficient = interpolation_coefficients_rounded[i]
            resulting_polynomial_equation_string += r"%r(x-%s)^{%r}+" % (
                rounded_coefficient,
                format_to_parenthesis_if_negative(self.CENTERED_POINT),
                x_powers[i],
            )
        # Remove last +1-string
        resulting_polynomial_equation_string = resulting_polynomial_equation_string[:-1]
        resulting_polynomial_equation_string += repr(
            interpolation_coefficients_rounded[-1]
        )
        (
            resulting_polynomial_equation,
            resulting_polynomial_equation_border,
        ) = create_equation_with_border(
            resulting_polynomial_equation_string, scale=CORNER_EQUATIONS_SCALE
        )
        resulting_polynomial_equation.to_corner(UR)
        self.add(resulting_polynomial_equation_border)
        self.play(Create(resulting_polynomial_equation))
        self.wait(0.5)
        self.next_slide()
        # Add a cheatsheet related to centering
        create_method_explanatory_slide(
            self,
            "Centrering",
            create_interpolation_general_method_tex_string(centering=True),
            title_color=BROWN,
            extra_mobjects=[
                Tex(
                    r"""(\underline{understrykningar} markerar skillnader i beräkningar mellan centrering och ``vanlig`` generell polynominterpolation)."""
                ).scale(DISCLAIMER_TEXT_SCALE)
            ],
        )
