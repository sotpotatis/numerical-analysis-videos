"""knob.py
The knob is a type of value slider to visualize the value of a certain
variable."""

from math import cos, sin
from typing import Optional
from manim import (
    ValueTracker,
    PI,
    WHITE,
    Mobject,
    always_redraw,
    DOWN,
    DecimalNumber,
    LEFT,
    MathTex,
    Circle,
    VGroup,
    BLACK,
)
from manim_slides.slide import ThreeDSlide


# Comment: I originally tried using an SVG but I could not rotate it. So I changed to a regular image instead
# But it wobbled when rotating, so I moved on to using just two simple circles inside Manim.
# See _create_knobject below.
class Knob:
    """A value slider to visualize the current value of a certain variable."""

    def __init__(
        self,
        scene_reference: ThreeDSlide,
        value_tracker: ValueTracker,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        show_value_text: Optional[bool] = None,
        knobject_updater_function: Optional[callable] = None,
        value_text_updater_function: Optional[callable] = None,
        knob_label: Optional[str] = None,
    ):
        """Initializes a knob.

        :param scene_reference: Reference to the scene the graph should be displayed in.


        :param value_tracker: The value tracker that the knob should be linked to.

        :param min_value: The minimum value of the knob. Used to calculate rotation of the knob. Default is 1.

        :param max_value: The max value of the knob. Used to calculate rotation of the knob. Default is 10.

        :param show_value_text: Whether to show the value of the knob or not.

        :param knobject_updater_function: Optional function to run every time the knob is about to be redrawn.
        The function will be passed the Mobject responding to the knob image and can be used for things like ensuring positioning of the knob.

        :param value_text_updater_function: Optional function to run every time the knob value text is about to be redrawn.
        The function will be passed the Mobject responding to the knob image and can be used for things like ensuring positioning of the knob.


        :param knob_label: A label (in TeX format) that will be shown next to the knob.
        """
        if min_value is None:
            min_value = 1
        if max_value is None:
            max_value = 10
        if show_value_text is None:
            show_value_text = True
        self.scene_reference = scene_reference
        self.value_tracker = value_tracker
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = value_tracker.get_value()
        self.show_value_text = show_value_text
        self.knobject_updater_function = knobject_updater_function
        self.value_text_updater_function = value_text_updater_function
        # Create knob. Had to do a wordplay here KNOBject :)
        # Save an unrotated instance of the object.
        self.knobject_unrotated = self._create_knobject(rotation_angle=0)
        self.knobject = always_redraw(self._create_knobject)
        self.created_objects = [self.knobject]
        # Create value text
        if self.show_value_text:
            self.value_text = always_redraw(self._create_value_text)
            self.value_text.next_to(self.knobject, DOWN)
            self.created_objects.append(self.value_text)
        if knob_label is not None:
            self.knob_label_object = MathTex(knob_label)
            self.knob_label_object.scale(1.5)
            self.knob_label_object.next_to(self.knobject, LEFT, buff=1)
            self.created_objects.append(self.knob_label_object)

    def _create_knobject(self, rotation_angle: Optional[float] = None) -> Mobject:
        """Creates the KnobObject (wordplay KNOBject). This is the knob that is shown
        on the scene.

        :param rotation_angle: Optional value that will be used for the rotation angle of the knob.
        """
        if rotation_angle is None:
            rotation_angle = self.get_knob_rotation_angle(
                self.value_tracker.get_value()
            )
        # Draw the knob. Constants related to knob drawing
        background_circle_radius = 0.75
        background_circle_radius_with_offset = (
            background_circle_radius * 3 / 4
        )  # Radius to place indicator circle at
        knob_rotation_angle_offset = (
            PI / 2
        )  # Offset to know where to place the indicator circle. See below
        knobject_background_circle = Circle(
            radius=background_circle_radius,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        )
        # Execute passed updater function if provided. This can be used handle positioning etc.
        if self.knobject_updater_function is not None:
            self.knobject_updater_function(knobject_background_circle)
        # Add a circle indicating the magnitude of the value. Find out where to place it based on sine and cosine
        knobject_background_circle_point = knobject_background_circle.get_center()
        knobject_background_circle_point[
            0
        ] += background_circle_radius_with_offset * cos(
            rotation_angle + knob_rotation_angle_offset
        )
        knobject_background_circle_point[
            1
        ] += background_circle_radius_with_offset * sin(
            rotation_angle + knob_rotation_angle_offset
        )
        knobject_indicator_circle = Circle(
            radius=0.1, fill_color=BLACK, fill_opacity=1, stroke_width=0
        )
        knobject_indicator_circle.move_to(knobject_background_circle_point)
        return VGroup(knobject_background_circle, knobject_indicator_circle)

    def _create_value_text(self) -> DecimalNumber:
        """Creates a text object that shows the current value.

        :param value: The value to show on the text object. May also be None, if so the text will be empty.
        """
        value_text = DecimalNumber(number=self.value_tracker.get_value(), color=WHITE)
        value_text.scale(0.75)
        value_text.next_to(self.knobject, DOWN)
        # Execute passed updater function if provided. This can be used handle positioning etc.
        if self.value_text_updater_function is not None:
            self.value_text_updater_function(value_text)
        return value_text

    def get_knob_rotation_angle(self, value: float) -> float:
        """Based on an integer value, get the knobs rotation.

        :param value The value that the knob should be set to

        :returns The angle that the knob should be rotated, in radians."""
        # Given that the rotation when value=min = -pi/4 and the
        # rotation when value = max = pi/4:
        MAX_ROTATION = -PI / 4
        MIN_ROTATION = -1 * MAX_ROTATION
        k = (MAX_ROTATION - MIN_ROTATION) * ((self.max_value - self.min_value) ** -1)
        rotation_angle = MIN_ROTATION + k * (value - self.min_value)
        if rotation_angle > MIN_ROTATION or rotation_angle < MAX_ROTATION:
            raise ValueError(
                f"""The passed value is too big, please adjust the boundaries of your knob rotation.
            You passed {value} but the value should be between {self.max_value}, {self.min_value}.
            Generated k={k} and rotation angle={rotation_angle/PI} radians"""
            )
        return rotation_angle
