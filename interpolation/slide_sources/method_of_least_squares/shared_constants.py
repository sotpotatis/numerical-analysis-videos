"""shared_constants.py
Constants shared by both parts of the method of least squares demonstration."""

from helper_functions.point_interpolation import interpolate_over
from interpolation.shared_constants import all_evaluated_points

# Calculate the real, true, best, whatever, line of best fit solution
# over the Witch of Agnesi
# which will be used for the demonstrating examples.
(
    (c3_real, c2_real, c1_real),
    coefficient_matrix_least_squares,
    value_matrix_least_squares,
) = interpolate_over(
    all_evaluated_points,
    polynomial_degree=2,
    line_of_best_fit=True,
    return_matricies=True,
)
