# Interpolation video

This tutorial video aims to explain interpolation.

## Order of scenes

Each file in `slide_sources/` contains one class which will provide either one or multiple different slides.
The order that they should appear from first to last:

* Slides from introduction.py
* Slides from interpolation_example.py
* Slides from splines.py
* Slides from error_calculation_demonstration.py


## Rendering video

If you want to render and present all slides, assuming you are in the root directory of the repository:

(the commands are shown in no particular order)

* `manim-slides render interpolation/slide_sources/overview.py`
* `manim-slides render interpolation/slide_sources/introduction.py`
* `manim-slides render interpolation/slide_sources/centering.py`
* `manim-slides render interpolation/slide_sources/splines.py`
* `manim-slides render interpolation/slide_sources/error_calculation_demonstration.py`
* `manim-slides render interpolation/slide_sources/interpolation_example_and_runges_phenomenon.py`
* `manim-slides render interpolation/slide_sources/method_of_least_squares/part_1.py`
* `manim-slides render interpolation/slide_sources/method_of_least_squares/part_2.py`

## Presenting the result

The command to show and present the result of all the slides can be found in `command_to_present_all_slides`

## Slides in HTML

See the directory `interpolation_slides_html` to find the slides in HTML format.
**Please note that this directory is not connected to any fancy thing like GitHub Actions or similar, and thus it is most likely not the most recent!**