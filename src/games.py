"""
A file that contains the class Games.
"""
from time import sleep
from random import choice, randrange

import wanakana

from src.utils.romaji_catalogue import bad_words
from src.utils.input_manager import Input_Manager

class Games():
    """
    A class that contains all the games, and the basic functionalities
    such as a way to choose a game.
    """

    def __init__(self,
                 symbols_catalogue: dict,
                 config: dict
                 ) -> None:
        """
        The function that will start an instance for the Game class.

        Args:
            symbols_catalogue (dict): A dictionary with all the usable
                symbols, with the main keys being the writting systems.
            config (dict): A dictionary of a config yaml file.
        """
        self._symbols_catalogue_ = symbols_catalogue
        self._config_ = config
        self.game_catalogue = {
            1: self.reading_combos,
            2: lambda symbols_catalogue: self.reading_combos(
                symbols_catalogue,
                writting_system_hint=False),
            3: self.write_it_down,
            4: lambda symbols_catalogue: self.write_it_down(
                symbols_catalogue,
                multiple=True)
        }

    def choose_game(self, game_number: int) -> None:
        """
        A function to run a game, given the number it corresponds to,
        and passes the internal symbol catalogue.

        Args:
            game_number (int): The chosen game number.
        """
        self.game_catalogue[game_number](self._symbols_catalogue_)
    
    def write_it_down(self,
                      catalogue: dict,
                      multiple: bool = False
                      ) -> None:
        """
        A game that gives you non-stop a writting system and a symbol
        to write on paper, every n seconds configured in the config file,
        and then it shows the symbol in it's corresponding writting system.

        Args:
            catalogue (dic): A dictionary with all the usable
                symbols, with the main keys being the writting systems.
                multiple (bool): Whether the game wil show one or multiple
                    symbols at a time.
        """
        games_config = self._config_["games"]
        game_config = (games_config["write_it_down"]
                       if not multiple
                       else games_config["write_them_down"])
        while True:
            chosen_writting_system = choice(list(catalogue.keys()))
            chosen_syllabe_or_kanji = choice(
                catalogue[chosen_writting_system])
            if multiple:
                for _ in range(randrange(2,6)):
                    chosen_syllabe_or_kanji += choice(
                        catalogue[chosen_writting_system])
            print(f"{chosen_writting_system}: {chosen_syllabe_or_kanji}")
            sleep(game_config["secs_between_letters"])
            if chosen_writting_system == "Hiragana":
                print(wanakana.to_hiragana(chosen_syllabe_or_kanji))
            elif chosen_writting_system == "Katakana":
                print(wanakana.to_katakana(chosen_syllabe_or_kanji))
            elif chosen_writting_system == "Kanji":
                print("TBI")
            print("----------------------------------")

    def reading_combos(self, catalogue: dict,
                       writting_system_hint: bool = True
                       ) -> None:
        """
        A game that non-stop gives you a combination of symbols and asks you
        to write it in romaji/latin symbols.

        Args:
            catalogue (dic): A dictionary with all the usable
                symbols, with the main keys being the writting systems.
            writting_system_hint (bool, optional): Whether the game will tell
                you which writting system does the symbols belong to. Defaults
                to True.
        """
        prev_romaji_word = ""
        input_manager = Input_Manager(self._config_)
        while True:
            chosen_writting_system = choice(list(catalogue.keys()))
            romaji_word = ""
            for _ in range(randrange(1,6)):
                romaji_word += choice(catalogue[chosen_writting_system])
            if romaji_word in bad_words or romaji_word == prev_romaji_word:
                continue
            prev_romaji_word = romaji_word

            if writting_system_hint:
                writting_system_hint = chosen_writting_system + ":\n\t"
            else:
                writting_system_hint = "\t"
            
            print(f"Your combo is:")
            if chosen_writting_system == "hiragana":
                print(f"{writting_system_hint}{wanakana.to_hiragana(romaji_word)}")
            elif chosen_writting_system == "katakana":
                print(f"{writting_system_hint}",
                      wanakana.to_katakana(romaji_word))
            elif chosen_writting_system == "kanji":
                print(f"{writting_system_hint}", "TBI")

            romaji_input = input_manager.ask_input("\nYour romaji answer:\n\t", str)
            if romaji_word.lower() == romaji_input.lower():
                print("\nCORRECT!!")
            else:
                print(f"\nIncorrect, the answer is: {romaji_word}")

            sleep(1)
            print("----------------------------------")
