from time import sleep
from random import choice, randrange

import wanakana

from src.utils.romaji_catalogue import bad_words

class Games():
    def __init__(self, symbols_catalogue, secs_between_letters) -> None:
        self.symbols_catalogue = symbols_catalogue
        self.secs_between_letters = secs_between_letters
        self.game_catalogue = {
            1: self.reading_combos,
            2: lambda symbols_catalogue: self.reading_combos(
                symbols_catalogue,
                writting_system_hint=False),
            3: self.write_it_down
        }

    def choose_game(self, game_number):
        self.game_catalogue[game_number](self.symbols_catalogue)
    
    def write_it_down(self, catalogue):
        while True:
            chosen_writting_system = choice(list(catalogue.keys()))
            chosen_syllabe_or_kanji = choice(
                catalogue[chosen_writting_system])
            print(f"{chosen_writting_system}: {chosen_syllabe_or_kanji}")
            sleep(self.secs_between_letters)
            if chosen_writting_system == "Hiragana":
                print(wanakana.to_hiragana(chosen_syllabe_or_kanji))
            elif chosen_writting_system == "Katakana":
                print(wanakana.to_katakana(chosen_syllabe_or_kanji))
            elif chosen_writting_system == "Kanji":
                print("TBI")
            print("----------------------------------")

    def reading_combos(self, catalogue, writting_system_hint= True):
        prev_romaji_word = ""
        while True:
            chosen_writting_system = choice(list(catalogue.keys()))
            romaji_word = ""
            for _ in range(randrange(1,6)):
                romaji_word += choice(catalogue[chosen_writting_system])
            if romaji_word in bad_words or romaji_word == prev_romaji_word:
                continue
            prev_romaji_word = romaji_word

            if writting_system_hint:
                writting_system_hint = chosen_writting_system + ": "
            else:
                writting_system_hint = ""
            
            print(f"Your combo is:")
            if chosen_writting_system == "hiragana":
                print(f"{writting_system_hint}",
                      wanakana.to_hiragana(romaji_word))
            elif chosen_writting_system == "katakana":
                print(f"{writting_system_hint}",
                      wanakana.to_katakana(romaji_word))
            elif chosen_writting_system == "kanji":
                print(f"{writting_system_hint}", "TBI")

            romaji_input = input("romaji: \n")
            if romaji_word.lower() == romaji_input.lower():
                print("CORRECT!!")
            else:
                print(f"No. The answer is: {romaji_word}")

            sleep(2)
            print("----------------------------------")
