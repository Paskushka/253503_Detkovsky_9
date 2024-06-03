# In accordance with the assignment of your option,
# create a program to find the sum of a sequence of numbers.
import functions


def function_for_task2():
    """Function for solve task2"""
    values = []
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Input sequence of integers and program will find average of even numbers")
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Enter gen to generate numbers automatically or anything for your personal input")
    string = input()
    if string == "gen":
        values = functions.random_integer()
        print(values)
    else:
        print("Input integers, to stop input 0")
        while True:
            n = input()

            if not functions.check_is_integer(n):
                continue

            n = int(n)

            if n == 0:
                break

            values.append(n)

    return integer_sum(values)


def integer_sum(values):
    """Function for to calculate the arithmetic mean of even numbers"""
    sum = 0
    counter = 0
    for i in values:
        if i % 2 == 0:
            sum += i
            counter += 1
    try:
        return sum/counter
    except ZeroDivisionError:
        return "Division by zero"
