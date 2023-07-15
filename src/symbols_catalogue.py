"""
A file that contains the Symbols_Catalogue class.
"""
from src.utils.romaji_catalogue import hiragana, katakana, kanji

class Symbols_Catalogue:
    """
    A class for the catalogue of syllabograms (Hiragana, Katakana) and
    logograms (Kanjis).
    """
    def __init__(self, config: dict) -> None:
        """
        The init of the class, gets the config variables regarding to
        latest elements, and creates a catalogue depending on said variables.

        Args:
            config (dict): A dictionary of a config yaml file.
        """
        self._top_hiragana_ = config["top_symbol"]["hiragana"]
        self._top_katakana_ = config["top_symbol"]["katakana"]
        self._top_kanji_ = config["top_symbol"]["kanji"]
        self.__create_catalogue()

    def get_catalogue(self) -> dict:
        """
        A getter for the created symbols catalogue.

        Returns:
            dict: A catalogue of symbols depending the config setup.
        """
        return self._catalogue_

    def __create_catalogue(self) -> None:
        """
        Creates a catalogue, either the whole catalogue or a truncated one
        depending of the config variables.
        """
        if(self._top_hiragana_ == 'py'
           and self._top_katakana_ == 'py'
           and self._top_kanji_ == "7"):
            self.__create_whole_catalogue()
        else:
            self.__create_config_truncated_catalogue()

    def __create_whole_catalogue(self) -> None:
        """
        Creates a catalogue with all the possibilities of hiragana, katakana
        and kanji (limited to the Joyo kanji database).
        """
        self._catalogue_ = {}

        self._catalogue_["hiragana"] = self.__get_symbols_as_list(
            hiragana
            )
        self._catalogue_["katakana"] = self.__get_symbols_as_list(
            katakana
            )
        self._catalogue_["kanji"] = self.__get_symbols_as_list(
            kanji 
            )

    def __create_config_truncated_catalogue(self) -> None:
        """
        Creates a catalogue truncated with all the possibilities of hiragana,
        katakana and kanji (limited to the Joyo kanji database), up to the
        top element given on the config file.
        """
        self._catalogue_ = {}
        
        if self._top_hiragana_ != "":
            self._catalogue_["hiragana"] = self.__get_symbols_as_list(
                hiragana,
                truncate_catalogue=True,
                top_symbol=self._top_hiragana_
            )

        if self._top_katakana_ != "":
            self._catalogue_["katakana"] = self.__get_symbols_as_list(
                katakana,
                truncate_catalogue=True,
                top_symbol=self._top_katakana_
            )

        if self._top_kanji_ != 0:
            self._catalogue_["kanji"] = self.__get_symbols_as_list(
                kanji,
                truncate_catalogue=True,
                top_symbol=self._top_kanji_
            )
    
    def __get_symbols_as_list(self,
                              symbols_catalogue: tuple,
                              truncate_catalogue: bool = False,
                              top_symbol: str = ""
                              ) -> list:
        """
        Gets the symbols of a given writting system as a list, up
        until a given one if given.

        Args:
            letter_catalogue (tuple): a tuple of all the symbols, each
                element being a dictionary with the consonant (for hiragana
                and katakana) or the grade (kanji) as the main key, and all
                of its elements in romaji as a list.
            truncate_catalogue (bool, optional): Whether the catalogue will
                be truncated. Defaults to False.
            top_symbol (str, optional): The top symbol the catalogue will be
                truncated at. Defaults to "".

        Returns:
            list: A list of all possibilities for that given writting system.
        """
        letters = []
        for letter in symbols_catalogue:
            letters.extend(list(letter.values())[0])
            if truncate_catalogue and top_symbol == list(letter.keys())[0]:
                break
        return letters