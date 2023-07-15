"""
A file that contains the complete catalogue of syllabogram writting systems
(hiragana, katakana) and a way to ingest the data for kanjis and it's
jukugos. As well as a bad word's list as to avoid them.
"""

hiragana = (
    {'base': ['a','i','u','e','o']},
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

katakana = (
    {'base': ['a','i','u','e','o']},
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

kanji = ()

bad_words = [
    "baka",
    "bakayurou",
    "aho",
    "kuso",
    "chikushou",
    "warugaki",
    "fuzakeruna",
    "doke",
    "shine",
    "busu",
    "urusai",
    "damare"
]
