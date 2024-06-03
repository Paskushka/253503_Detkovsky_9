import matplotlib.pyplot as plt
import numpy as np
import math
from abc import ABC, abstractmethod


class GeometricalFigure(ABC):
    """Abstract Class of figure"""

    @abstractmethod
    def calculate_area(self):
        """Abstract method for calculating figures area"""
        pass


class Color:
    """Class of color"""

    def __init__(self, color):
        self.color = color

    @property  # Getter
    def color(self):
        return self._color

    @color.setter  # Setter
    def color(self, value):
        self._color = value


class ValidateMixin:
    """Mixin for validating color"""

    @staticmethod
    def validate_color(color):
        allowed_colors = ["red", "green", "blue", "black"]
        return color.lower() in allowed_colors


class Polygon(GeometricalFigure, ValidateMixin):
    """Class of polygon"""
    figure_name = "Polygon"

    def __init__(self, sides, side_length, color):
        self.sides = sides
        self.side_length = side_length
        self.color = Color(color)

    def calculate_area(self):
        """Method for calculating figures area"""
        apothem = self.side_length / (2 * math.tan(math.pi / self.sides))
        area = (self.sides * self.side_length * apothem) / 2
        return area

    def plot_shape(self, label_text):
        """Method for drawing figure"""
        plt.figure()

        angles = np.linspace(0, 2 * math.pi, self.sides + 1)  # Angles for each vertex
        x = self.side_length * np.cos(angles)  # X-coordinates of vertices
        y = self.side_length * np.sin(angles)  # Y-coordinates of vertices

        plt.plot(x, y, color=self.color.color)
        plt.fill(x, y, color=self.color.color, alpha=0.3)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(label_text)
        plt.grid(True)
        plt.savefig('C:/Users/Lenovo/PycharmProjects/Lab4IGI/plot2.png')  # Save to file
        plt.show()

    def __str__(self):  # Special method
        return "{} with {}, sides={}, side_length={}".format(
            self.figure_name, self.color.color, self.sides, self.side_length
        )


def input_data():
    while True:
        try:
            sides = int(input("Enter the number of sides of the polygon: "))
            if sides < 3:
                raise ValueError("Number of sides must be greater than or equal to 3.")
            side_length = float(input("Enter the length of each side of the polygon: "))
            if side_length <= 0:
                raise ValueError("Side length must be greater than zero.")
            color = input("Enter the color of the polygon (red, green, blue, black): ")
            if not Polygon.validate_color(color):
                raise ValueError("Invalid color format or name.")
            return sides, side_length, color
        except ValueError as ve:
            print(f"ERROR! {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def main():
    """Main function for task4"""
    while True:
        sides, side_length, color = input_data()
        label_text = input("Enter text label for the polygon: ")
        polygon = Polygon(sides, side_length, color)
        area = polygon.calculate_area()
        print(f"Area of the {polygon.figure_name}: {area:.2f} square units.")
        print(polygon)
        polygon.plot_shape(label_text)
        repeat = input("Do you want to execute the program one more time? Type 'yes' if so: ")
        if repeat.lower() != 'yes':
            break


if __name__ == "__main__":
    main()