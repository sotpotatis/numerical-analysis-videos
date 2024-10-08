"""premade_slides.py
Contains some functions that can be used to create premade slides.
"""

import logging
from typing import Optional, List, Tuple, Union
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
    WHITE,
    UP,
    ManimColor,
    Create,
    BLUE,
)
from manim_slides.slide import ThreeDSlide, Slide

from helper_functions.general_utilities import clear_screen, play_multiple
from helper_functions.latex_utilities import create_list
from helper_functions.text_scales import TOP_HEADING_SCALE


logger = logging.getLogger(__name__)


def create_title_frame(
    scene_reference: ThreeDSlide,
    title_text: str,
    subtitle_text: Optional[str] = None,
    title_scale: Optional[float] = None,
    subtitle_scale: Optional[float] = None,
) -> Group:
    """Creates a title frame.

    :param scene_reference A reference to the current scene.

    :param title_text: The title text to show.

    :param subtitle_text: The subtitle text to show.

    :param title_scale: Control the scale of the title if you'd wish!

    :param subtitle_scale: Control the scale of the subtitle if you'd wish!
    """
    if title_scale is None:
        title_scale = 1
    if subtitle_scale is None:
        subtitle_scale = 1
    # Create group to hold the two texts
    text_group = Group()
    title = Tex(rf"\Huge {title_text} \normalfont")
    title.scale(title_scale)
    text_group.add(title)
    if subtitle_text is not None:
        subtitle = Tex(rf"\Large {subtitle_text} \normalfont")
        subtitle.scale(subtitle_scale)
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
    show_numbers_instead_of_bullets: Optional[bool] = None,
) -> List[Mobject]:
    """The essential PowerPoint classic. A bullet list with a title on top of the frame.
    Since Manim uses TeX to create the bullet list, you can do things like include math: just pass $$x^2$$ as an entry

    :param scene_reference: A reference to the current scene.

    :param title_text: The title text to show.

    :param bullet_points: A list of strings to show as bullet points.

    :param show_bullet_points_one_by_one: If True, the bullet points will be shown one by one. If False, all bullet points will be shown at once. Default is True.

    :param fade_in: Whether to play a fade in animation or not. Default if unset is true.

    Comment: If you need to implement color support later, see https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.BulletedList.html

    :param show_numbers_instead_of_bullets: If True, will display the passed items as a list with numbers instead of bullets
    """
    if show_bullet_points_one_by_one is None:
        show_bullet_points_one_by_one = True
    if fade_in is None:
        fade_in = True
    if show_numbers_instead_of_bullets is True:
        additional_bullet_point_kwargs = {"dot_scale_factor": 0}
        # Add numbers to all bullet points
        new_bullet_points = []
        for i in range(1, len(bullet_points) + 1):
            new_bullet_points.append(f"{i}. {bullet_points[i-1]}")
        bullet_points = new_bullet_points
    else:
        additional_bullet_point_kwargs = {}
    logger.debug(f"Creating bullet point list with texts: {bullet_points}")
    title = Title(title_text).to_corner(UL).align_to(LEFT)
    # Create function to position and align bullet point list
    list_alignment = lambda list: list.next_to(title, DOWN, aligned_edge=LEFT)
    scene_reference.add(title)
    added_objects = [title]
    if show_bullet_points_one_by_one:
        bullet_point_list = BulletedList(
            bullet_points[0], **additional_bullet_point_kwargs
        )
        list_alignment(bullet_point_list)
        scene_reference.next_slide()
        for i in range(1, len(bullet_points) + 1):
            # Remove old list and fade in new one
            scene_reference.remove(bullet_point_list)
            bullet_point_list = BulletedList(
                *bullet_points[0:i], **additional_bullet_point_kwargs
            )
            list_alignment(bullet_point_list)
            if fade_in:
                scene_reference.play(FadeIn(bullet_point_list))
            else:
                scene_reference.add(bullet_point_list)
            scene_reference.wait(0.5)
            scene_reference.next_slide()
    else:  # Add all points directly if no animation should be played
        bullet_point_list = BulletedList(
            *bullet_points, **additional_bullet_point_kwargs
        )
        if fade_in:
            scene_reference.play(FadeIn(bullet_point_list))
        else:
            scene_reference.add(bullet_point_list)
    added_objects.append(bullet_point_list)
    return added_objects


def create_slide_with_title_and_mobjects(
    scene_reference: ThreeDSlide,
    title: str,
    mobjects: List[Mobject],
    title_color: Optional[ManimColor] = None,
    play: Optional[bool] = None,
) -> List[Mobject]:
    """See the lovely docstring. A slide with a title and mobjects below.

    :param scene_reference: A reference to the current scene.

    :param title:  The title to show on the slide.

    :param mobjects: Additional Mobjects to add to the slide.

    :param title_color: The color of the title. Default is white.

    :param play: If False, the function will not play (add) the slide, but just return the objects.
    The coder can then handle the rendering themselves. Defaults to True.

    :returns A list of all the mobjects  in the scene the format [heading, <other added mobjects>]
    """
    if title_color is None:
        title_color = WHITE
    if play is None:
        play = True
    if play:
        clear_screen(scene_reference)
    heading = Tex(title, color=title_color)
    heading.scale(TOP_HEADING_SCALE)
    heading.to_edge(UP)
    # Add all mobjects passed to the function and position them below each other
    prev_mobject = heading
    for moject_to_add in mobjects:
        moject_to_add.next_to(prev_mobject, DOWN)
        prev_mobject = moject_to_add
    all_mobjects = [heading]
    all_mobjects.extend(mobjects)
    if play:
        play_multiple(scene_reference, all_mobjects, Create)
        scene_reference.wait(0.5)
        scene_reference.next_slide()
    return all_mobjects


def create_method_explanatory_slide(
    scene_reference: ThreeDSlide,
    title: str,
    explanation_tex: str,
    extra_mobjects: Optional[List[Mobject]] = None,
    title_color: Optional[ManimColor] = None,
    play: Optional[bool] = None,
) -> Tuple[Mobject, Mobject]:
    """Creates a slide with a title and some LateX beneath, which can be used to explain a math concept
    and summarizing a key part.

    :param scene_reference: A reference to the current scene.

    :param title:  The title to show on the slide.

    :param explanation_tex: The explanation LaTeX source code to show on the slide.

    :param extra_mobjects: Additional Mobjects to add to the slide.

    :param title_color: The color of the title. Default is white.

    :param play: If False, the function will not play (add) the slide, but just return the objects.
    The coder can then handle the rendering themselves. Defaults to True.

    :returns A tuple of the created mobjects in format:
    (title mobject, LaTeX explanation mobject, optional mobjects from extra_mobjects)
    """
    if extra_mobjects is None:
        extra_mobjects = []
    explanation = Tex(explanation_tex)
    mobjects_to_add = [explanation]
    mobjects_to_add.extend(extra_mobjects)
    created_mobjects = create_slide_with_title_and_mobjects(
        scene_reference, title, mobjects_to_add, title_color, play
    )
    # created_mobjects[0] is the heading
    return created_mobjects[0], explanation


def create_general_rules_slide(
    scene_reference: Union[Slide, ThreeDSlide],
    general_rules: List[str],
    *args,
    **kwargs,
) -> List[Mobject]:
    """Creates a list of general rules. Such list is displayed at the end of an important segment
    to add a little cheatsheet.


    :param scene_reference: A reference to the current scene.

    :param general_rules: A list of general rules as a list of TeX strings.

    :param args: Any arguments to pass to the create_slide_with_title_and_mobjects function.

    :param kwargs: Any keyword arguments to pass to the create_slide_with_title_and_mobjects function.
    """
    general_rules_text = Tex(create_list(general_rules))
    create_slide_with_title_and_mobjects(
        scene_reference,
        "Minnesregler",
        [general_rules_text],
        *args,
        title_color=BLUE,
        **kwargs,
    )
