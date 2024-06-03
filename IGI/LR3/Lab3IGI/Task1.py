# In accordance with the assignment of your option,
# create a program to calculate the value of a function using a power series expansion of the function.
import functions
import math
from decimal import Decimal
from functions import my_decorator
def function_for_task1():
    """Function for solve task1"""
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Input x and epsilon for calculating the value of a function using a power series expansion of the function")
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    while True:
        print("Enter x:")
        x = input()

        while not functions.check_is_number(x) or math.fabs(float(x)) > 1:
            print("Error, enter again: ")
            x = input()

        x = float(x)

        print("Enter epsilon:")
        eps = input()

        while not functions.check_is_number(eps):
            print("Error, enter again: ")
            eps = input()

        eps = float(eps)

        try:
            func_result, math_result, n = solve_task(x, eps)
            break
        except OverflowError:
            print("OverflowError!!!! Enter again")

    result_list = [x, n, func_result, math_result, eps]
    return result_list


@my_decorator
def solve_task(x, eps):
    """Function for calculating the value of a function using a power series expansion of the function"""
    n = 0

    math_result = math.acos(x)
    func_result = Decimal(math.pi/2)

    while n <= 500 and math.fabs(math.fabs(math_result) - math.fabs(func_result)) > eps:
        func_result -= Decimal(math.factorial(2*n))/Decimal((Decimal(math.pow(4, n)) * Decimal(math.pow(Decimal(math.factorial(n)), 2)) * Decimal((2*n+1)))) * Decimal(math.pow(x, 2*n+1))
        n += 1

    return func_result, math_result, n
