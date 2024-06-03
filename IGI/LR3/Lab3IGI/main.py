# Detkovsky Kirill Anatolievich
# Version 1.0.0
# Date of developing 28.03.2024
# Lab 3 "Standard data types, collections, functions, modules"
# This program implements 5 tasks based on the laboratory work option.
import Task1
import Task2
import Task3
import Task4
import Task5
import functions

def main():
    """Main function for menu"""
    while True:
        print("Enter symbol: 1 for task1, 2 for task2, 3 for task3, 4 for task4, 5 for task5, exit fot exit ")
        temp = input()
        if temp == "1":
            functions.print_as_table(Task1.function_for_task1())
        elif temp == "2":
            print(f"Answer: {Task2.function_for_task2()}")
        elif temp == "3":
            print(Task3.function_for_task3())
        elif temp == "4":
            print(Task4.function_for_task4())
        elif temp == "5":
            print(Task5.function_for_task5())
        elif temp == "exit":
            a = 2+'3'
            print(a)
            break
        else:
            print("Incorrect input")


if __name__ == "__main__":
    main()
