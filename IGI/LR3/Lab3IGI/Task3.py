# In accordance with the assignment of your option,
# create a program for analyzing text entered from the keyboard.
def function_for_task3():
    """Function for solve task3"""
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Input your string and program will find number of spaces and punctuation marks in it")
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Enter your string")
    string = input()
    count1 = count_symbol(" ", string)
    count2 = count_symbol(".", string)
    count3 = count_symbol("?", string)
    count4 = count_symbol("...", string)
    count5 = count_symbol(":", string)
    count6 = count_symbol("!", string)
    count7 = count_symbol(";", string)
    count8 = count_symbol(",", string)
    count9 = count_symbol("-", string)
    count10 = count_symbol("—", string)
    count11 = count_symbol("(", string)
    return f"Amount of: Spaces = {count1}, Period = {count2}, Question mark = {count3}, Ellipsis = {count4}, Colon = {count5}, Exclamation mark = {count6}, Semicolon = {count7}, Comma = {count8}, Dash = {count9}, Double dash = {count10}, Parentheses = {count11}"


def count_symbol(symbol, string):
    """Function fot count symbol in string"""
    return string.count(symbol)
