from games import Games
from symbols_catalogue import Symbols_Catalogue
from utils.utils import Utils

def main():
    config = Utils.read_config()
    symbols_catalogue = Symbols_Catalogue(config).get_catalogue()

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
                to writeon paper, and you have to write it before the next
                one comes.
        """)
    game_number = input(
        "Type the number of the game you would like to play: ")

    if game_number is None:
        print("You have to write a number")
        exit()
    try:
        game_number = int(game_number)
        if game_number not in [1,2,3]:
            raise ValueError
    except ValueError or Exception:
        print(f"Incorrect value, given: {game_number} expected 1, 2, 3")
        exit()
    secs_between_letters = config["system"]["secs_between_letters"]
    Games(symbols_catalogue, secs_between_letters).choose_game(game_number)

if __name__ == "__main__":
    main()
