# In accordance with the instructions of your option, create a program for processing real lists.
import functions


def function_for_task5():
    """Function for solve task5"""
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Input list of float numbers and funcrion will find the product of negative list elements and the sum of positive list elements located up to the maximum element")
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Enter gen to generate numbers automatically or anything for your personal input")
    string = input()
    if string == "gen":
        numbers = functions.random_float()
        print(numbers)
    else:
        numbers = input_list()
    max_index = numbers.index(max(numbers))
    negative_product, positive_sum = solve_task(numbers, max_index)
    return f"Product of negative numbers: {negative_product} \nSum of positive numbers: {positive_sum}"


def solve_task(numbers, max_index):
    """Function for find Product of negative numbers and sum of positive numbers"""
    negative_product = 1
    positive_sum = 0
    temp = False
    for i in range(max_index):
        if numbers[i] < 0:
            temp = True
            negative_product *= numbers[i]
        elif numbers[i] > 0:
            positive_sum += numbers[i]
    if not temp:
        negative_product = 0
    return negative_product, positive_sum


def input_list():
    """Function fot input list"""
    numbers = []
    print("Enter len of list")
    temp = int(0)
    while True:
        try:
            temp = int(input())
        except:
            print("Error, enter again")
            continue
        break
    print("Enter elements: ")
    temp = int(temp)
    while True:
        n = input()

        if not functions.check_is_number(n):
            continue

        temp -= 1
        n = float(n)

        numbers.append(n)

        if temp == 0:
            break
    return numbers


def print_list(numbers):
    """Function for print list"""
    print("List of numbers:", numbers)
