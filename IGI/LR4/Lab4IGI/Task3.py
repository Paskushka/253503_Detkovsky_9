import math
import numpy as np
import matplotlib.pyplot as plt
import statistics
import math
from decimal import Decimal

class Lab3Approx:
    """Class for approximating"""

    def __init__(self, x, eps=1e-5, max_iterations=500):
        self.x = x
        self.eps = eps
        self.max_iterations = max_iterations

    def calculate_arccos_approximation(self, x):
        """Method for approximating func and for math result"""
        n = 0

        math_result = math.acos(x)
        func_result = math.pi / 2

        while n <= self.max_iterations and math.fabs(math.fabs(math_result) - math.fabs(func_result)) > self.eps:
            func_result -= math.factorial(2 * n) / (math.pow(4, n) * math.pow(math.factorial(n), 2) * (2 * n + 1)) * math.pow(
                x, 2 * n + 1)
            n += 1

        return func_result, n, math_result


class StatMixin:
    """Mixin for getting statistics"""

    Mean = 0

    def calculate_statistics(self, results):
        """Method for calculating statistics"""
        Mean = statistics.mean(results)
        median = statistics.median(results)
        mode = statistics.mode(results)
        variance = statistics.variance(results)
        stdev = statistics.stdev(results)
        return Mean, median, mode, variance, stdev


class LnApproximation(Lab3Approx, StatMixin):
    """Class ln approximation and drawing plot"""

    def __init__(self, x, eps=1e-10, max_iterations=500):
        super().__init__(x, eps, max_iterations)
        self.results = []  # List for saving all results

    def plot_approximation(self):
        """Method for drawing plot"""
        x_values = np.linspace(-0.99, 0.99, 100)
        y_values = np.arccos(x_values)
        approx_values_x = []
        approx_values_y = []

        for i in x_values:
            approx_values_x.append(i)
            result = self.calculate_arccos_approximation(i)
            approx_values_y.append(result[0])

        plt.plot(approx_values_x, y_values, label="math")
        plt.plot(approx_values_x, approx_values_y, label="my_func")
        plt.scatter(self.x, np.arccos(self.x), color='red', label='x')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.savefig('C:/Users/Lenovo/PycharmProjects/Lab4IGI/plot.png')  # Save to file
        plt.title('Approximation of arccos(x)')
        plt.show()
        self.results = approx_values_y

    def calculate_statistics_method(self):
        """Method for calculating statistics"""
        return self.calculate_statistics(self.results)
    @property  # Getter for x
    def x(self):
        return self._x

    @x.setter  # Setter for x
    def x(self, value):
        self._x = value

    def print_table(self, x, n, result, math_result, eps):
        """Method for printing table"""
        print("|   x   |   n   |   F(x)    |   Math F(x)    |   eps   |")
        print("-" * 56)
        print(f"| {x:.3f} | {n:5d} | {result:.6f} | {math_result:.11f} | {eps:.1e} |")

    def __str__(self):  # Special method
        return self.results


def input_of_data():
    """Method for input data"""
    while True:
        try:
            x = float(input("Enter x (-1 , 1): "))
            if -1 < x < 1 or x == 0:
                break
            else:
                print("INPUT ERROR")
        except ValueError:
            print("ERROR! Please enter a float number")
    while True:
        try:
            eps = float(input("Enter eps (precision): "))
            if eps > 0:
                break
            else:
                print("ERROR! Must be non negative")
        except ValueError:
            print("Error! Please enter a number")
    return x, eps


def main():
    """Main function for task3"""
    while True:
        print("Approximate arccos(x) with Taylor series:")
        while True:
            x, eps = input_of_data()
            if eps >= 0.01:
                break
            else:
                print("Enter eps => 0.01")
        approx = LnApproximation(x, eps)
        result, n, math_result = approx.calculate_arccos_approximation(x)
        approx.print_table(x, n, result, math_result, eps)
        approx.plot_approximation()
        mean, median, mode, variance, stdev = approx.calculate_statistics_method()
        print("Mean:", mean)
        print("Median:", median)
        print("Mode:", mode)
        print("Variance:", variance)
        print("Standard Deviation:", stdev)
        repeat = input("Do you want to execute program one more time? Type 'yes' if so: ")
        if repeat != 'yes':
            break


if __name__ == "__main__":
    main()