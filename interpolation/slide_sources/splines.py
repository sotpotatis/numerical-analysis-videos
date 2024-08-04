"""splines.py
Demonstrates the concept of splines."""

from manim_slides.slide import ThreeDSlide
from typing import Optional, List, Tuple, Union

from manim import (
    MathTex,
    UP,
    ReplacementTransform,
    DOWN,
    Mobject,
    Dot3D,
    Tex,
    WHITE,
    GrowFromCenter,
    ManimColor,
    VGroup,
    ParametricFunction,
    BackgroundRectangle,
    BLUE,
    Create,
    MED_LARGE_BUFF,
)
from sympy import lambdify
from helper_functions.general_utilities import (
    clear_screen,
    play_multiple,
)
from helper_functions.graph import SYMBOL_X
from helper_functions.latex_utilities import create_list
from helper_functions.point_interpolation import (
    interpolation_coefficients_to_function_template,
    linear_spline_interpolation,
    cubic_spline_interpolation,
)
from helper_functions.premade_slides import (
    create_bullet_list_and_title_frame,
)
from helper_functions.graph import AxesAndGraphHelper
from interpolation.shared_constants import (
    all_evaluated_points,
    set_title_heading_to,
    add_witch_of_agnesi_points,
    create_logger,
)
from helper_functions.text_scales import TOP_HEADING_SCALE
from helper_functions.color_utilities import (
    cycle_through_color_wheel,
    darker_or_brighter,
)


class Splines(ThreeDSlide):
    # Manually define the positions of the labels that highlight what number
    # the interpolation polynomial is. See plot_spline_polynomial for the usage.
    POLYNOMIAL_LABEL_POSITIONS = [DOWN] + [UP] * 4 + [DOWN] * 2 + [UP] + [DOWN] * 2

    def construct(self):
        create_logger(self)
        set_title_heading_to(self, "Splines")
        self.axes = AxesAndGraphHelper(
            self,
            interval=[[-10, 11], [0, 5]],
            use_2d_axes_class=True,
            show_graph_labels_on_axes=[False, True, False],  # Hide x axis label
        )
        # Demonstrate splines
        add_witch_of_agnesi_points(self, all_evaluated_points, animation_run_time=0)
        # Indicate that we create a spline between every 2 points
        # Make every interval clearer by indicating its color
        # We have 11 points so we will get 10 polynomials.
        INTERVAL_COLORS = cycle_through_color_wheel(10)
        # Construct splines between the evaluated points. Start by generating coefficients
        all_evaluated_points.sort(key=lambda point: point[0])  # Sort points by x
        linear_spline_coefficients = linear_spline_interpolation(all_evaluated_points)
        cubic_spline_coefficients = cubic_spline_interpolation(all_evaluated_points)
        # Create a list of all the points{ in the different intervals
        interval_x_locations = []  # List of the x interval that an interval is between
        for i in range(len(all_evaluated_points)):
            interval_x_locations.append(
                [x_value for x_value, y_value in all_evaluated_points[i : i + 2]]
            )
        self.logger.debug(
            f"Generated linear spline coefficients: {linear_spline_coefficients}"
        )
        self.logger.debug(
            f"Generated cubic spline coefficients: {cubic_spline_coefficients}"
        )
        self.logger.debug(f"Intervals for splines: {interval_x_locations}")

        # Plot each function. We do this separately because we want them to be different slides
        # We save the kwargs since we will transform the plot later. See below.
        number_of_intervals = len(linear_spline_coefficients)
        linear_interpolation_plots = []
        all_linear_interpolation_kwargs = []
        linear_interpolation_polynomial_labels = []
        for interval_index in range(number_of_intervals):
            self.logger.info(
                f"Plotting linear spline over interval {interval_x_locations[interval_index]} (interval {interval_index+1}/{number_of_intervals})"
            )
            linear_interpolation_kwargs = {
                "graph_function": interpolation_coefficients_to_function_template(
                    linear_spline_coefficients[interval_index], SYMBOL_X
                ),
                "input_variables": [SYMBOL_X],
                "range_to_use_for_function": interval_x_locations[interval_index],
                "plot_color": INTERVAL_COLORS[interval_index],
            }
            function_plot, function_label = self.plot_spline_polynomial(
                linear_interpolation_kwargs, interval_index + 1
            )
            linear_interpolation_plots.append(function_plot)
            linear_interpolation_polynomial_labels.append(function_label)
            all_linear_interpolation_kwargs.append(linear_interpolation_kwargs)
        self.wait(0.5)
        self.next_slide()
        # Fade out the linear interpolation polynomials. We do so by darkening their color
        self.transform_plot_colors(
            all_linear_interpolation_kwargs,
            linear_interpolation_plots,
            [darker_or_brighter(color, brighter=False) for color in INTERVAL_COLORS],
        )
        self.next_slide()
        for label in linear_interpolation_polynomial_labels:
            self.remove(label)
        self.next_slide()
        # Plot the cubic interpolation polynomials
        cubic_interpolation_plots = []
        cubic_interpolation_polynomial_labels = []
        all_cubic_interpolation_kwargs = []
        for interval_index in range(number_of_intervals):
            self.logger.info(
                f"Plotting cubic spline over interval {interval_x_locations[interval_index]} (interval {interval_index+1}/{number_of_intervals})"
            )
            cubic_interpolation_kwargs = {
                "graph_function": interpolation_coefficients_to_function_template(
                    cubic_spline_coefficients[interval_index], SYMBOL_X
                ),
                "input_variables": [SYMBOL_X],
                "range_to_use_for_function": interval_x_locations[interval_index],
                "plot_color": INTERVAL_COLORS[interval_index],
            }
            all_cubic_interpolation_kwargs.append(cubic_interpolation_kwargs)
            function_plot, function_label = self.plot_spline_polynomial(
                cubic_interpolation_kwargs, interval_index + 1
            )
            cubic_interpolation_plots.append(function_plot)
            cubic_interpolation_polynomial_labels.append(function_label)
        self.wait(0.5)
        self.next_slide()
        # Animate the effect that a cubic interpolation polynomial has on the smoothing of
        # points by changing the color of the cubic interpolation plots to the same color
        self.transform_plot_colors(
            all_cubic_interpolation_kwargs,
            cubic_interpolation_plots,
            INTERVAL_COLORS[0],
        )
        self.next_slide()
        # Show the characteristics of a cubic interpolation polynomial.
        clear_screen(self)
        # Indicate that this is true for all polynomials, that is p_1, p_2, p_3, etc...
        bullet_point_and_title_frame_objects = None
        for interval_index in range(3):
            # The two polynomial numbers to show for this iteration
            p1_number, p2_number = [interval_index + 1, interval_index + 2]
            points_involved_in_interpolation = all_evaluated_points[
                interval_index : interval_index + 3
            ]
            first_endpoint_x, middle_point_x, second_endpoint_x = [
                point[0] for point in points_involved_in_interpolation
            ]
            first_endpoint_y, middle_point_y, second_endpoint_y = [
                round(point[1], 2) for point in points_involved_in_interpolation
            ]
            derivatives_equal_strings = []
            # There is one string in the point list that is basically the same except for the prime sign.
            # Automate it.
            for i in range(1, 4):
                derivative_prefix = "^{" + "'" * i + "}"
                derivatives_equal_strings.append(
                    "$p%s_{%d}(%r)=p%s_{%d}(%r)$"
                    % (
                        derivative_prefix,
                        p1_number,
                        middle_point_x,
                        derivative_prefix,
                        p2_number,
                        middle_point_x,
                    )
                )
            clear_screen(self)
            is_first_slide = bullet_point_and_title_frame_objects is None
            self.logger.info(
                f"Adding bullet points for polynomials {p1_number} and {p2_number}"
            )
            bullet_point_and_title_frame_objects = create_bullet_list_and_title_frame(
                self,
                "Karaktäristiskt för splines $p_{%d}$ och $p_{%d}$:"
                % (p1_number, p2_number),
                [
                    "Första polynomet $p_{%d}$, går genom $(%r, %r)$ och $(%r, %r)$"
                    % (
                        p1_number,
                        first_endpoint_x,
                        first_endpoint_y,
                        middle_point_x,
                        middle_point_y,
                    ),
                    "Andra polynomet, $p_{%d}$ går genom $(%r, %r)$ och $(%r, %r)$"
                    % (
                        p2_number,
                        middle_point_x,
                        middle_point_y,
                        second_endpoint_x,
                        second_endpoint_y,
                    ),
                    derivatives_equal_strings[0]
                    + r" (samma \textit{första}derivata vid mittpunkten)",
                    derivatives_equal_strings[1]
                    + r" (samma \textit{andra}derivata vid mittpunkten)",
                    (
                        "$p^{''}_{%d}(%r)=0$ och $p^{''}_{%d}(%r)=0$"
                        % (p1_number, first_endpoint_x, p2_number, second_endpoint_x)
                        + r" (andraderivator noll vid ändpunkter)"
                    ),
                ],
                # Animate all bullet points one by one only the first time
                show_bullet_points_one_by_one=is_first_slide,
                fade_in=True,
            )
            self.wait(0.5)
            self.next_slide()
        # Add a text showing that the rules in the bullet point list are generic
        clear_screen(self)
        and_so_forth_text = Tex("...och så vidare!")
        and_so_forth_text.scale(2)
        self.play(GrowFromCenter(and_so_forth_text))
        self.next_slide()
        clear_screen(self)
        # Add some general rules to keep in mind
        general_rules_title = Tex("Minnesregler", color=BLUE)
        general_rules_title.scale(TOP_HEADING_SCALE)
        general_rules_title.to_edge(UP, buff=MED_LARGE_BUFF)
        general_rules_text = Tex(
            create_list(
                [
                    r"$\text{Antal (individuella) splines-polynom}=\text{Antal datapunkter}-1$",
                    r"Antal ekvationer som krävs: $4\cdot \text{Antal datapunkter}$ (för kubiska splines)",
                ]
            )
        )
        general_rules_text.next_to(general_rules_title, DOWN)
        play_multiple(self, [general_rules_title, general_rules_text], Create)
        self.wait(0.5)
        self.next_slide()

    def transform_plot_colors(
        self,
        all_old_plot_kwargs: List[dict],
        old_plots: List[Mobject],
        new_colors: Union[List[ManimColor], ManimColor],
    ) -> None:
        """Change the color of an earlier plot and animate the change.

        :param old_plot_kwargs: Kwargs passed to the plot_function method to generate the old plot.

        :param old_plot: The old plot that we want to change the color of.

        :param new_colors: The new color we want to change the plot to. If a list, the colors will be different for each plot.
        If not a list, the same color will be used for all plots.

        """
        self.logger.info(f"Transforming {len(old_plots)} old plots.")
        for i in range(len(old_plots)):
            self.logger.info(
                f"Transforming interpolation polynomial {i + 1}/{len(old_plots)}"
            )
            old_plot = old_plots[i]
            old_plot_kwargs = all_old_plot_kwargs[i]
            if isinstance(new_colors, list):
                old_plot_kwargs["plot_color"] = new_colors[i]
            else:
                old_plot_kwargs["plot_color"] = new_colors
            old_plot_kwargs["animate"] = False
            new_plot = self.plot_spline_polynomial(old_plot_kwargs, None)[0]
            self.logger.info(f"Transforming {old_plot} into {new_plot}")
            self.play(ReplacementTransform(old_plot, new_plot))

    def plot_spline_polynomial(
        self, plot_kwargs: dict, polynomial_number: Optional[int] = None
    ) -> Tuple[ParametricFunction, Optional[Mobject]]:
        """Plot a spline polynomial. The reason this is its own function is that we add the ability
        to add a "number label" (p_1(x), p_2(x)) etc. underneath the plotted curve."""
        plotted_function = self.axes.plot_function(**plot_kwargs)
        created_objects = [plotted_function]
        if polynomial_number is not None:
            label_color = plot_kwargs.get("plot_color", WHITE)
            x_interval = plot_kwargs["range_to_use_for_function"]
            middle_point_x = x_interval[0] + 1 / 2 * abs(x_interval[1] - x_interval[0])
            # Add a label indicating the number of the spline polynomial
            # Comment: self.axes.axes_object.get_graph_label did not work, for p1 it kept placing it on top of p2.
            # I therefore had to implement it myself.
            plot_label = MathTex(r"p_{%d}(x)" % (polynomial_number), color=label_color)
            # Get function value at middle point and add the label to there
            graph_lambda_function = lambdify(
                plot_kwargs["input_variables"], plot_kwargs["graph_function"], "numpy"
            )
            self.logger.info(
                f"Adding label for polynomial {polynomial_number}, positioned at x={middle_point_x} with color {label_color}"
            )
            point_to_move_to = graph_lambda_function(middle_point_x)
            # Add a dummy dot, this is only to position the plot label above the function plot.
            dummy_dot = Dot3D()
            dummy_dot.move_to(self.axes.axes_object.coords_to_point(*point_to_move_to))
            plot_label.next_to(
                dummy_dot, self.POLYNOMIAL_LABEL_POSITIONS[polynomial_number - 1]
            )
            plot_label_background = BackgroundRectangle(
                plot_label, fill_opacity=1, stroke_width=0
            )
            plot_label_with_background = VGroup(plot_label_background, plot_label)
            created_objects.append(plot_label_with_background)
            self.add(plot_label_with_background)
        return tuple(created_objects)
