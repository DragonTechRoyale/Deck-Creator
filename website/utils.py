from py_console import console
from flask import flash

messages = {
    "errors" : {
        "deck_exists" : "deck already exists",
        "no_word_count_error" : "place a number in the amount of words",
        "word_count_error" : "Word count is too big or low",
        "lang_not_supported" : "One of the languages is not supported (this error shouldn\'t happen)",
        "user_not_create_deck" : "You haven't created any decks to learn yet. Click the \"Create Deck\" button to create a deck",
        "arabic_not_supported" : "Arabic is not supported currently as a target language"
    },
    "warns" : {
        "window_closed" : "create_deck() - Window was closed while making the database\n(the database was still created succesfully, just with less items)"
    },
    "successes" : {
        "created_deck" : "successfully created deck",
        "making_deck" : "making deck..."
    }
}

def display_success(success_message) -> None:
    console.success(success_message)
    flash(success_message, category='success')


def display_error(error_message) -> None:
    console.error(error_message)
    flash(error_message, category='error')
    
