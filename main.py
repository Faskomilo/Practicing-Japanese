"""
A file that contains the main function of the system, the main entry point.
"""
from src.games import Games
from src.symbols_catalogue import Symbols_Catalogue
from src.utils.utils import Utils
from src.utils.input_manager import Input_Manager

def main() -> None:
    """
    Runs the whole system for choosing a game, creating a syllabogram
    and logogram catalogue for the Hiragana, Katakana and Kanji systems
    depending on the configurations given on the config.yaml file and
    running a game.
    """
    config = Utils.read_config()
    symbols_catalogue = Symbols_Catalogue(config).get_catalogue()
    game_options = [1,2,3,4]

    print("""Which game would you like to play?

        Options:
            1. Reading combos:
                A combination of syllabs and logographs (kanjis) will appear
                and you have to read it and write it in romaji.
            2. Reading combos without system hint:
                A combination of syllabs and logographs (kanjis) will appear
                and you have to read it and write it in romaji.
            3. Write it down: 
                A game where the game will tell you which syllable or kanji
                to write on paper, and you have to write it before the next
                one pops up.
            4. Write them down: 
                A game where the game will tell you a combination of syllables
                or kanjis to write on paper, and you have to write it before
                the next combo pops up.
        """)
    
    message = "Type the number of the game you would like to play: "
    game_number = Input_Manager(config).ask_input(message, int, game_options)
    Games(symbols_catalogue, config).choose_game(game_number)

if __name__ == "__main__":
    main()
