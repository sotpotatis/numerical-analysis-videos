"""matrix_utilities.py
Some functions related to common operations on matricies."""

from typing import List


def transpose_matrix(entries: List[List]) -> List[List]:
    """Transposes a matrix.

    :param entries: The input individual matrix entries as a 2D list of strings [[<row 1, col 1>, <row 1, col 2>,
    <row 1, col m>],
    [<row n, col 1>, <row n, col 2>, ..., <row n, col m>]] for an n by m matrix"""
    # Transpose: one interpretation of this operation is that rows become columns in new matrix
    transposed_matrix = []
    number_of_columns = len(entries[0])
    number_of_rows = len(entries)
    for a in range(number_of_columns):
        transposed_matrix_row = []
        for b in range(number_of_rows):
            transposed_matrix_row.append(entries[b][a])
        transposed_matrix.append(transposed_matrix_row)
    return transposed_matrix
