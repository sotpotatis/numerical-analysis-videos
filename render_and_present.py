"""render_and_present.py
See SCRIPT_DESCRIPTION"""

import os, sys, logging
from pathlib import Path
from argparse import ArgumentParser
from redbaron import RedBaron

SCRIPT_DESCRIPTION = """Small CLI version to render and present a set of slides.
Useful when you have multiple files containing the slides that one presentation should use."""
# Create logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# Create CLI
cli = ArgumentParser(description=SCRIPT_DESCRIPTION)
cli.add_argument(
    "slides_path",
    type=Path,
    help="The path to the slides to render. This directory should have a folder slide_sources/ with all the slides.",
)
cli.add_argument(
    "--present_only",
    action="store_true",
    help="Will skip rendering the files and present them directly.",
)
arguments = cli.parse_args()
slides_path = os.path.join(os.getcwd(), arguments.slides_path)
slides_source_files = os.path.join(slides_path, "slide_sources")
if not os.path.exists(slides_path) or not os.path.exists(slides_source_files):
    logger.critical(
        "Could not find the slides path that you enterred, or the directory slide_source within it. Please verify that those two exists!"
    )
    exit(1)
FILE_PATH = os.path.realpath(__file__)
FILE_DIRECTORY = os.path.dirname(FILE_PATH)
IGNORED_PRESENTATION_FILES = ["__pycache__", ".slides_order"]


# Add slides path to pwd
def add_to_path(text_to_add):
    os.environ["PATH"] += os.pathsep + text_to_add
    sys.path.append(text_to_add)


add_to_path(slides_path)
add_to_path(FILE_DIRECTORY)
slide_parts = os.listdir(slides_source_files)
logger.info("Creating presentation...")
os.chdir(slides_path)
for ignored_file in IGNORED_PRESENTATION_FILES:
    if ignored_file in slide_parts:
        slide_parts.remove(ignored_file)
slide_parts_to_render = [
    os.path.join(slides_source_files, slide_part) for slide_part in slide_parts
]

# You can optionally ensure the order of how the slides are rendered if the file .slides_order is created.
SLIDE_ORDER_FILEPATH = os.path.join(slides_source_files, ".slides_order")
if os.path.exists(SLIDE_ORDER_FILEPATH):
    logger.info("Will apply slide ordering.")
    # The .slides_order file should be structured like this:
    # file_1
    # file_2
    # file_3
    # If you want the slides from file_1 to appear first, file_2 to appear second, etc.
    slide_order_file_contents = open(SLIDE_ORDER_FILEPATH).read().splitlines()

    def slide_parts_file_ordering(slide_file: str) -> int:
        """Key lookup function for ordering files containing slides based on a user-provided order.

        :param slide_file: The path of the slide file."""
        slide_filename = Path(slide_file).stem
        if slide_filename in slide_order_file_contents:
            return slide_order_file_contents.index(slide_filename)
        else:
            raise ValueError(
                f"""{slide_filename} is not present in the slide ordering file, so I do not know where to place it.
            Please add an entry on that file."""
            )

    logger.info("Ordering slide parts...")
    slide_parts_to_render.sort(key=slide_parts_file_ordering, reverse=True)
    logger.info(f"Ordered slide parts: {','.join(slide_parts_to_render)}")
else:
    logger.info(
        "Will not apply slide ordering, please consider creating the file .slides_order if the slide ordering is wrong."
    )

if not arguments.present_only:
    logger.info("Rendering each slide source file:")
    for slide_part in slide_parts_to_render:
        logger.info(f"Rendering {slide_part}...")
        render_output = os.system(f"manim-slides render -aql {slide_part}")
        if render_output != 0:
            logger.critical(
                f"Looks like there was an error rendering {slide_part}! Aborting."
            )
            exit(1)
        logger.info(f"Finished rendering {slide_part}.")
else:
    logger.info("Will not render files, just present them.")
# Find out all the classes of the presentations
slide_classes = []
for presentation_file in slide_parts:
    presentation_file_full_path = os.path.join(slides_source_files, presentation_file)
    presentation_file_contents = open(presentation_file_full_path, "r").read()
    # Find the class names of all slides
    baron = RedBaron(presentation_file_contents)
    slide_classes.extend(
        [found_class.name for found_class in baron.find_all("ClassNode")]
    )
slide_classes_text = " ".join(slide_classes)

logger.info(f"Starting presentation of slide classes: {slide_classes_text}")
os.system(f"manim-slides present {slide_classes_text}")
