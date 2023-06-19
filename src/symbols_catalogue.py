from src.utils.romaji_catalogue import hiragana, katakana, kanji

class Symbols_Catalogue:
    def __init__(self, config) -> None:
        self._hiragana_latest_ = config["latest_element"]["hiragana"]
        self._katakana_latest_ = config["latest_element"]["katakana"]
        self._kanji_latest_ = config["latest_element"]["kanji"]
        self._create_catalogue_()

    def get_catalogue(self):
        return self._catalogue_

    def _create_catalogue_(self):
        if(self._hiragana_latest_ == 'py'
           and self._katakana_latest_ == 'py'
           and self._kanji_latest_ == list(kanji.keys())[0]):
            self._create_whole_catalogue_()
        else:
            self._reduce_catalogue_from_config_()

    def _create_whole_catalogue_(self):
        self._catalogue_ = {}

        self._catalogue_["hiragana"] = self._get_letter_elements_as_list_(
            hiragana
            )
        self._catalogue_["katakana"] = self._get_letter_elements_as_list_(
            katakana
            )
        self._catalogue_["kanji"] = self._get_letter_elements_as_list_(
            kanji 
            )

    def _reduce_catalogue_from_config_(self):
        self._catalogue_ = {}
        
        if self._hiragana_latest_ != "":
            self._catalogue_["hiragana"] = self._get_letter_elements_as_list_(
                hiragana,
                break_list=True,
                break_element=self._hiragana_latest_
            )

        if self._katakana_latest_ != "":
            self._catalogue_["katakana"] = self._get_letter_elements_as_list_(
                katakana,
                break_list=True,
                break_element=self._katakana_latest_
            )

        if self._kanji_latest_ != 0:
            self._catalogue_["kanji"] = self._get_letter_elements_as_list_(
                kanji,
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