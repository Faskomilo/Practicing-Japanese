import yaml
from random import choice, randrange
from time import sleep

import wanakana

def main():
    config = Utils.read_config()
    catalogue = Catalogue(config).get_catalogue()

    print("""Which game would you like to play?

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
        
        """)
    game_type = input("Type the number of the game you would like to play: ")

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
        seconds_between_letters = config["system"]["secs_between_letters"]
        Games.write_it_down(catalogue, seconds_between_letters)
    elif game_type == 2:
        Games.reading_combos(catalogue)
    elif game_type == 3:
        Games.reading_combos(catalogue, type_hint=False)

class Games():
    @staticmethod
    def write_it_down(catalogue, seconds_between_letters):
        while True:
            chosen_writting_system = choice(list(catalogue.keys()))
            chosen_syllabe_kanji = choice(catalogue[chosen_writting_system])
            print(f"{chosen_writting_system}: {chosen_syllabe_kanji}")
            sleep(seconds_between_letters)
            if chosen_writting_system == "Hiragana":
                print(wanakana.to_hiragana(chosen_syllabe_kanji))
            elif chosen_writting_system == "Katakana":
                print(wanakana.to_katakana(chosen_syllabe_kanji))
            elif chosen_writting_system == "Kanji":
                print("TBI")
            print("----------------------------------")

    @staticmethod
    def reading_combos(catalogue, type_hint= True):
        while True:
            chosen_writting_type = choice(list(catalogue.keys()))
            romanji_word = ""
            for _ in range(randrange(1,6)):
                romanji_word += choice(catalogue[chosen_writting_type])
            if type_hint:
                type_hint = chosen_writting_type + ": "
            else:
                type_hint = ""
            print(f"Your combo is:")
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

class Catalogue:
    _hiragana_ = (
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

    _katakana_ = (
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

    _kanji_ = ()

    def __init__(self, config) -> None:
        self._hiragana_latest_ = config["letters"]["hiragana"]
        self._katakana_latest_ = config["letters"]["katakana"]
        self._kanji_latest_ = config["letters"]["kanji"]
        self._create_catalogue_()

    def get_catalogue(self):
        return self._catalogue_()

    def _create_catalogue_(self):
        if(self._hiragana_latest_ == 'py'
           and self._katakana_latest_ == 'py'
           and self._kanji_latest_ == list(self._kanji_.keys())[0]):
            self._create_whole_catalogue_()
        else:
            self._reduce_catalogue_from_config_()

    def _create_whole_catalogue_(self):
        self._catalogue_ = {}

        self._catalogue_["hiragana"] = self._get_letter_elements_as_list_(
            self._hiragana_
            )
        self._catalogue_["katakana"] = self._get_letter_elements_as_list_(
            self._katakana_
            )
        self._catalogue_["kanji"] = self._get_letter_elements_as_list_(
            self._kanji_
            )

    def _reduce_catalogue_from_config_(self):
        self._catalogue_ = {}
        
        if self._hiragana_latest_ != "":
            self._catalogue_["hiragana"] = self._get_letter_elements_as_list_(
                self._hiragana_,
                break_list=True,
                break_element=self._hiragana_latest_
            )

        if self._katakana_latest_ != "":
            self._catalogue_["katakana"] = self._get_letter_elements_as_list_(
                self._katakana_,
                break_list=True,
                break_element=self._katakana_latest_
            )

        if self._kanji_latest_ != "":
            self._catalogue_["kanji"] = self._get_letter_elements_as_list_(
                self._kanji_,
                break_list=True,
                break_element=self._kanji_latest_
            )
    
    def _get_letter_elements_as_list_(self,
                                    letter_catalogue,
                                    break_list= False,
                                    break_element= ""
                                    ) -> list:
        letters = []
        for letter in letter_catalogue:
            letters.extend(list(letter.values())[0])
            if break_list and break_element == list(letter.keys())[0]:
                break
        return letters

class Utils():
    @staticmethod
    def read_config():
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        return config

if __name__ == "__main__":
    main()
