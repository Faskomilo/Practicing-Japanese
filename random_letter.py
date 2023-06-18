import yaml
from random import choice, randrange
from time import sleep

import wanakana

def main():
    hiragana = (
        {'basic': ['a','i','u','e','o']},
        {'k': ['ka','ki','ku','ke','ko']},
        {'s': ['sa','shi','su','se','so']},
        {'t': ['ta','chi','tsu','te','to']},
        {'n': ['na','ni','nu','ne','no']},
        {'h': ['ha','hi','fu','he','ho']},
        {'m': ['ma','mi','mu','me','mo']},
        {'y': ['ya','yu','yo']},
        {'r': ['ra','ri','ru','re','ro']},
        {'w': ['wa','wo']},
        {'n': ['n']},
        {'g': ['ga','gi','gu','ge','go']},
        {'z': ['za','ji','zu','ze','zo']},
        {'d': ['da','ji','zu','de','do']},
        {'b': ['ba','bi','bu','be','bo']},
        {'p': ['pa','pi','pu','pe','po']},
        {'ky': ['kya','kyu','kyo']},
        {'sh': ['sha','shu','sho']},
        {'ch': ['cha','chu','cho']},
        {'ny': ['nya','nyu','nyo']},
        {'hy': ['hya','hyu','hyo']},
        {'my': ['mya','myu','myo']},
        {'ry': ['rya','ryu','ryo']},
        {'gy': ['gya','gyu','gyo']},
        {'j': ['ja','ju','jo']},
        {'by': ['bya','byu','byo']},
        {'py': ['pya','pyu','pyo']}
    )

    katakana = ()

    kanji = ()

    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    hiragana_latest = config["letters"]["hiragana"]
    katakana_latest = config["letters"]["katakana"]
    kanji_latest = config["letters"]["kanji"]
    seconds_between_letters = config["system"]["secs_between_letters"]

    catalogue = {}

    if hiragana_latest != "":
        catalogue["hiragana"] = []
        for letter in hiragana:
            catalogue["hiragana"].extend(list(letter.values())[0])
            if hiragana_latest == list(letter.keys())[0]:
                break

    if katakana_latest != "":
        catalogue["katakana"] = []
        for letter in katakana:
            catalogue["katakana"].extend(list(letter.values())[0])
            if katakana_latest == list(letter.keys())[0]:
                break

    if kanji_latest != "":
        catalogue["kanji"] = []
        for letter in kanji:
            catalogue["kanji"].extend(list(letter.values())[0])
            if kanji_latest == list(letter.keys())[0]:
                break

    game_type = input(
        """Which game would you like to play?

        Options:
            1. Write it down: 
                A game where the game will tell you which syllable to write, and
                you have to write it before the next one comes.
            2. Reading combos:
                A combination of syllabs and logographs (kanjis) will appear and
                you have to read it and write it in romanji.
            3. Read combos without system hint:
                A combination of syllabs and logographs (kanjis) will appear and
                you have to read it and write it in romanji.

        Type the number of the game you would like to play: """
        )
    if game_type is None:
        print("You have to write a number")
        exit()
    try:
        game_type = int(game_type)
        if game_type not in [1,2,3]:
            raise ValueError
    except ValueError or Exception:
        print(f"Incorrect value, given: {game_type} expected 1, 2, 3")
        exit()

    if game_type == 1:
        games.write_it_down(catalogue, seconds_between_letters)
    elif game_type == 2:
        games.read_me(catalogue)
    elif game_type == 3:
        games.read_me(catalogue, type_hint=False)

class games():
    @staticmethod
    def write_it_down(catalogue, seconds_between_letters):
        while True:
            chosen_writting_type = choice(list(catalogue.keys()))
            chosen_letter = choice(catalogue[chosen_writting_type])
            print(f"{chosen_writting_type}: {chosen_letter}")
            sleep(seconds_between_letters)
            if chosen_writting_type == "Hiragana":
                print(wanakana.to_hiragana(chosen_letter))
            elif chosen_writting_type == "Katakana":
                print(wanakana.to_katakana(chosen_letter))
            elif chosen_writting_type == "Kanji":
                print("TBI")
            print("----------------------------------")

    @staticmethod
    def read_me(catalogue, type_hint= True):
        while True:
            chosen_writting_type = choice(list(catalogue.keys()))
            romanji_word = ""
            for _ in range(randrange(1,6)):
                romanji_word += choice(catalogue[chosen_writting_type])
            if type_hint:
                type_hint = chosen_writting_type + ": "
            else:
                type_hint = ""
            print(f"Your word is:")
            if chosen_writting_type == "hiragana":
                print(f"{type_hint}", wanakana.to_hiragana(romanji_word))
            elif chosen_writting_type == "katakana":
                print(f"{type_hint}", wanakana.to_katakana(romanji_word))
            elif chosen_writting_type == "kanji":
                print(f"{type_hint}", "TBI")
            romanji_input = input("Romanji: ")
            print("")
            if romanji_word.lower() == romanji_input.lower():
                print("CORRECT!!")
            else:
                print(f"No. The answer is: {romanji_word}")
            sleep(2)
            print("----------------------------------")

if __name__ == "__main__":
    main()
