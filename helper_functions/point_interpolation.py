"""point_interpolation.py
Helper functions for fitting a polynomial to a set of points.
"""

import logging

from numpy._typing import NDArray
from sympy import Symbol
from typing import List, Tuple, Optional, Union
from numpy.linalg import solve
from numpy import transpose, matmul

logger = logging.getLogger(__name__)


def interpolate_over(
    points: List[List[Union[int, float]]],
    polynomial_degree: Optional[int] = None,
    line_of_best_fit: Optional[bool] = None,
    return_matricies: Optional[bool] = None,
    center_around_point: Optional[float] = None,
) -> Union[List[float], Tuple[List[float], NDArray, NDArray]]:
    """Generates interpolation polynomial coefficients for a set of points.
    The function will generate a polynomial of degree i-1 if i is the number of given points, unless the degree is set.

    :param points: A list of points to interpolate over.

    :param polynomial_degree: Optionally set the degree of the interpolating polynomial manually. NOTE: If you set the parameter to an interval where it requires
    a line of best fit, you must set line_of_best_fit=True. This is to acknowledge you understand that line of best fit is being used.

    :param line_of_best_fit: Set to True to acknowledge that you're interpolating using line of best fit, polynomial_degree<i-1 where i is the number of given points


    :param return_matricies If True, also returns the A matrix and the b matrix (in the format Ax=b) that lies out the equations for solving for the coefficients

    :param center_around_point: If not None, calculate a centering polynomial around the given point. This can speed up calculation times.

    :returns The set of polynomial coefficients, in order lowest (x^0) to highest(x^(i-1)) . If return_matricies is True, also returns the A matrix and the b matrix
    (in the format Ax=b) that lies out the equations for solving for the coefficients
    """
    if polynomial_degree is None:
        polynomial_degree = len(points) - 1
    if line_of_best_fit is None:
        line_of_best_fit = False
    if return_matricies is None:
        return_matricies = False
    if polynomial_degree < len(points) - 1 and not line_of_best_fit:
        raise ValueError(
            """"You've set a polynomial degree that requires a line of best fit 
        to be calculated but has not acknowledged that a line of best fit is to be used. To do this, please set line_of_best_fit=True as an 
        argument to interpolate_over."""
        )
    # Generate equation system
    coefficient_matrix = []
    value_matrix = []
    for a in range(len(points)):
        # Get the output and input that was passed to original function
        input_value, output_value = points[a]
        value_matrix.append(output_value)
        coefficient_matrix_row = [1]
        for b in range(1, polynomial_degree + 1):
            # Perform centering if set
            if center_around_point is not None:
                coefficient_matrix_value = input_value - center_around_point
            else:
                coefficient_matrix_value = input_value
            coefficient_matrix_row.append(coefficient_matrix_value**b)
        coefficient_matrix.append(coefficient_matrix_row)
    # Multiply both sides by coefficient_matrix^T if needed
    if line_of_best_fit:
        value_matrix = matmul(transpose(coefficient_matrix), value_matrix)
        coefficient_matrix = matmul(transpose(coefficient_matrix), coefficient_matrix)
    logger.debug(
        f"""
        Performing degree {polynomial_degree} interpolation with coefficient matrix: {coefficient_matrix}, 
        value matrix: {value_matrix}"""
    )
    solutions = solve(coefficient_matrix, value_matrix)
    if not return_matricies:
        return solutions
    else:
        return solutions, coefficient_matrix, value_matrix


def interpolation_coefficients_to_function_template(
    interpolation_coefficients: List[float],
    input_variable: Symbol,
    center_around_point: Optional[float] = None,
) -> Tuple[Symbol, callable, float]:
    """Converts a list of interpolation coefficients to a tuple that can be used to create a lambda function returning the value of the
    interpolation polynomial at a certain point.

    :param interpolation_coefficients: Coefficients of the polynomial in the same format as interpolate_over (order lowest --> highest)

    :param input_variable The Sympy input variable/symbol.

    :param center_around_point: If set, specifies a point towards which the polynomial is centered.

    :returns Call the generated interpolation polynomial f, a function of <variable>, then the output is
    (<variable>, f(<variable>), 0)"""
    result = 0
    for i in range(len(interpolation_coefficients)):
        interpolation_coefficient = interpolation_coefficients[i]
        if center_around_point is not None:
            function_expression = input_variable - center_around_point
        else:
            function_expression = input_variable
        result += interpolation_coefficient * (function_expression**i)
    return (input_variable, result, 0)


def linear_spline_interpolation(points: List[List[float]]) -> List[List[float]]:
    """Perform linear spline interpolation over a given list of points.

    :param points: The points to perform spline interpolation over.

    :returns A list of the coefficients for each interpolation polynomial that was generated.
    """
    all_coefficients = []
    for i in range(len(points) - 1):
        points_to_interpolate = points[i : i + 2]
        logger.debug(
            f"""
           Performing linear spline interpolation over points: {points_to_interpolate}."""
        )
        all_coefficients.append(interpolate_over(points_to_interpolate))
    return all_coefficients


def three_point_cubic_spline_interpolation(
    points: List[List[float]],
) -> List[List[float]]:
    """Perform cubic spline interpolation over 3 points (aka generates 2 interpolation polynomials).

    :param points: The number of points to generate a spline interpolation polynomial between.
    Must be exactly 3 points.

    :returns Coefficients in order lowest to highest (x^0)-->(x^3)
    """
    # Set up the equation system
    # The algorithm
    coefficient_matrix: List[List[float]] = []
    value_matrix: List[float] = []
    if len(points) != 3:
        raise ValueError(
            "Please pass exactly 3 points to the cubic spline interpolation function."
        )
    for i in range(2):
        relevant_points = points[i : i + 2]
        logger.debug(f"Adding coefficients for relevant points {relevant_points}")
        # Separate relevant point in x and y
        relevant_x = [relevant_point[0] for relevant_point in relevant_points]
        relevant_y = [relevant_point[1] for relevant_point in relevant_points]
        # Ensure polynomials pass over all points
        for x_variable in relevant_x:
            coefficient_multipliers_to_append = [
                x_variable**3,
                x_variable**2,
                x_variable,
                1,
            ]
            # Either pad start or end of coefficient matrix with zeros depending on number of equation
            # The first iteration (i=0) will be for the first two points on the interval.
            if i == 0:
                coefficient_multipliers_to_append.extend([0] * 4)
            else:
                coefficient_multipliers_to_append = [
                    0
                ] * 4 + coefficient_multipliers_to_append
            coefficient_matrix.append(coefficient_multipliers_to_append)
        value_matrix.extend(relevant_y)
    # Ensure derivatives are equal at the middle point. A little hacky but more intuitive imo to do it manually
    middle_x, _ = points[1]
    equal_derivatives_list = [3 * (middle_x**2), 2 * middle_x, 1, 0]
    # equal_derivatives_list should be [3 * middle_x ** 2, 2 * middle_x, 1, 0, -3 * middle_x ** 2, -2 * middle_x, -1, 0]
    # Hence we do it as below
    equal_derivatives_list.extend([-1 * element for element in equal_derivatives_list])
    logger.debug(f"Equal derivatives list: {equal_derivatives_list}")
    coefficient_matrix.append(equal_derivatives_list)
    value_matrix.append(0)
    # Ensure second derivatives are equal
    # Same story as for equal_derivatives_list, that's why the formatting is as below
    equal_second_derivatives_list = [6 * middle_x, 2, 0, 0]
    equal_second_derivatives_list.extend(
        [-1 * element for element in equal_second_derivatives_list]
    )
    logger.debug(f"Equal second derivatives list: {equal_second_derivatives_list}")
    coefficient_matrix.append(equal_second_derivatives_list)
    value_matrix.append(0)
    # Ensure second derivatives are 0 at endpoints (natural cubic spline)
    coefficient_matrix.append([6 * points[0][0], 2] + [0] * 6)
    coefficient_matrix.append([0] * 4 + [6 * points[2][0], 2] + [0] * 2)
    value_matrix.extend([0] * 2)
    logger.debug(
        f"""
    Performing cubic spline interpolation with coefficient matrix: {coefficient_matrix}, value matrix: {value_matrix}"""
    )
    # Return coefficients
    solution = solve(coefficient_matrix, value_matrix)
    # Reverse coefficients to return them in order lowest --> highest
    # The other parts of the code uses that ordering, I know it's not ideal to reverse after the coefficients have been calculated.
    logger.debug(f"Solution to cubic spline interpolation: {solution}")
    polynomial_1_coefficients = solution[:4][::-1]
    polynomial_2_coefficients = solution[4:][::-1]
    return [polynomial_1_coefficients, polynomial_2_coefficients]


def cubic_spline_interpolation(
    points: List[List[Union[float, int]]]
) -> List[List[Union[float, int]]]:
    """Perform cubic spline interpolation over a set of points.

    :param points: The set of points to iterate over.
    """
    all_coefficients = []
    for i in range(0, len(points) - 2, 2):
        points_to_interpolate_over = points[i : i + 3]
        logger.debug(
            f"Performing cubic spline interpolation over points: {points_to_interpolate_over}..."
        )
        generated_coefficients = three_point_cubic_spline_interpolation(
            points_to_interpolate_over
        )
        logger.debug(f"Generated cubic spline coefficients: {generated_coefficients}.")
        all_coefficients.extend(generated_coefficients)
        logger.debug(
            f"Generated cubic spline coefficients for interation {i}: {generated_coefficients}"
        )
    return all_coefficients
