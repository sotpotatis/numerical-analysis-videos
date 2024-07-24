"""point_interpolation_tests.py
Tests some interpolation-related functions with known values."""

import logging
import os.path
import unittest
from typing import List

from interpolation.shared_constants import all_evaluated_points
from helper_functions.point_interpolation import (
    cubic_spline_interpolation,
    linear_spline_interpolation,
)

TEST_LOCATION = os.path.realpath(__file__)
TEST_DIRECTORY = os.path.dirname(TEST_LOCATION)
# We know the coefficients for cubic spline interpolation and linear spline interpolation over all_evaluated_points
# or at least we can figure out how to know it! You can use MATLAB or WolframAlpha to obtain the correct coefficients.
CUBIC_INTERPOLATION_TEST_DATA_LOCATION = os.path.join(
    TEST_DIRECTORY, "cubic_interpolation_coefficients.txt"
)
LINEAR_INTERPOLATION_TEST_DATA_LOCATION = os.path.join(
    TEST_DIRECTORY, "linear_interpolation_coefficients.txt"
)
CUBIC_INTERPOLATION_TEST_DATA = open(CUBIC_INTERPOLATION_TEST_DATA_LOCATION, "r").read()
LINEAR_INTERPOLATION_TEST_DATA = open(
    LINEAR_INTERPOLATION_TEST_DATA_LOCATION, "r"
).read()

logger = logging.getLogger(__name__)


class TestsSplines(unittest.TestCase):
    """Tests that cubic and linear spline interpolation functions work as
    expected."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points_for_test = all_evaluated_points
        # Sort points by X
        self.points_for_test.sort(key=lambda point: point[0])
        logger.debug(f"Data used for tests: {self.points_for_test}")
        logger.debug(
            f"That makes the number of datapoints to be: {len(self.points_for_test)}"
        )

    def data_to_coefficients_list(self, input_data: str) -> List[List[float]]:
        """Converts input data from a file containing the correct coefficients for a spline polynomial.
        Returns it in the format that cubic_spline_interpolation and linear_spline_interpolation uses
        """
        parsed_coefficients = []
        for row in input_data.split("\n"):
            coefficient_buffer = ""
            parsed_row_coefficients = []
            for character_index in range(len(row)):
                character = row[character_index]
                if character.isdigit() or character in ["-", "."]:
                    coefficient_buffer += character
                    character_relevant = True
                else:
                    character_relevant = False
                if len(coefficient_buffer) > 0 and (
                    not character_relevant or character_index == len(row) - 1
                ):
                    parsed_row_coefficients.append(float(coefficient_buffer))
                    coefficient_buffer = ""
            parsed_coefficients.append(parsed_row_coefficients)
        return parsed_coefficients

    def assert_coefficients_equal(
        self, list_1: List[List[float]], list_2: List[List[float]]
    ) -> None:
        """Asserts that a list of coefficients are equal by comparing them.

        :param list_1: The first list of coefficients to compare. The known correct values.

        :param list_2: The second list of coefficients to compare."""
        self.assertEqual(len(list_1), len(list_2))
        for a in range(len(list_1)):
            list_1_coefficient_set = list_1[a]
            list_2_coefficient_set = list_2[a]
            self.assertEqual(len(list_1_coefficient_set), len(list_2_coefficient_set))
            # Ensure coefficient values are equal. To the point of machine epsilon is a little ambitious,
            # but ensuring at least 10 decimals are correct.
            for b in range(len(list_1_coefficient_set)):
                self.assertAlmostEqual(
                    list_1_coefficient_set[b],
                    list_2_coefficient_set[b],
                    10,  # 10 decimals
                )

    def test_cubic_interpolation_witch_of_agnesi(self):
        """Tests that cubic interpolation works using known interpolation spline polynomial
        constants for a Witch of Agnesi function."""
        known_correct_cubic_spline_coefficients = self.data_to_coefficients_list(
            CUBIC_INTERPOLATION_TEST_DATA
        )
        logger.debug(
            f"Known correct cubic spline coefficients: {known_correct_cubic_spline_coefficients}"
        )
        all_coefficients = cubic_spline_interpolation(self.points_for_test)
        logger.debug(f"Generated cubic spline coefficients: {all_coefficients}")
        self.assert_coefficients_equal(
            known_correct_cubic_spline_coefficients, all_coefficients
        )

    def test_linear_interpolation_witch_of_agnesi(self):
        """Tests that linear interpolation works using known interpolation spline polynomial
        constants for a Witch of Agnesi function."""
        known_correct_linear_spline_coefficients = self.data_to_coefficients_list(
            LINEAR_INTERPOLATION_TEST_DATA
        )
        logger.debug(
            f"Known correct linear spline coefficients: {known_correct_linear_spline_coefficients}"
        )
        linear_spline_coefficients = linear_spline_interpolation(self.points_for_test)
        logger.debug(
            f"Generated linear spline coefficients: {linear_spline_coefficients}"
        )
        self.assert_coefficients_equal(
            known_correct_linear_spline_coefficients, linear_spline_coefficients
        )
