# Detkovsky Kirill Anatolievich
# Version 1.0.0
# Date of developing 21.04.2024
# Lab 4
# This program implements 5 tasks based on the laboratory work option.
import Task1
import Task2
import Task3
import Task4
import Task5


def main():
    """Main function for 4 lab."""
    while True:
        print("Welcome to lab4!")
        print("Here are the tasks:")
        print("1. Human data handling")
        print("2. Text analyzis with regual expressions")
        print("3. Arccos approximation task")
        print("4. Polygon drawing")
        print("5. Matrix operations")

        choice = input("Choose task (to stop type 'exit'): ")

        if choice == '1':
            Task1.main()
        elif choice == '2':
            Task2.main()
        elif choice == '3':
            Task3.main()
        elif choice == '4':
            Task4.main()
        elif choice == '5':
            Task5.main()
        elif choice.lower() == 'exit':
            print("End of program")
            break
        else:
            print("ERROR! WRONG INPUT")


main()
