import decimal

import requests


def get_joke():
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)
    data = response.json()

    setup = data["setup"]
    punch = data["punchline"]
    return f"{setup} - {punch}"


def get_quote():
    url = 'https://favqs.com/api/qotd'
    response = requests.get(url)
    data = response.json()

    quote = data['quote']['body']
    author = data['quote']['author']

    return f"{quote} - {author}."
