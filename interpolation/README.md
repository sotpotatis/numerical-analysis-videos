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

`manim-slides render interpolation/all_slides.py IntroductionSlide InterpolationExample Splines -ql`
