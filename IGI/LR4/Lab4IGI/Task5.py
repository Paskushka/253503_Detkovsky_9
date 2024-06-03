import numpy as np
import random


class CaclulateStats:
    """Class for calcualting statistics"""

    def __init__(self):
        self.matrix = None

    def calculate_statistics(self):
        """Method for calculating statistics with numpy"""
        if self.matrix is None:
            print("Matrix is empty!")
            return

        matrix_list = self.matrix.flatten().tolist()
        mean = np.mean(matrix_list)  # Ufunc (for all values)
        median = np.median(matrix_list)
        variance = np.var(matrix_list)
        stdev = np.std(matrix_list)
        return mean, median, variance, stdev


class CreateArrayMixin:
    """Mixin for creating array"""

    def create_array(self, shape, value=0):
        """Method for creating array"""
        return np.full(shape, value)  # array of certain shape and values


class MatrixOperations(CaclulateStats, CreateArrayMixin):
    """Class for matrix operations"""

    Matrix = 0  # Static attribute

    def __init__(self):
        r, c = self.input_of_data()
        self.c = c
        self.r = r
        super().__init__()
        MatrixOperations.Matrix = None

    def generate_matrix(self):
        """Method for generating matrix"""
        matrix_list = []

        for _ in range(self.c):
            row = []
            for _ in range(self.r):
                row.append(random.randint(1, 100))
            matrix_list.append(row)
            self.matrix = np.array(matrix_list)  # array()

    def swap_max_elements(self):
        """Method for swapping max elements of first and last rows"""
        if self.matrix is None:
            print("Matrix is empty!")
            return

        max_first_column = np.argmax(self.matrix[:, 0]) # Slices
        max_last_column = np.argmax(self.matrix[:, -1]) # Slices

        self.matrix[max_first_column, 0], self.matrix[max_last_column, -1] = self.matrix[max_last_column, -1], self.matrix[max_first_column, 0]

    def calculate_correlation_coefficient(self):
        """Method for calculating correlation coefficient"""
        if self.matrix is None:
            print("Matrix is empty!")
            return

        correlation_coefficient = np.corrcoef(self.matrix[:, 0], self.matrix[:, -1])[0, 1]
        return round(correlation_coefficient, 2)

    def __str__(self):  # Special method
        if self.matrix is None:
            print("Matrix is empty!")
            return

        matrix_str = ""
        for row in self.matrix:
            matrix_str += " ".join(str(cell) for cell in row) + "\n"
        return matrix_str

    def double_matrix(self):
        """Method for doubling matrix's values"""
        if self.matrix is None:
            print("Matrix is empty!")
            return
        self.matrix = np.multiply(self.matrix, 2)

    def get_first_elem(self):
        """Method for getting first elem of matrix"""
        if self.matrix is None:
            print("Matrix is empty!")
            return
        return self.matrix[0, 0]  # Indexing

    @property  # Getter
    def matrix(self):
        return self._matrix

    @matrix.setter  # Setter
    def matrix(self, value):
        self._matrix = value

    def input_of_data(self):
        """Method for input data"""
        while True:
            try:
                r = int(input("Enter amount of rows in matrix: "))
                if r > 1:
                    break
                else:
                    print("Enter int > 1")
            except ValueError:
                print("Input error!")
        while True:
            try:
                c = int(input("Enter amount of columns in matrix: "))
                if c > 1:
                    break
                else:
                    print("Enter int > 1")
            except ValueError:
                print("Input error!")

        return r, c


def main():
    """Main function for task5"""
    while True:
        matrix_operations = MatrixOperations()
        matrix_operations.generate_matrix()
        print(matrix_operations)
        mean, median, variance, stdev = matrix_operations.calculate_statistics()
        print("Mean:", mean)
        print("Median:", median)
        print("Variance:", variance)
        print("Standard Deviation:", stdev)
        coef_cor = matrix_operations.calculate_correlation_coefficient()
        print("Correlation coefficient between first and last columns:", coef_cor)
        # print(matrix_operations.get_first_elem())
        # matrix_operations.double_matrix()
        # print(matrix_operations.create_array((3,3),6))

        matrix_operations.swap_max_elements()
        print("\nMatrix after swapping max elements in the first and in the last columns:")
        print(matrix_operations)
        repeat = input("Do you want to execute program one more time? Type 'yes' if so: ")
        if repeat != 'yes':
            break


if __name__ == "__main__":
    main()