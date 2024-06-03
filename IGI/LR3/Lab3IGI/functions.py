import tkinter as tk
from tkinter import ttk
import time
from decimal import Decimal
from random import *


def check_is_integer(x):
    """Function for check input integer"""
    try:
        int(x)
    except:
        print("Enter an integer")
        return False
    return True


def gen_int():
    """Function for get sec of integer number input"""
    for i in range(10):
        yield randint(-100, 100)


def gen_float():
    """Function for get sec of float number input"""
    for i in range(10):
        yield uniform(-100, 100)


def random_integer():
    """Function for random integer input"""
    numbers = []
    gen = gen_int()
    for i in range(10):
        numbers.append(next(gen))
    return numbers


def random_float():
    """Function for random float input"""
    numbers = []
    gen = gen_float()
    for i in range(10):
        numbers.append(next(gen))
    return numbers


def check_is_number(x):
    """Function for check input number"""
    try:
        float(x)
    except:
        print("Enter a number not a string")
        return False
    return True


def print_as_table(list):
    """Function fot input result in table"""
    window = tk.Tk()
    window.title('Table')
    frame_list = tk.Frame(window, bg='blue')
    frame_list.place(relx=0, rely=0, relheight=0.1, relwidth=1)
    table = ttk.Treeview(frame_list, show='headings')
    heads = ["x", "n", "F(x)", "Math F(x)", "eps"]
    table['columns'] = heads

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')

    table.insert('', tk.END, values=list)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    window.mainloop()


def my_decorator(func):
    """Decorator to determine the execution time of a function"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        for i in range(100):
            func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} run for {Decimal(end_time-start_time)/100:.10f} seconds")
        return func(*args, **kwargs)
    return wrapper
