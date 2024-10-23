"""introduction.py
Introduces the viewer to what an interpolation polynomial is and what it looks like."""

import logging
from typing import List

from manim_slides.slide import ThreeDSlide
from manim import (
    Create,
    ReplacementTransform,
    ValueTracker,
    DOWN,
    GREEN,
    RED,
    VGroup,
    UR,
    MathTex,
    Tex,
    BLUE,
    Write,
    UP,
    MED_SMALL_BUFF,
)

from helper_functions.equation_displaying import create_equation_with_border
from helper_functions.general_utilities import clear_screen, play_multiple
from helper_functions.graph import SYMBOL_X
from helper_functions.premade_slides import create_title_frame
from helper_functions.graph import AxesAndGraphHelper
from helper_functions.knob.knob import Knob
from helper_functions.text_scales import TOP_HEADING_SCALE
from interpolation.shared_constants import (
    INTERPOLATION_DEFAULT_AXES_INTERVAL,
    CORNER_EQUATIONS_SCALE,
    generate_generic_polynomial_equation,
)
from interpolation.value_tracker_plotting import (
    generate_updater_for_equation_related_to_constant_values,
    generate_updater_for_plot_graph_according_to_constant_values,
)


class IntroductionSlide(ThreeDSlide):
    """Contains code for the main interpolation video"""

    def construct(self):
        self.logger = logging.getLogger(__name__)
        # Title slide
        title_frame = create_title_frame(self, "Polynominterpolation")
        self.remove(title_frame)
        self.next_slide()
        # Illustrate generic equation for 1st deg polynomial
        # Show generic equation for 1st deg polynomial
        generic_polynomial_equation, equation_rectangle = create_equation_with_border(
            "y=kx+m"
        )
        self.add(equation_rectangle)
        self.play(Create(generic_polynomial_equation))
        self.wait(0.5)
        self.next_slide()
        # Highlight the notation that I will be using
        generic_polynomial_equation_group = VGroup(
            generic_polynomial_equation, equation_rectangle
        )
        (
            generic_polynomial_equation_alternate_notation,
            new_equation_rectangle,
        ) = create_equation_with_border("y=c_1x+c_2")
        generic_polynomial_equation_alternate_notation_group = VGroup(
            new_equation_rectangle, generic_polynomial_equation_alternate_notation
        )
        self.play(
            ReplacementTransform(
                generic_polynomial_equation_group,
                generic_polynomial_equation_alternate_notation_group,
            )
        )
        self.next_slide()
        # Illustrate parameters for 1st deg polynomial
        c1 = ValueTracker(1)
        c2 = ValueTracker(0)
        coefficient_value_trackers = [c2, c1]
        # Scale down generic equations and move them to the top right
        first_degree_equation_value_updater = (
            generate_updater_for_equation_related_to_constant_values(
                self, coefficient_value_trackers
            )
        )
        smaller_generic_polynomial_equation_alternate_notation_group = (
            first_degree_equation_value_updater(return_generic_equation=True)
        )
        self.play(
            ReplacementTransform(
                generic_polynomial_equation_alternate_notation_group,
                smaller_generic_polynomial_equation_alternate_notation_group,
            )
        )
        # Add graph
        self.axes = AxesAndGraphHelper(
            self, interval=INTERPOLATION_DEFAULT_AXES_INTERVAL
        )
        # Add constant knobs for showing how the graph reacts to tuning the coefficients

        c1_knob = Knob(
            self,
            c1,
            min_value=1 / 4,
            max_value=2,
            knobject_updater_function=lambda object: object.next_to(
                smaller_generic_polynomial_equation_alternate_notation_group, DOWN
            ),
            knob_label="c_1",
        )
        c2_knob = Knob(
            self,
            c2,
            min_value=-3,
            max_value=3,
            knobject_updater_function=lambda object: object.next_to(
                c1_knob.value_text, DOWN
            ),
            knob_label="c_2",
        )
        self.add(*c1_knob.created_objects)
        self.add(*c2_knob.created_objects)
        coefficient_knobs = [c2_knob, c1_knob]
        # Add updater that shows how constants change what the graph looks like
        first_degree_polynomial_value_updater = (
            generate_updater_for_plot_graph_according_to_constant_values(
                self, coefficient_value_trackers, SYMBOL_X, GREEN
            )
        )
        coefficient_knobbing_polynomial_plot = first_degree_polynomial_value_updater(
            return_new_plot=True
        )
        coefficient_knobbing_polynomial_plot.add_updater(
            first_degree_polynomial_value_updater
        )
        smaller_generic_polynomial_equation_alternate_notation_group.add_updater(
            first_degree_equation_value_updater
        )
        self.add(coefficient_knobbing_polynomial_plot)
        self.wait(0.5)
        self.next_slide()
        # Show how the coefficients control the plot
        self.animate_coefficient_value_trackers(
            coefficient_value_trackers, coefficient_knobs
        )
        # Illustrate parameters for a 2nd degree polynomial
        self.next_slide()
        self.remove(coefficient_knobbing_polynomial_plot)
        c3 = ValueTracker(0)
        coefficient_value_trackers.insert(0, c3)
        second_degree_equation_value_updater = (
            generate_updater_for_equation_related_to_constant_values(
                self, coefficient_value_trackers
            )
        )
        second_degree_equation_group = second_degree_equation_value_updater(
            return_generic_equation=True
        )
        self.remove(smaller_generic_polynomial_equation_alternate_notation_group)
        # Show the generic second degree polynomial
        (
            generic_second_degree_polynomial_equation,
            generic_second_degree_polynomial_equation_border,
        ) = create_equation_with_border("y=c_1x^2+c_2x+c_3x")
        generic_second_degree_polynomial_equation.move_to([0, 0, 0])
        generic_second_degree_polynomial_equation_group = VGroup(
            generic_second_degree_polynomial_equation_border,
            generic_second_degree_polynomial_equation,
        )
        self.play(Create(generic_second_degree_polynomial_equation_group))
        self.next_slide()
        generic_second_degree_polynomial_equation_group.scale(CORNER_EQUATIONS_SCALE)
        generic_second_degree_polynomial_equation_group.to_corner(UR)
        self.play(
            ReplacementTransform(
                generic_second_degree_polynomial_equation_group,
                second_degree_equation_group,
            )
        )
        # Add knobs for 2nd degree polynomial. Adjust old knobs to fit new visualization
        c1_knob.min_value = -10
        c1_knob.max_value = 6
        c2_knob.default_value = 1
        c2_knob.min_value = -4
        c2_knob.max_value = 4
        c1.set_value(c1_knob.default_value)
        c2.set_value(c2_knob.default_value)
        c3_knob = Knob(
            self,
            c3,
            min_value=-2,
            max_value=2,
            knobject_updater_function=lambda object: object.next_to(
                c2_knob.value_text, DOWN
            ),
            knob_label="c_3",
        )
        coefficient_knobs.insert(0, c3_knob)
        self.add(*c3_knob.created_objects)
        self.wait(0.5)  # Needed for animations to play
        self.next_slide()
        # Create plots for second degree polynomial
        second_degree_polynomial_value_updater = (
            generate_updater_for_plot_graph_according_to_constant_values(
                self, coefficient_value_trackers, SYMBOL_X, RED
            )
        )
        new_coefficient_knobbing_polynomial_plot = (
            second_degree_polynomial_value_updater(return_new_plot=True)
        )
        new_coefficient_knobbing_polynomial_plot.add_updater(
            second_degree_polynomial_value_updater
        )
        second_degree_equation_group.add_updater(second_degree_equation_value_updater)
        self.add(new_coefficient_knobbing_polynomial_plot)
        self.wait(0.5)
        self.next_slide()
        self.animate_coefficient_value_trackers(
            coefficient_value_trackers, coefficient_knobs
        )
        self.next_slide()
        # The first time around, we want to simply reveal the equations.
        # The other time, we want an emphasis on the implicit x^0 and x^1.
        for slide_index in range(2):
            clear_screen(self)
            # Provide a list of generic polynomial equations
            polynomial_names = [
                "Förstagradspolynom",
                "Andragradspolynom",
                "Tredjegradspolynom",
            ]
            # Add a title
            heading = Tex("Generella polynomekvationer", color=BLUE)
            heading.scale(TOP_HEADING_SCALE)
            heading.to_edge(UP)
            self.play(Create(heading))
            # Add rows showing the polynomial equation and its name
            last_mobject = (
                heading  # Used for positioning polynomial names below each other
            )
            for i in range(len(polynomial_names)):
                polynomial_equation = generate_generic_polynomial_equation(
                    degree=i + 1, show_implicit_powers=slide_index == 1
                )
                polynomial_name = polynomial_names[i]
                (
                    polynomial_equation_object,
                    polynomial_equation_border,
                ) = create_equation_with_border(polynomial_equation, scale=2)
                polynomial_equation_group = VGroup(
                    polynomial_equation_border, polynomial_equation_object
                )
                polynomial_name_object = Tex(polynomial_name)
                polynomial_name_object.scale(1.5)
                polynomial_formula_objects = VGroup(
                    polynomial_equation_group, polynomial_name_object
                )
                polynomial_formula_objects.arrange_in_grid(rows=1, cols=2)
                polynomial_formula_objects.next_to(
                    last_mobject, DOWN, buff=MED_SMALL_BUFF
                )
                last_mobject = polynomial_formula_objects
                self.play(Create(polynomial_formula_objects))
                self.wait(0.5)
                if slide_index == 0:
                    self.next_slide()
            coefficients_explaination_tex = (
                r"Där $c_1, c_2,$ osv. är godtyckliga reella konstanter"
            )
            coefficients_explaination = Tex(coefficients_explaination_tex)
            coefficients_explaination.next_to(last_mobject, DOWN)
            self.play(Write(coefficients_explaination))
            self.next_slide()
        # Add vertical dots and generic formula
        vertical_dots = MathTex(r"\vdots")
        vertical_dots.scale(2)
        vertical_dots.next_to(last_mobject, DOWN)
        general_polynomial_equation_heading = Tex("Generell polynomekvation")
        general_polynomial_equation_heading.scale(1.5)
        general_polynomial_equation_heading.next_to(vertical_dots, DOWN)
        (
            general_polynomial_equation,
            generic_polynomial_equation_border,
        ) = create_equation_with_border(
            r"y=c_1x^n+c_2x^{(n-1)}+c_3x^{(n-2)}+...+c_{(n+1)}", scale=2
        )
        general_polynomial_equation_group = VGroup(
            generic_polynomial_equation_border, general_polynomial_equation
        )
        general_polynomial_equation_group.next_to(
            general_polynomial_equation_heading, DOWN
        )
        self.remove(coefficients_explaination)
        play_multiple(
            self,
            [
                vertical_dots,
                general_polynomial_equation_heading,
                general_polynomial_equation_group,
            ],
            Create,
        )
        # Define what n means
        coefficients_explaination_new = Tex(
            coefficients_explaination_tex + " och $n$ är polynomets gradtal"
        )
        coefficients_explaination_new.next_to(general_polynomial_equation, DOWN)
        self.play(Write(coefficients_explaination_new))
        self.wait(0.5)
        self.next_slide()

    def animate_coefficient_value_trackers(
        self,
        coefficient_value_trackers: List[ValueTracker],
        coefficient_knobs: List[Knob],
    ) -> None:
        """Used for the scene where we animate how different coefficients control the "look" of polynomials.


        :param coefficient_value_trackers: A list of ValueTrackers for the different coefficients that the polynomial uses, in order lowest degree - highest.

        :param coefficient_knobs: A list of Knobs that is shown to visualize how the coefficients change the polynomial.
        """
        # We want to animate in the opposite order that the list uses
        for a in reversed(range(len(coefficient_value_trackers))):
            self.logger.info(
                f"Animating change of value tracker {a + 1}/{len(coefficient_value_trackers)}..."
            )
            # Reset other value trackers to their default values
            for b in range(len(coefficient_value_trackers)):
                if b != a:
                    coefficient_value_trackers[b].set_value(
                        coefficient_knobs[b].default_value
                    )
            coefficient_value_tracker = coefficient_value_trackers[a]
            coefficient_knob = coefficient_knobs[a]
            # Animate changing the coefficients
            self.play(
                coefficient_value_tracker.animate.set_value(coefficient_knob.max_value),
                run_time=5,
            )
            self.play(
                coefficient_value_tracker.animate.set_value(coefficient_knob.min_value),
                run_time=5,
            )
