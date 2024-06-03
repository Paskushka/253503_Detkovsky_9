# Given a line of text in which words are separated by spaces and commas.
# In accordance with the specification of your option,
# create a program to analyze the string initialized in the program code:

# «So she was considering in her own mind, as well as she could,
# for the hot day made her feel very sleepy and stupid,
# whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies,
# when suddenly a White Rabbit with pink eyes ran close by her.»
def function_for_task4():
    """Function for solve task4"""
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Function will: ")
    print("a) determine the number of words beginning and ending with a vowel")
    print("b) determine how many times each character is repeated")
    print("c) list words after commas in alphabetical order")
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
    string = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    string_array = split_string(string)
    return f"Start or end with vowel: {count_words(string_array)} \nSymbol frequency: {count_symbol_frequency(string)} \nWords after comma: {sort_words_after_comma(string)}"


def split_string(string):
    """Function for split string"""
    string_array = string.replace(',', '').split()
    return string_array


def count_words(string_array):
    """Function for count words in string"""
    vowels = "aeiouyAEIOUY"
    count = 0;
    for word in string_array:
        if word[0] in vowels or word[-1] in vowels:
            count+=1
    return count


def count_symbol_frequency(string):
    """Function for count symbol frequency in string"""
    frequency = {}
    for char in string:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    return frequency


def sort_words_after_comma(string):
    """Function for sort words in string"""
    words = string.split(",")
    result = []
    for i in range(1, len(words)):
        words_after_comma = words[i].split()
        if len(words_after_comma) > 0:
            first_word = words_after_comma[0].strip()
            result.append(first_word)

    return sorted(result)