"""premade_slides.py
Contains some functions that can be used to create premade slides.
"""

import logging
from typing import Optional, List
from manim import (
    Tex,
    Group,
    FadeIn,
    DOWN,
    UL,
    Title,
    Mobject,
    LEFT,
    BulletedList,
)
from manim_slides.slide import ThreeDSlide

logger = logging.getLogger(__name__)


def create_title_frame(
    scene_reference: ThreeDSlide, title_text: str, subtitle_text: Optional[str] = None
) -> Group:
    """Creates a title frame.

    :param scene_reference A reference to the current scene.

    :param title_text: The title text to show.

    :param subtitle_text: The subtitle text to show."""
    # Create group to hold the two texts
    text_group = Group()
    title = Tex(rf"\Huge {title_text} \normalfont")
    text_group.add(title)
    if subtitle_text is not None:
        subtitle = Tex(rf"\Large {subtitle_text} \normalfont")
        text_group.add(subtitle)
        subtitle.next_to(title, DOWN)
    text_group.center()
    scene_reference.play(FadeIn(text_group))
    return text_group


def create_bullet_list_and_title_frame(
    scene_reference: ThreeDSlide,
    title_text: str,
    bullet_points: List[str],
    show_bullet_points_one_by_one: Optional[bool] = None,
    fade_in: Optional[bool] = False,
) -> List[Mobject]:
    """The essential PowerPoint classic. A bullet list with a title on top of the frame.
    Since Manim uses TeX to create the bullet list, you can do things like include math: just pass $$x^2$$ as an entry

    :param scene_reference: A reference to the current scene.

    :param title_text: The title text to show.

    :param bullet_points: A list of strings to show as bullet points.

    :param show_bullet_points_one_by_one: If True, the bullet points will be shown one by one. If False, all bullet points will be shown at once. Default is True.

    :param fade_in: Whether to play a fade in animation or not. Default if unset is true.

    Comment: If you need to implement color support later, see https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.BulletedList.html
    """
    if show_bullet_points_one_by_one is None:
        show_bullet_points_one_by_one = True
    if fade_in is None:
        fade_in = True
    logger.debug(f"Creating bullet point list with texts: {bullet_points}")
    title = Title(title_text).to_corner(UL).align_to(LEFT)
    # Create function to position and align bullet point list
    list_alignment = lambda list: list.next_to(title, DOWN, aligned_edge=LEFT)
    scene_reference.add(title)
    added_objects = [title]
    if show_bullet_points_one_by_one:
        bullet_point_list = BulletedList(bullet_points[0])
        list_alignment(bullet_point_list)
        scene_reference.next_slide()
        for i in range(1, len(bullet_points)):
            # Remove old list and fade in new one
            scene_reference.remove(bullet_point_list)
            bullet_point_list = BulletedList(*bullet_points[0:i])
            list_alignment(bullet_point_list)
            if fade_in:
                scene_reference.play(FadeIn(bullet_point_list))
            else:
                scene_reference.add(bullet_point_list)
            scene_reference.next_slide()
    else:  # Add all points directly if no animation should be played
        bullet_point_list = BulletedList(*bullet_points)
        if fade_in:
            scene_reference.play(FadeIn(bullet_point_list))
        else:
            scene_reference.add(bullet_point_list)
    added_objects.append(bullet_point_list)
    return added_objects
