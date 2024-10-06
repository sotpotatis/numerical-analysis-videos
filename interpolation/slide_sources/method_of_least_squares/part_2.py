"""method_of_least_squares/part_2.py
Briefly explains the method of least squares for interpolation.
Part one includes graphically introducing the method of least squares."""

from manim import (
    MathTex,
    VGroup,
    Create,
    ReplacementTransform,
    GrowFromCenter,
    WHITE,
    Text,
    DOWN,
    UR,
    FadeIn,
    UL,
    Write,
    SurroundingRectangle,
    GREEN,
    ORANGE,
)
from manim_slides.slide import ThreeDSlide
from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.general_utilities import clear_screen, play_multiple
from helper_functions.graph import SYMBOL_X, AxesAndGraphHelper
from helper_functions.latex_utilities import (
    create_matrix,
    create_cases,
    TEX_TEMPLATE_FIX_MAX_MATRIX_SIZE,
)
from helper_functions.loading.loading import LoadingSpinner
from helper_functions.matrix_utilities import transpose_matrix
from helper_functions.point_interpolation import (
    interpolation_coefficients_to_function_template,
)
from helper_functions.premade_slides import create_method_explanatory_slide
from interpolation.shared_constants import (
    sorted_all_evaluated_points,
    CORNER_EQUATIONS_SCALE,
    add_witch_of_agnesi_points,
    create_logger,
    set_title_heading_to,
)
from helper_functions.text_scales import DISCLAIMER_TEXT_SCALE
from interpolation.slide_sources.interpolation_equations import (
    illustrate_interpolation_equations,
    create_interpolation_matrix,
)
from interpolation.slide_sources.method_of_least_squares.shared_constants import (
    c1_real,
    c2_real,
    c3_real,
    coefficient_matrix_least_squares,
    value_matrix_least_squares,
)


class MethodOfLeastSquaresPartTwo(ThreeDSlide):
    def construct(self):
        create_logger(self)
        set_title_heading_to(self, "Minsta kvadratmetoden - räkneexempel")
        self.axes = AxesAndGraphHelper(
            self, interval=[[-10, 10], [0, 5]], use_2d_axes_class=True
        )
        # Add points used in part 1
        add_witch_of_agnesi_points(
            self, sorted_all_evaluated_points, animation_run_time=0
        )
        # Show how to fit the polynomial
        (
            generic_equation_system,
            point_equation_system,
        ) = illustrate_interpolation_equations(
            self,
            sorted_all_evaluated_points,
            2,
            generic_equation_system_positioning_function=self.interpolation_illustration_positioning_function,
            play_replacement_animation=False,
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
            sorted_all_evaluated_points, 2
        )
        a_matrix_values, x_matrix_values, b_matrix_values = matrix_equation_strings
        self.play(ReplacementTransform(generic_equation_system, matrix_equation_system))
        self.next_slide()
        a_matrix_string = create_matrix(a_matrix_values)
        x_matrix_original_string = create_matrix(x_matrix_values)
        b_matrix_string = create_matrix(b_matrix_values)
        # Highlight the names of the matricies
        a_matrix_string = r"\underbrace{%s}_{\vec A}" % (a_matrix_string)
        x_matrix_string = r"\underbrace{%s}_{\vec x}" % (x_matrix_original_string)
        b_matrix_string = r"\underbrace{%s}_{\vec b}" % (b_matrix_string)
        matrix_equation_system_with_highlighted_names = MathTex(
            a_matrix_string,
            x_matrix_string + "=",
            b_matrix_string,
            tex_template=TEX_TEMPLATE_FIX_MAX_MATRIX_SIZE,
        )
        self.remove(matrix_equation_system)
        self.play(FadeIn(matrix_equation_system_with_highlighted_names))
        self.next_slide()
        # Highlight how the system can be written
        general_matrix_equation_text = r"\vec A\vec x =  \vec b"
        (
            general_matrix_equation,
            general_matrix_equation_border,
        ) = create_equation_with_border(general_matrix_equation_text)
        general_matrix_equation_group = VGroup(
            general_matrix_equation_border, general_matrix_equation
        )
        general_matrix_equation_group.next_to(
            matrix_equation_system_with_highlighted_names, DOWN
        )
        self.add(general_matrix_equation_group)
        self.wait(0.5)
        self.next_slide()
        self.remove(general_matrix_equation_group)
        # Now, indicate that we multiply the left side with A transpose
        matrix_equation_system_with_transpose_indication = MathTex(
            r"\Huge{A^T}\normalsize",
            a_matrix_string,
            x_matrix_string,
            r"= \Huge{A^T}\normalsize",
            b_matrix_string,
            tex_template=TEX_TEMPLATE_FIX_MAX_MATRIX_SIZE,
        )
        self.remove(matrix_equation_system_with_highlighted_names)
        self.add(matrix_equation_system_with_transpose_indication)
        self.wait(0.5)
        self.next_slide()
        # Now, write out the values of A transpose
        a_matrix_transpose = transpose_matrix(a_matrix_values)
        a_matrix_transpose_string = create_matrix(a_matrix_transpose)
        a_matrix_transpose_string = r"\underbrace{%s}_{\vec A^T}" % (
            a_matrix_transpose_string
        )
        # Divide matrix equation system in 2 parts to make it display without being tiny tiny
        general_matrix_equation, _ = create_equation_with_border(
            [r"\vec A^T \vec A\vec x", r" =  \vec A^T \vec b"], scale=1
        )  # This will be used to indicate that we don't show the whole equation system in the code below.
        general_matrix_equation.to_corner(UL)
        matrix_equation_highlighting_border = SurroundingRectangle(
            general_matrix_equation[0], color=GREEN
        )
        matrix_equation_system_with_transpose_values_part_1 = MathTex(
            a_matrix_transpose_string,
            a_matrix_string,
            x_matrix_string,
            tex_template=TEX_TEMPLATE_FIX_MAX_MATRIX_SIZE,
        )
        matrix_equation_system_with_transpose_values_part_2 = MathTex(
            f"= {a_matrix_transpose_string}",
            b_matrix_string,
            tex_template=TEX_TEMPLATE_FIX_MAX_MATRIX_SIZE,
        )
        self.add(general_matrix_equation)
        self.add(matrix_equation_highlighting_border)
        self.play(
            ReplacementTransform(
                matrix_equation_system_with_transpose_indication,
                matrix_equation_system_with_transpose_values_part_1,
            )
        )
        self.next_slide()
        # Show the second part of the equations
        # Highlight that we have moved to the second part of the equation§
        new_matrix_equation_highlighting_border = SurroundingRectangle(
            general_matrix_equation[1], color=GREEN
        )
        self.remove(matrix_equation_system_with_transpose_values_part_1)
        self.play(
            ReplacementTransform(
                matrix_equation_highlighting_border,
                new_matrix_equation_highlighting_border,
            )
        )
        self.play(FadeIn(matrix_equation_system_with_transpose_values_part_2))
        self.next_slide()
        for object in [
            general_matrix_equation,
            new_matrix_equation_highlighting_border,
        ]:
            self.remove(object)
        # Show what the matrix multiplication results are
        ata_matrix_string = create_matrix(
            coefficient_matrix_least_squares, round_to_decimals=2
        )
        atb_matrix_string = create_matrix(
            value_matrix_least_squares, round_to_decimals=2
        )
        matrix_multiplication_result = MathTex(
            ata_matrix_string, x_matrix_original_string, f"={atb_matrix_string}"
        )
        self.remove(matrix_equation_system_with_transpose_values_part_2)
        self.play(FadeIn(matrix_multiplication_result))
        self.next_slide()
        # Play animation of solving the system
        loading_spinner = LoadingSpinner(
            self, before_addition_function=lambda object: object.move_to([0, 0, 0])
        )
        loading_spinner.spin(duration=3)
        self.remove(*loading_spinner.created_objects)
        solution_equation_system = MathTex(
            create_cases(
                [
                    f"c_1={round(c1_real, 2)}",
                    f"c_2={round(c2_real, 2)}",
                    f"c_3={round(c3_real, 2)}",
                ],
                include_math_environment_start=False,
            )
        )
        self.play(
            ReplacementTransform(matrix_multiplication_result, solution_equation_system)
        )
        # Add disclaimer about rounding
        disclaimer_text = Text(
            "*värden på koefficienter har avrundats till två decimaler."
        )
        disclaimer_text.scale(DISCLAIMER_TEXT_SCALE)
        disclaimer_text.next_to(solution_equation_system, DOWN)
        self.play(Write(disclaimer_text), run_time=0.5)
        self.next_slide()
        clear_screen(self)
        self.next_slide()
        # Plot the resulting interpolating polynomial
        self.axes.create_axes([[-10, 10], [0, 5]])
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
        (
            interpolation_polynomial_equation,
            interpolation_polynomial_equation_border,
        ) = create_equation_with_border(
            "y={}x^2+{}x+{}".format(*rounded_coefficients),
            scale=CORNER_EQUATIONS_SCALE,
        )
        interpolation_polynomial_equation.to_corner(UR)
        self.add(interpolation_polynomial_equation_border)
        self.play(Create(interpolation_polynomial_equation))
        self.next_slide()
        # Show the general equation for least squares
        clear_screen(self)
        general_matrix_equation_scale = 2
        general_matrix_equation.scale(general_matrix_equation_scale)
        general_matrix_equation.move_to([0, 0, 0])
        self.play(GrowFromCenter(general_matrix_equation_group))
        self.next_slide()
        # Create heading and explanation about how the method of least squares works. But it will not be added yet!
        # They are created here for positioning purposes.
        heading, least_squares_explanation = create_method_explanatory_slide(
            self,
            "Minsta kvadratmetoden",
            r"Konstruera ett system av ekvationer för att interpolera över önskat antal punkter. (se tidigare i videon) "
            + r"Skriv om systemet på matrisform, där $\vec A$ är koefficientmatris och $\vec b$ är högerledsmatris."
            + r" Låt $\vec x$ representera de sökta koefficienterna för interpolationspolynomet du vill skapa."
            r" Ekvationssystemet som ska lösas ges då av:",
            title_color=ORANGE,
            play=False,
        )
        # Fade the general matrix equation into general least squares equation
        (
            general_least_squares_equation,
            general_least_squares_border,
        ) = create_equation_with_border(
            r"\vec A^T\vec A\vec x =  \vec A^T \vec b",
            scale=general_matrix_equation_scale,
        )
        general_least_squares_equation_group = VGroup(
            general_least_squares_border, general_least_squares_equation
        )
        general_least_squares_equation_group.next_to(least_squares_explanation, DOWN)
        self.play(
            ReplacementTransform(
                general_matrix_equation_group, general_least_squares_equation_group
            )
        )
        self.next_slide()
        # Define the method of least squares
        play_multiple(self, [heading, least_squares_explanation], Create)
        self.wait(1)  # Needed to make sure the slide is displayed completely
        self.next_slide()

    def interpolation_illustration_positioning_function(
        self, current_generic_equation_system: MathTex, current_iteration: int
    ) -> None:
        """Custom positioning function for the interpolation illustration. See interpolation_equations.py's docstring of
        illustrate_interpolation_equations for more information."""
        # Position the equation system differently depending on what part of the screen that is currently being illustrated
        current_point_x, _ = sorted_all_evaluated_points[current_iteration]
        self.logger.debug(
            f"interpolation_illustration_positioning_function called with point x {current_point_x}, iteration {current_iteration}."
        )
        if current_point_x < 0:
            self.logger.debug("Positioning equation system on the right side.")
            current_generic_equation_system.to_corner(UR)
        else:
            self.logger.debug("Positioning equation system on the left side.")
            current_generic_equation_system.to_corner(UL)
