# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random
from WordleDictionary import FIVE_LETTER_WORDS
from RussianWordleDictionary import RUSSIAN_WORD_LIST
from WordleGraphics import WordleGWindow, RussianWordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR
from tkinter import messagebox


def wordle(language='english'):
    if language == 'english':
        word_list = FIVE_LETTER_WORDS
    elif language == 'russian':
        filtered_words = [word for word in RUSSIAN_WORD_LIST if len(word) == 5]
        word_list = filtered_words
    else:
        raise ValueError("Invalid language selection")

    # Generate the solution word once at the beginning of the game
    solution_word = random.choice(word_list)

    def enter_action(s):
        if evaluate_word(s):
            color_boxes(s)

    def evaluate_word(word):
        # Check if the entered word is a legitimate English word
        if word.lower() in word_list:
            return True
        else:
            gw.show_message("Please enter a valid word")
            return False

    def count_occurrences(word):
        # Count the occurrences of each letter in the word
        occurrences = {}
        for letter in word:
            occurrences[letter] = occurrences.get(letter, 0) + 1
        return occurrences

    def color_boxes(word):
        nonlocal solution_word  # Use the solution_word from the outer scope

        print(f"Solution word: {solution_word}")

        solution_occurrences = count_occurrences(solution_word)
        used_positions = set()

        # Color the correct positions in green
        for col in range(N_COLS):
            guess_letter = word[col].lower()
            solution_letter = solution_word[col].lower()

            # Check if the letter is in the correct position
            if guess_letter == solution_letter and solution_occurrences.get(guess_letter, 0) > 0:
                gw.set_square_color(gw.get_current_row(), col, CORRECT_COLOR)
                solution_occurrences[guess_letter] -= 1
                used_positions.add(col)

        # Loop through again to color the remaining positions in yellow or gray
        for col in range(N_COLS):
            guess_letter = word[col].lower()
            solution_letter = solution_word[col].lower()

            # Check if the letter is present in the solution word
            if col not in used_positions and solution_occurrences.get(guess_letter, 0) > 0:
                gw.set_square_color(gw.get_current_row(), col, PRESENT_COLOR)
                solution_occurrences[guess_letter] -= 1
            elif col not in used_positions:
                gw.set_square_color(gw.get_current_row(), col, MISSING_COLOR)

        # Check if the user has correctly guessed all five letters
        if word.lower() == solution_word:
            gw.show_message("Congratulations! You guessed the word!")
         
        else:
            # Move on to the next row
            current_row = gw.get_current_row()
            if current_row < N_ROWS - 1:
                gw.set_current_row(current_row + 1)
            else:
                gw.show_message(f"Game Over. The word was {solution_word}")

    if language == 'english':
        gw = WordleGWindow()
        gw.add_enter_listener(enter_action)
    else:
        gw = RussianWordleGWindow()
        gw.add_enter_listener(enter_action)


# Startup code

if __name__ == "__main__":
    language_choice = messagebox.askquestion("Language Selection", "Do you want to play the game in Russian?\n(If you select 'no' the game will be played in english)")
    if language_choice == 'yes':
        language = 'russian'
    else:
        language = 'english'

    question = messagebox.askquestion("Colorblind Mode", "Do you want to turn on colorblind mode?\nThis will toggle a High Contrast color set")
    if question == 'yes':
        CORRECT_COLOR = '#FFA500'
        PRESENT_COLOR = '#ADD8E6'
        print('colorblind mode on.')
    else:
        print('colorblind mode off')
        
    wordle(language)