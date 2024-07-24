"""loading.py
Shows a loading animation by showing a loading spinner on the screen"""

import os
from typing import Union, Optional

from manim import ImageMobject, Rotate, PI, BackgroundRectangle, BLACK
from manim_slides.slide import Slide, ThreeDSlide

FILE_BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LOADING_SPINNER_ASSET_PATH = os.path.join(FILE_BASE_DIRECTORY, "loading_spinner.png")


class LoadingSpinner:
    """A loading spinner which can be placed on the screen."""

    def __init__(
        self,
        scene_reference: Union[Slide, ThreeDSlide],
        before_addition_function: Optional[callable] = None,
        transparent_background: Optional[bool] = None,
    ) -> None:
        """Initializes a loading spinner.

        :param scene_reference: The scene to place the loading spinner on.

         :param before_addition_function: Optional function to run before adding the loading spinner to the scene.
        The function will be passed the loading spinner Mobject and can be used for things like ensuring positioning of the spinner.
        """
        if transparent_background is None:
            transparent_background = False
        self.scene_reference = scene_reference
        self.before_addition_function = before_addition_function
        self.loading_spinner = ImageMobject(LOADING_SPINNER_ASSET_PATH)
        self.loading_spinner.scale(4)
        self.created_objects = []
        if self.before_addition_function is not None:
            self.before_addition_function(self.loading_spinner)
        if not transparent_background:
            self.loading_spinner_background = BackgroundRectangle(
                self.loading_spinner, color=BLACK, fill_opacity=1
            )
            self.created_objects.append(self.loading_spinner_background)
        self.created_objects.append(self.loading_spinner)
        self.scene_reference.add(*self.created_objects)

    def spin(
        self,
        duration: Optional[float] = None,
        number_of_rotations: Optional[int] = None,
    ) -> None:
        """Play a spinning animation for a number of seconds.

        :param duration: How long to play the spinner animation for. Defaults to 1 second

        :param number_of_rotations: Total number of rotations to make. Defaults to 3 full rotations
        """
        if duration is None:
            duration = 1
        if number_of_rotations is None:
            number_of_rotations = 3
        self.scene_reference.play(
            Rotate(
                self.loading_spinner,
                angle=2 * PI * number_of_rotations,
                duration=duration,
            )
        )
