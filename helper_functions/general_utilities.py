"""general_utilities.py
Utilities used at many places in the project."""

from typing import Union, List, Optional
from manim import Mobject, Animation
from manim_slides.slide import Slide, ThreeDSlide


def play_multiple(
    source_scene: Union[Slide, ThreeDSlide],
    items_to_animate: List[Mobject],
    animation_to_play: Animation,
    *args,
    **kwargs,
) -> None:
    """Plays an animation on multiple items.

    :param source_scene: The scene to play the animation in.

    :param items_to_animate: A list of items to animate.

    :param animation_to_play: The animation to play on the items.

    Other args and kwargs passed will be passed to play."""
    for item in items_to_animate:
        source_scene.play(animation_to_play(item, *args, **kwargs))


def addition_string(input_number: Union[int, float]) -> str:
    """If you're rendering a string like 1+2+3 this is a helpful function.
    Formats a number for either addition or subtraction depending on its value.

    :param input_number The number to base the result and check on.

    :retuns +{number} if the number is positive, otherwise {number}.
    (example: input 1 --> output +1. input -1 --> output -1"""
    if input_number < 0:
        return str(input_number)
    else:
        return f"+{input_number}"


def clear_screen(
    source_scene: Union[Slide, ThreeDSlide], items_to_preserve: Optional[List] = None
) -> None:
    """Clears the current scene by removing all Mobjects.

    :param source_scene: The scene to clear objects from.

    :param items_to_preserve: A list of items to preserve. If not set, will remove all items.
    """
    if items_to_preserve is None:
        items_to_preserve = []
    for item in source_scene.mobjects:
        if item not in items_to_preserve:
            source_scene.remove(item)


def format_to_parenthesis_if_negative(source_number: Union[float, int, str]) -> str:
    """Formats a number, adding parenthesis if it's smaller than 0, otherwise preserves the number.
    For example: input -6 (float) --> (-6) (string). Input 2 (float) --> 2 (string).

    :param source_number: The number to format. If not a number (float, int) but a string,
    float(string) will be applied to the input"""
    if not isinstance(source_number, float) or not isinstance(source_number, int):
        source_number = float(source_number)
        if source_number.is_integer():
            source_number = int(source_number)
    return f"({source_number})" if source_number < 0 else repr(source_number)
