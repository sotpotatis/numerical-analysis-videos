"""color_utilities.py
I love adding some color to my life!
This file is all about custom colors."""

import logging
import warnings
from typing import Optional, List, Union

from manim.utils.color.core import ManimColor
from numpy import arange

logger = logging.getLogger(__name__)


def cycle_through_color_wheel(
    number_of_colors: int,
    base_saturation: Optional[int] = None,
    base_brightness: Optional[int] = None,
) -> List[ManimColor]:
    """Cycles through the full hue values of the "color wheel" using HSB/HSV color format.
    Basically, if you pass number_of_colors=5, you will get 5 colors with the same saturation and brightness, but hue values
    ranging from 0-360 with the step equal to 359/number_of_colors

    :param number_of_colors: The number of colors to generate.

    :param base_saturation: The base saturation to use. Default is 80.

    :param base_brightness: The base brightness to use. Default is 100.
    """
    if base_saturation is None:
        base_saturation = 80
    if base_brightness is None:
        base_brightness = 100
    if number_of_colors < 2:
        raise ValueError("Too few colors requested! Please request at least 2.")
    if not 0 <= base_saturation <= 100 or not 0 <= base_brightness <= 100:
        raise ValueError(
            "Invalid base saturation or base brightness (must be between 0 and 100)"
        )
    step = 359 / number_of_colors
    generated_colors = []
    for i in arange(0, 359, step):
        hsb_value = (i, base_saturation, base_brightness)
        generated_colors.append(
            ManimColor.from_hsv(convert_manim_hsv_format(*hsb_value))
        )
    return generated_colors


def darker_or_brighter(
    color: ManimColor,
    brighter: Optional[bool] = None,
    brightness_change: Optional[int] = None,
):
    """Return a color that is brighter or darker than a certain ManimColor.
    This is done by increasing the V value of the HSV color.

    :param color: The color to base the result on.

    :param brighter: Whether to return the brighter or darker color. If unset, will return the darker color.

    :param brightness_change: How much to increase the V value by. If unset, will increase by 50.
    """
    if brightness_change is None:
        brightness_change = 50
    original_color = convert_manim_hsv_format(
        *color.to_hsv(), to_manim_color_format=False
    )
    new_color = list(original_color)
    if not brighter:
        brightness_change = -1 * brightness_change
    v = new_color[2] + brightness_change
    # Ensure v is in [0, 100]
    if v > 100:
        warnings.warn(
            f"The increase to brighten the color {original_color} resulted in a too bright color. It's suggested that you use a darker color for better effect."
        )
        v = 100
    elif v < 0:
        warnings.warn(
            f"The decrease to darken the color {original_color} resulted in a too dark color. It's suggested that you use a brighter color for better effect."
        )
        v = 0
    new_color[2] = v
    logger.debug(f"Brightened up color: {original_color}-->{new_color}")
    return ManimColor.from_hsv(convert_manim_hsv_format(*new_color))


def convert_manim_hsv_format(
    h: Union[int, float],
    s: Union[int, float],
    v: Union[int, float],
    to_manim_color_format: Optional[bool] = None,
) -> tuple[float, float, float]:
    """In my brain, I've always thought of the HSV color format as ranging from:
    H: 0-360, S: 0-100, V: 0-100.
    However Manim uses a different format, so this function converts between the two.

    :param h: The hue value to convert.

    :param s: The saturation value to convert.

    :param v: The brightness value to convert.

    :param to_manim_color_format: Whether to convert from the "normal" HSV format to the Manim format. If unset, will convert
    to the Manim format."""
    if to_manim_color_format is None:
        to_manim_color_format = True
    if to_manim_color_format:
        return h / 360, s / 100, v / 100
    else:
        return h * 360, s * 100, v * 100
