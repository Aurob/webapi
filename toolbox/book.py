import requests
import random

def get_random_book():
    # Get a random number
    random_id = random.randint(1, 10000000) # consider this number based on available books in OpenLibrary

    # Use OpenLibrary API with the random id
    response = requests.get(f"https://openlibrary.org/works/OL{random_id}W.json")

    # Parse the result
    result = response.json()

    # If the book with this id exists, return its info

    if result:
        # return result
        title = result['title']
        return title
    else:
        return None

def default():
    return get_random_book()