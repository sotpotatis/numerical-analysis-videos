"""graphs.py
Contains helper functions for displaying graphs."""

import logging
from typing import Callable, Optional, List, Tuple, Union

from manim import (
    Axes,
    ThreeDAxes,
    PI,
    Text,
    ParametricFunction,
    RED,
    Create,
    GRAY,
    Dot3D,
    Dot,
    UP,
    VGroup,
    NumberPlane,
    Mobject,
    ReplacementTransform,
)
from numpy._typing import NDArray
from sympy import Symbol, lambdify
from manim_slides.slide import ThreeDSlide

# Symbol quick access
from helper_functions.general_utilities import play_multiple

SYMBOL_X = Symbol("x")
SYMBOL_Y = Symbol("y")
SYMBOL_Z = Symbol("z")
COMMON_SYMBOLS = [SYMBOL_X, SYMBOL_Y, SYMBOL_Z]

DEFAULT_AXES_INTERVALS = [[-10, 10, 1]] * 3
AXIS_CONFIG_INCLUDE_NUMBERS = {"include_numbers": True}
AXIS_CONFIG_NO_TIPS = {"include_tip": False}
X_AXIS_LENGTH = 20
Y_AXIS_LENGTH = 12
Z_AXIS_LENGTH = 12
logging.basicConfig(level=logging.DEBUG)


class AxesAndGraphHelper:
    """A graph with axis and the possibility to add plots,
    vectors and points.

    Both 2D and 3D possible."""

    def __init__(
        self,
        scene_reference: ThreeDSlide,
        interval: Optional[List[List[int]]] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        z_label: Optional[str] = None,
        phi: Optional[int] = None,
        theta: Optional[int] = None,
        gamma: Optional[int] = None,
        is_r2: Optional[bool] = None,
        use_2d_axes_class: Optional[bool] = None,
    ) -> None:
        """Creates a graph based on a function.


        :param scene_reference: Reference to the scene the graph should be displayed in.

        :param interval: What interval to render over. In the format [[x_int_start, x_int_end], ..., [z_int_start, z_int_end]]

        :param x_label: Label for the x-axis.

        :param y_label: Label for the y-axis.

        :param z_label: Label for the z-axis.

        :param phi: Control the rotation of the coordinate system. This variable controls the phi value.

        :param theta: Control the rotation of the coordinate system. This variable controls the theta value.

        :param gamma: Control the rotation of the coordinate system. This variable controls the gamma value.

        :param is_r2: Whether the plot is 2D or not. If 2D, the z-axis will be hidden.

        :param use_2d_axes_class: Forces the axes to 2D by using Axes() instead of ThreeDAxes().
        Note that this removes all the features related to plotting and animating in 3D!! But what it comes with is that
        you can use it with 2D scenes.
        """
        if phi is None:
            phi = 0
        if theta is None:
            theta = -PI / 2
        if gamma is None:
            gamma = 0
        if interval is None:
            interval = DEFAULT_AXES_INTERVALS
        if use_2d_axes_class is None:
            use_2d_axes_class = False
        # Save all passed arguments to self
        self.scene_reference = scene_reference
        self.interval = interval
        self.x_label = x_label
        self.y_label = y_label
        self.z_label = z_label
        self.phi = phi
        self.theta = theta
        self.gamma = gamma
        self.is_r2 = is_r2
        self.use_2d_axes_class = use_2d_axes_class
        self.rendered_functions = []
        self.added_points = []
        self.axes_and_functions = None
        self.logger = logging.getLogger(__name__)
        self.create_axes(interval, x_label, y_label, z_label, is_r2, zoom=0.5)
        # Set camera orientation
        self.scene_reference.move_camera(phi=phi, theta=theta, gamma=gamma)

    def create_axes(
        self,
        interval,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        z_label: Optional[str] = None,
        is_r2: Optional[bool] = None,
        zoom: Optional[float] = None,
        include_number_plane: Optional[bool] = None,
    ) -> None:
        """Creates axes given configuration parameters.


        :param interval: What interval to render over. In the format [[x_int_start, x_int_end], ..., [z_int_start, z_int_end]]

        :param x_label: Label for the x-axis.

        :param y_label: Label for the y-axis.

        :param z_label: Label for the z-axis.

        :param is_r2: Whether the plot is 2D or not. If 2D, the z-axis will be hidden. Defaults to True if unset.

        :param zoom: Set the graph camera zoom if you'd like.

        :param include_number_plane: Whether to draw a number plane or not. Defaults to True if unset.
        """
        self.logger.debug(
            f"Creating axes... Rerendering {len(self.rendered_functions)} functions, moving {len(self.added_points)} points."
        )
        if is_r2 is None:
            is_r2 = True
        if x_label is None:
            x_label = "x"
        if y_label is None:
            y_label = "y"
        if z_label is None:
            z_label = "z"
        if include_number_plane is None:
            include_number_plane = True
        # Start by zooming out to avoid "choppy" effect
        if zoom is not None:
            self.scene_reference.set_camera_orientation(zoom=zoom)
        # Create Manim axes
        if len(interval) == 3:
            x_interval, y_interval, z_interval = interval
        else:
            x_interval, y_interval = interval
            z_interval = None
        axes_config_kwargs = {
            "z_axis_config": (
                AXIS_CONFIG_NO_TIPS if is_r2 else AXIS_CONFIG_INCLUDE_NUMBERS
            ),
            "y_axis_config": AXIS_CONFIG_INCLUDE_NUMBERS,
            "x_axis_config": AXIS_CONFIG_INCLUDE_NUMBERS,
            # Note: previously I auto-genereated the axis length as commented out below,
            # but I figured fixing the axis length and letting Manim position the coordinates
            # automatically worked better
            # It is somewhat hacky as the number are set up for my computer - but again - it works
            "x_length": X_AXIS_LENGTH,  # abs(x_interval[1] - x_interval[0]),
            "y_length": Y_AXIS_LENGTH,  # abs(y_interval[1] - y_interval[0]),
            "z_length": (
                0 if is_r2 else Z_AXIS_LENGTH
            ),  # abs(z_interval[1] - z_interval[0]),
            "x_range": x_interval,
            "y_range": y_interval,
            "z_range": (
                [0, 0.1, 1] if is_r2 else z_interval
            ),  # Suuuper hacky but it works!
        }
        axes_label_kwargs = {
            "x_label": Text(x_label),
            "y_label": Text(y_label),
            "z_label": Text(z_label),
        }
        if not self.use_2d_axes_class:
            self.axes_object = ThreeDAxes(**axes_config_kwargs)
        else:
            # Remove kwargs related to R^3
            del axes_config_kwargs["z_range"]
            del axes_config_kwargs["z_axis_config"]
            del axes_config_kwargs["z_length"]
            del axes_label_kwargs["z_label"]
            self.axes_object = Axes(**axes_config_kwargs)
        # Add labels
        self.labels = self.axes_object.get_axis_labels(**axes_label_kwargs)
        # If axes has been rendered already (function is being called to rescale axes)
        new_axes_and_labels = VGroup(self.axes_object, self.labels)
        if self.axes_and_functions is not None:
            self.logger.debug("Animating transformation of old axes...")
            # Animate transform and remove old axes and functions
            self.scene_reference.play(
                ReplacementTransform(self.axes_and_functions, new_axes_and_labels)
            )
        else:
            self.logger.debug(
                "Axes were created for the first time. Will render creation of axes and labels."
            )
            self.scene_reference.play(Create(new_axes_and_labels))
            self.scene_reference.add(self.axes_object, self.labels)
            self.logger.debug("Rendered creation of axes and labels.")
        # Add number plane if user wants
        if include_number_plane:
            # Number plane should have same config as axes but not show numbers
            # (so we remove that part of the configuration)
            number_plane_config_kwargs = axes_config_kwargs.copy()
            del number_plane_config_kwargs["x_axis_config"]
            del number_plane_config_kwargs["y_axis_config"]
            if "z_axis_config" in number_plane_config_kwargs:
                del number_plane_config_kwargs["z_axis_config"]
            if "z_length" in number_plane_config_kwargs:
                del number_plane_config_kwargs["z_length"]
            if "z_range" in number_plane_config_kwargs:
                del number_plane_config_kwargs["z_range"]
            number_plane = NumberPlane(**number_plane_config_kwargs)
            # If an old number plane has been added, redraw it.
            if hasattr(self, "number_plane"):
                self.logger.debug("Animation transformation of number plane...")
                self.scene_reference.play(
                    ReplacementTransform(self.number_plane, number_plane)
                )
            else:
                self.logger.debug(
                    "Number plane was created for the first time. Will render creation of it."
                )
                self.scene_reference.play(Create(number_plane))
            self.number_plane = number_plane
        self.axes_and_functions = new_axes_and_labels
        # Manim does not by default rescale and move created dots and objects as far as I know if you change the
        # axes length. So if the axes length is changed we need to manually redraw / move any previously created objects
        # here.
        # Recreate previously plotted functions
        functions_to_rerender = self.rendered_functions.copy()
        for rendered_function, function_kwargs in functions_to_rerender:
            self.logger.debug(f"Adding previously rendered function {function_kwargs}")
            self.plot_function(**function_kwargs)
            self.scene_reference.remove(rendered_function)
        # Recreate previously plotted points
        points_to_rerender = self.added_points.copy()
        for point_object, text_object, point_kwargs in points_to_rerender:
            self.logger.debug(f"Adding previously rendered point {point_kwargs}")
            self.add_point(animation_run_time=0, **point_kwargs)
            self.scene_reference.remove(point_object)
            if text_object is not None:
                self.scene_reference.remove(text_object)

    def plot_function(
        self,
        graph_function: Union[Callable, Tuple],
        input_variables: List[Symbol],
        range_to_use_for_function: Optional[List[int]] = None,
        plot_color: Optional[int] = None,
        add_function_plot_to_scene: Optional[bool] = None,
        animate: Optional[bool] = None,
    ) -> ParametricFunction:
        """Plots a function on the axes.

        :param graph_function: A function to use for displaying the graph.
        For example, for the function z(x,y)=x^2+y^2, pass SYMBOL_X^2+SYMBOL_Y^2

        :param graph_function_variables: The variables that the function to display takes as input.
        For example, for the function z(x,y)=x^2+y^2, pass [SYMBOL_X, SYMBOL_Y]

        :param range_to_use_for_function: If your function takes two or more inputs, you need to define the range manually here.
        In the format [range_start, range_end].
        For example, for a function z(y,t)=(yt)^2 that should be plotted on a t interval, pass the t interval here.

        :param plot_color: The color to plot the graph with.

        :param add_function_plot_to_scene: If True, adds and shows the creation of the function plot.
        Defaults to True.
        WARNING: Setting to False will remove a reference to the function plot from self.rendered_functions-
        This will imply that the function will be lost if you rescale the axes and needs to be removed from the plot manually.

        :param animate: If True, will render the addition of the plot to the scene using the Create() animation.
        If False, will instead use the .add() function.
        """
        if plot_color is None:
            plot_color = RED
        if add_function_plot_to_scene is None:
            add_function_plot_to_scene = True
        if animate is None:
            animate = True
        graph_lambda_function = lambdify(input_variables, graph_function, "numpy")

        def parsed_graph_function(*args) -> NDArray[float]:
            return self.axes_object.coords_to_point(*graph_lambda_function(*args))

        if range_to_use_for_function is not None:
            parsed_function_interval = range_to_use_for_function
        elif len(input_variables) == 1 and input_variables[0] in COMMON_SYMBOLS:
            parsed_function_interval = self.interval[
                COMMON_SYMBOLS.index(input_variables[0])
            ]
        else:
            raise ValueError(
                """If your function takes two or more inputs or uses an uncommon input variable (not X,Y,Z),
             you need to define the range manually under range_to_use_for_function."""
            )
        # Plot function
        function_plot = ParametricFunction(
            function=parsed_graph_function, t_range=parsed_function_interval
        )
        function_plot.set_color(plot_color)
        if add_function_plot_to_scene:
            self.rendered_functions.append(
                (
                    function_plot,
                    {  # Save kwargs passed to this function
                        "graph_function": graph_function,
                        "input_variables": input_variables,
                        "range_to_use_for_function": range_to_use_for_function,
                        "plot_color": plot_color,
                    },
                )
            )
            self.axes_object.add(function_plot)
            if animate:
                self.scene_reference.play(Create(function_plot))
            else:
                self.scene_reference.add(function_plot)
        return function_plot

    def add_point(
        self,
        coordinates: List[int],
        show_coordinates: Optional[int] = None,
        coordinate_display_location: Optional = None,
        dot_color: Optional[int] = None,
        show_z_coordinate: Optional[bool] = None,
        round_coordinates_to_decimals: Optional[int] = None,
        animation_run_time: Optional[float] = None,
        return_created_objects: Optional[bool] = None,
    ) -> Union[None, List[Mobject]]:
        """Adds a point to the graph and shows it.

        :param coordinates: The coordinates for the dot.

        :param show_coordinates: If True, the coordinates will be indicated by showing them next to the point.

        :param coordinate_display_location: If show_coordinates=True, changes where the coordinates are displayed relative to the point.
        Default is UP.

        :param dot_color: The color of the dot. Default is GRAY.

        :param show_z_coordinate: Whether to show the z coordinate or not if show_coordinates=True. Default is False.

        :param round_coordinates_to_decimals: Optionally round the given coordinates in the display (if show_coordinates=True) to this many decimals.

        :param animation_run_time: How long to animate the addition of the point. If 0, no animation will be shown.

        :param return_created_objects: If True, will return a list of created objects. If False (default), will return None
        """
        # Set z coordinate to 0 if a z coordinate is not passed and we're using 3D
        if len(coordinates) < 3 and not self.use_2d_axes_class:
            coordinates.append(0)
        if dot_color is None:
            dot_color = GRAY
        if show_coordinates is None:
            show_coordinates = False
        if coordinate_display_location is None:
            coordinate_display_location = UP
        if show_z_coordinate is None:
            show_z_coordinate = True
        if animation_run_time is None:
            animation_run_time = 0.5
        if return_created_objects is None:
            return_created_objects = False
        point_base_class = Dot3D if not self.use_2d_axes_class else Dot
        point = point_base_class(
            point=self.axes_object.coords_to_point(*coordinates), color=dot_color
        )
        added_objects = [point]
        # Add coordinate display if enabled
        coordinate_display = None
        if show_coordinates:
            coordinate_text = "("
            for coordinate in coordinates[: (-1 if show_z_coordinate else -2)]:
                coordinate_value = coordinate
                if round_coordinates_to_decimals is not None:
                    coordinate_value = round(
                        coordinate_value, round_coordinates_to_decimals
                    )
                coordinate_text += f"{coordinate_value},"
            coordinate_text = (
                coordinate_text[:-1] + ")"
            )  # [:-1] to remove trailing comma
            coordinate_display = Text(coordinate_text)
            coordinate_display.scale(0.5)
            coordinate_display.next_to(point, coordinate_display_location)
            added_objects.append(coordinate_display)
        # Save point and kwargs
        self.added_points.append(
            (
                point,
                coordinate_display,
                {
                    "coordinates": coordinates,
                    "show_coordinates": show_coordinates,
                    "coordinate_display_location": coordinate_display_location,
                    "dot_color": dot_color,
                    "show_z_coordinate": show_z_coordinate,
                    "round_coordinates_to_decimals": round_coordinates_to_decimals,
                },
            )
        )
        if animation_run_time > 0:
            play_multiple(
                self.scene_reference, added_objects, Create, run_time=animation_run_time
            )
        else:
            self.scene_reference.add(*added_objects)
        if return_created_objects:
            return added_objects

    def plot_line(self, coordinate: float, vertical: Optional[bool] = None) -> None:
        """Plot a line, either horizontal or vertical. The line will cover the whole axes.

        :param coordinate: The y coordinate to put the line at if vertical=False.
        Otherwise, the x coordinate to put it on.

        :param vertical: If True, will generate a vertical line. If False, it will be horizontal.
        Default is True."""
        if vertical is None:
            vertical = True
        # Get the relevant range and function depending on the provided coordinates
        if vertical:
            range_to_plot = self.axes_object.y_range
            graph_function = (coordinate, SYMBOL_Y, 0)
        else:
            range_to_plot = self.axes_object.x_range
            graph_function = (SYMBOL_X, coordinate, 0)
        self.plot_function(
            graph_function=graph_function,
            input_variables=[SYMBOL_X],
            range_to_use_for_function=range_to_plot,
        )
