import random
from tkinter import *

import pandas as pd

# Constants
BACKGROUND_COLOR = "#B1DDC6"
FRONT_IMG_PATH = "images/card_front.png"
BACK_IMG_PATH = "images/card_back.png"
WORDS_TO_LEARN_PATH = "data/words_to_learn.csv"
FALLBACK_WORDS_PATH = "data/french_words.csv"
CHECK_BUTTON_IMG_PATH = "images/right.png"
CROSS_BUTTON_IMG_PATH = "images/wrong.png"

current_card = {}
to_learn = {}
window = None
canvas = None
card_front_img = None
card_back_img = None
flip_timer = None
canvas_image = None
card_title = None
card_word = None


# Load data from CSV
def load_data():
    global to_learn
    try:
        data = pd.read_csv(WORDS_TO_LEARN_PATH)
    except FileNotFoundError:
        data = pd.read_csv(FALLBACK_WORDS_PATH)
        to_learn = data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")


# Display the next card
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


# Flip the card to show the English word
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back_img)


# Remove the card from the list and update the CSV
def remove_card():
    to_learn.remove(current_card)
    next_card()
    need_to_learn_data = pd.DataFrame(to_learn)
    need_to_learn_data.to_csv(WORDS_TO_LEARN_PATH, index=False)


# UI Setup
def setup_ui():
    global window, canvas, card_front_img, card_back_img, flip_timer, canvas_image, card_title, card_word

    window = Tk()
    window.title("Flashy")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    flip_timer = window.after(3000, flip_card)

    canvas = Canvas(width=800, height=526)
    card_front_img = PhotoImage(file=FRONT_IMG_PATH)
    card_back_img = PhotoImage(file=BACK_IMG_PATH)
    canvas_image = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 150, text=f"Title", font=("Arial", 40, "italic"))
    card_word = canvas.create_text(400, 263, text=f"Word", font=("Arial", 60, "bold"))
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=2)

    check_button_img = PhotoImage(file=CHECK_BUTTON_IMG_PATH)
    check_button = Button(image=check_button_img, highlightthickness=0, command=next_card)
    check_button.grid(row=1, column=1)

    cross_button_img = PhotoImage(file=CROSS_BUTTON_IMG_PATH)
    cross_button = Button(image=cross_button_img, highlightthickness=0, command=remove_card)
    cross_button.grid(row=1, column=0)

    next_card()
    window.mainloop()


# Main Execution
if __name__ == "__main__":
    load_data()
    setup_ui()
