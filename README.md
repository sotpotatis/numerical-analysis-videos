# Numerical Analysis videos

This repository contains the source code for a series of Swedish videos about Numerical Analysis.
The videos are animated in [Manim](https://docs.manim.community/en/stable/index.html) (Community Edition),
using the add-on [Manim Slides](https://manim-slides.eertmans.be/latest/).

## Installing
Run 
`pip install -r "requirements.txt"`.
You might have to install [Manim Slides](https://manim-slides.eertmans.be/latest/) with a flag specifying your desired rendering environment.
Refer to their documentaiton for that.

## Running the videos

The videos are meant to be played using Manim-slides since that is the tool they are written in.

For example, to *render* the interpolation polynomial video, given that you are in the directory containing interpolation polynomials tutorial:


`manim-slides render interpolation.py InterpolationVideo`

And to *present* it:

`manim-slides InterpolationVideo`

Note: If you're using PySide6 and get the error Static surface pool size exceeded, try:

`manim-slides InterpolationVideo --hide-info-window`

It might still spit out error messages but should work.