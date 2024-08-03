"""interpolation_example_and_runges_phenomenon.py
Shows an example of how interpolation is performed.
Also demonstrates Runges Phenomenon."""

from manim_slides.slide import ThreeDSlide
from manim import (
    BLUE,
    MathTex,
    Create,
    ReplacementTransform,
    UR,
)

from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.general_utilities import clear_screen, addition_string
from helper_functions.graph import SYMBOL_X
from helper_functions.latex_utilities import create_cases
from helper_functions.point_interpolation import (
    interpolate_over,
    interpolation_coefficients_to_function_template,
)
from helper_functions.graph import AxesAndGraphHelper
from helper_functions.premade_slides import create_method_explanatory_slide
from interpolation.shared_constants import (
    set_title_heading_to,
    evaluated_points,
    all_evaluated_points,
    add_witch_of_agnesi_points,
    CORNER_EQUATIONS_SCALE,
)

from interpolation.slide_sources.interpolation_equations import (
    illustrate_interpolation_equations,
    illustrate_solving_interpolation_equation_system,
    create_interpolation_general_method_tex_string,
)


class InterpolationExampleAndRungesPhenomenon(ThreeDSlide):
    def construct(self):
        set_title_heading_to(self, "Interpolation - grundläggande exempel")
        self.axes = AxesAndGraphHelper(
            self, interval=[[0, 7], [0, 5]], use_2d_axes_class=True
        )
        # Scale up axes to make the points appear bigger and clearer to the viewer
        add_witch_of_agnesi_points(self, evaluated_points)
        # Add and create graph to demonstrate how to interpolate
        self.next_slide()
        # Demonstrate the calculation of the polynomial coefficients
        # Bring back polynomial equation
        (
            polynomial_equation_second_degree,
            equation_rectangle_second_degree,
        ) = create_equation_with_border("y=c_1x^2+c_2x+c_3", scale=1)
        self.add(equation_rectangle_second_degree)
        polynomial_equation_second_degree.to_corner(UR)
        self.play(Create(polynomial_equation_second_degree))
        (
            generic_equation_system,
            point_equation_system,
        ) = illustrate_interpolation_equations(
            self, evaluated_points, polynomial_degree=2
        )
        matrix_system_latex = illustrate_solving_interpolation_equation_system(
            self, evaluated_points, 2, generic_equation_system
        )
        # Show solution of equation system
        (
            c_3_interpolation_example,
            c_2_interpolation_example,
            c_1_interpolation_example,
        ) = interpolate_over(evaluated_points)
        c_1_interpolation_example = round(c_1_interpolation_example, 2)
        c_2_interpolation_example = round(c_2_interpolation_example, 2)
        c_3_interpolation_example = round(c_3_interpolation_example, 2)
        self.play(
            ReplacementTransform(
                matrix_system_latex,
                MathTex(
                    create_cases(
                        [
                            f"c_1={c_1_interpolation_example}",
                            f"c_2={c_2_interpolation_example}",
                            f"c_3={c_3_interpolation_example}",
                        ],
                        include_math_environment_start=False,
                    )
                ).scale(1.5),
            )
        )
        clear_screen(self)
        # Add final equation
        final_polynomial_function = f"y={c_1_interpolation_example}x^2{addition_string(c_2_interpolation_example)}x{addition_string(c_3_interpolation_example)}"
        (
            final_polynomial_equation,
            final_polynomial_equation_rectangle,
        ) = create_equation_with_border(final_polynomial_function)
        self.add(final_polynomial_equation, final_polynomial_equation_rectangle)
        self.next_slide()
        # Shrink final polynomial equation
        (
            smaller_final_polynomial_equation,
            smaller_final_polynomial_equation_rectangle,
        ) = create_equation_with_border(
            final_polynomial_function, scale=CORNER_EQUATIONS_SCALE
        )
        smaller_final_polynomial_equation.to_edge(UR)
        final_polynomial_equation_rectangle.become(
            smaller_final_polynomial_equation_rectangle
        )
        self.play(
            ReplacementTransform(
                final_polynomial_equation, smaller_final_polynomial_equation
            )
        )
        # Rerender axes
        self.axes.create_axes([[0, 7], [0, 5]])
        # Generate interpolation polynomial
        interpolation_coefficients = interpolate_over(evaluated_points)
        initial_interpolation_demonstration = self.axes.plot_function(
            graph_function=interpolation_coefficients_to_function_template(
                interpolation_coefficients, SYMBOL_X
            ),
            input_variables=[SYMBOL_X],
            range_to_use_for_function=[0, 7],
        )
        self.next_slide()
        # Add a cheatsheet to how to interpolate
        create_method_explanatory_slide(
            self,
            "Generell polynominterpolation",
            create_interpolation_general_method_tex_string(centering=False),
            title_color=BLUE,
        )
        set_title_heading_to(self, "Runges fenomen")
        # Change axes range to include negative x values as well
        self.axes.create_axes([[-12, 12], [-10, 10]])
        # Add more points
        add_witch_of_agnesi_points(self, all_evaluated_points)
        # Generate interpolation polynomial to demonstrate Runges phenomenon
        interpolation_coefficients = interpolate_over(all_evaluated_points)
        runges_phenomenon_demonstration = self.axes.plot_function(
            graph_function=interpolation_coefficients_to_function_template(
                interpolation_coefficients, SYMBOL_X
            ),
            input_variables=[SYMBOL_X],
            range_to_use_for_function=[-10, 10],
            plot_color=BLUE,
        )
