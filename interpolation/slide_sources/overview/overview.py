"""overview.py
Provides an overview of some practical examples of interpolation.
"""

import os.path

from manim import (
    BackgroundRectangle,
    BLUE,
    Tex,
    Write,
    DOWN,
    Arrow,
    MathTex,
    UP,
    ImageMobject,
    UR,
    SMALL_BUFF,
    always_redraw,
    ReplacementTransform,
    MED_LARGE_BUFF,
    Circumscribe,
    RED,
    VGroup,
    GREEN,
)
from manim_slides.slide import ThreeDSlide
from sympy import lambdify

from helper_functions.graph import AxesAndGraphHelper, SYMBOL_X
from helper_functions.point_interpolation import (
    interpolate_over,
    interpolation_coefficients_to_function_template,
)
from interpolation.shared_constants import create_logger

SOURCE_CODE_FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LEMONADE_IMAGE_FILEPATH = os.path.join(SOURCE_CODE_FILE_DIRECTORY, "lemonade")


class Overview(ThreeDSlide):
    def construct(self):
        create_logger(self)
        # Add the lemonade image
        lemonade_image = ImageMobject(LEMONADE_IMAGE_FILEPATH)
        lemonade_image_final_scale = 1 / 4
        lemonade_image.scale(lemonade_image_final_scale)
        self.add(lemonade_image)
        self.wait(0.5)
        self.next_slide()
        # Shrink lemonade image
        new_lemonade_image = lemonade_image.copy()
        new_lemonade_image.scale(lemonade_image_final_scale)
        new_lemonade_image.to_corner(UR, buff=SMALL_BUFF)
        # Add some coordinates to illustrate the overview question
        # which is about lemonade
        ILLUSTRATIVE_COORDINATES = [[5, 4], [10, 9], [30, 27]]
        POINT_COLOR = GREEN  # Decide on cohesive, standout point color
        label_styling = lambda object: object.scale(
            0.5
        )  # Transformation to apply to axis labels
        self.axes = AxesAndGraphHelper(
            self,
            interval=[
                [0, ILLUSTRATIVE_COORDINATES[-1][0] + 20, 4],
                [0, ILLUSTRATIVE_COORDINATES[-1][1] + 10, 4],
            ],
            use_2d_axes_class=True,
            show_graph_labels_on_axes=[True, True, False],
            x_label="Tid (minuter)",
            y_label="Temperatur",
            x_label_styling=label_styling,
            y_label_styling=label_styling,
            z_label_styling=label_styling,
        )
        # Bring lemonade image to front
        new_lemonade_image.z_index = self.axes.number_plane.z_index + 1
        self.play(ReplacementTransform(lemonade_image, new_lemonade_image))
        self.next_slide()
        for coordinate in ILLUSTRATIVE_COORDINATES:
            self.axes.add_point(
                coordinate, show_coordinates=True, dot_color=POINT_COLOR
            )
            self.next_slide()
        self.next_slide()
        # Add the question
        question = Tex("""Hur varm var lemonaden efter $16$ minuter?""")
        question.scale(1.5)
        question_background = always_redraw(
            lambda: BackgroundRectangle(
                question,
                fill_opacity=1,
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=1,
                corner_radius=0.2,
                buff=MED_LARGE_BUFF,
            )
        )  # z index setting does not work z_index=new_lemonade_image.z_index+1))
        self.add(question_background)
        self.play(Write(question))
        self.next_slide()
        # Shrink question
        new_question = question.copy()
        new_question.scale(0.5)
        new_question.next_to(new_lemonade_image, DOWN)
        self.play(ReplacementTransform(question, new_question))
        self.next_slide()
        # Add arrow at x=16
        arrow_starting_y = 15
        arrow = Arrow(
            start=self.axes.axes_object.coords_to_point(16, arrow_starting_y + 5),
            end=self.axes.axes_object.coords_to_point(16, arrow_starting_y),
            color=RED,
            stroke_width=12,
        )
        arrow_head_text = MathTex("x=16")
        arrow_head_text.scale(1.25)
        arrow_head_text.next_to(arrow, UP)
        arrow_and_text_group = VGroup(arrow, arrow_head_text)
        self.add(arrow_and_text_group)
        self.play(Circumscribe(arrow_and_text_group, color=RED))
        self.next_slide()
        # Illustrate that we can construct an interpolation polynomial
        interpolation_coefficients = interpolate_over(ILLUSTRATIVE_COORDINATES)
        interpolation_function_template = (
            interpolation_coefficients_to_function_template(
                interpolation_coefficients, SYMBOL_X
            )
        )
        self.axes.plot_function(
            graph_function=interpolation_function_template,
            range_to_use_for_function=[0, 60],
            input_variables=[SYMBOL_X],
        )
        self.next_slide()
        interpolation_function = lambdify(
            [SYMBOL_X], interpolation_function_template, "numpy"
        )
        # Add point at X=16
        _, interpolated_y, _ = interpolation_function(16)
        self.axes.add_point(
            [16, interpolated_y],
            show_coordinates=False,
            return_created_objects=True,
            dot_color=POINT_COLOR,
        )
        self.next_slide()
