import csv
import re
from os.path import join as path_join

def kanjis_csv_to_json(csv_path):
    """
    After reading the whole kaji csv file, refactors the data
    in order to 

    Args:
        csv_path (_type_): _description_

    Raises:
        ValueError: _description_
        Exception: _description_
        ValueError: _description_
        Exception: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    csv_path = path_join(csv_path, "Kanji.csv")
    with open(csv_path,
              newline='',
              encoding="utf8") as kanji_csv_file:
        kanjis_reader = csv.reader(kanji_csv_file, delimiter=";")
        kanjis_data = list(kanjis_reader)

    kanjis_headers = kanjis_data[0]
    kanjis_headers[0] = "id"
    kanjis_data = kanjis_data[1:]
    kanjis_dict = {number:[] for number in range(1,8)}

    new_kanjis_headers = []
    for header in kanjis_headers:
        new_header = header.lower().replace(" ", "_")
        new_header = re.sub(r"(\d)", r"_\1_", new_header)
        new_kanjis_headers.append(new_header)
        if new_header == 'name_of_radical':
            new_header = "radical"

    for kanji in kanjis_data:
        kanji_dict = {}
        for index, header in enumerate(new_kanjis_headers):
            if header == "id":
                continue
            kanji_data = kanji[index]
            kanji_data = "" if kanji_data == "-" else kanji_data
            kanji_data = (kanji_data.replace("\t", "")
                        if "\t" in kanji_data
                        else kanji_data)
            kanji_data = (kanji_data.split("; ")
                        if "; " in kanji_data
                        else kanji_data)
            kanji_data = (kanji_data.split(", ")
                        if ", " in kanji_data
                        else kanji_data)

            if header == "name_of_radical":
                kanji_data = [kanji_data] if isinstance(kanji_data, str) else kanji_data
                header = "radicals"
            elif "translation" in header:
                new_kanji_data = []
                if isinstance(kanji_data, str):
                    if kanji_data == "":
                        kanji_data = []
                    else:
                        kanji_data = [kanji_data]
                for translation in kanji_data:
                    translation = (translation.split(", ")
                                if ", " in translation
                                else [translation])
                    new_kanji_data.append(translation)
                kanji_data = new_kanji_data
                if "_on" in header:
                    translation_data = {"on": kanji_data}
                elif "_kun" in header:
                    translation_data = {"kun": kanji_data}
                header = "translation"
                if header in kanji_dict:
                    translation_data.update(kanji_dict[header])
                kanji_data = translation_data
            elif "within" in header and "reading" not in header:
                if "on_" in header:
                    reading_type = "on"
                elif "kun_" in header:
                    reading_type = "kun"
                reading_data = {"on":[],"kun":[]}
                header = "reading"
                if header in kanji_dict:
                    reading_data = kanji_dict["reading"]
                if kanji_data != "":
                    reading_data[reading_type].append(kanji_data)
                kanji_data = reading_data
            elif "sound" in header:
                sound_dict = {}
                if "sounds" in kanji_dict:
                    sound_dict = kanji_dict["sounds"]
                index_search = re.search(r"\d{1}", header)
                index = index_search.group() if index_search is not None else None
                if index is None:
                    raise ValueError(
                        f"Sounds header should have an index or numeric value," +
                        " given {header}")
                try:
                    index = int(index) - 1
                    if 7 < index < 0:
                        raise Exception()
                except:
                    raise ValueError(
                        f"Sounds header should have an index or numeric " +
                        "value bigger than 0 and larger than 7, given {header}")
                sounds = [""]*7
                if "left" in header:
                    if "left" not in sound_dict:
                        sound_dict["left"] = sounds
                    sound_dict["left"][index] = kanji_data
                if "right" in header:
                    if "right" not in sound_dict:
                        sound_dict["right"] = sounds
                    sound_dict["right"][index] = kanji_data
                header = "sounds"
                kanji_data = sound_dict
            elif header == "grade":
                try:
                    kanji_data = int(kanji_data)
                    if 8 < kanji_data < 1:
                        raise Exception()
                except:
                    raise ValueError("Grade should be a numeric value " +
                                    f"between 1 and 7, given: {kanji_data}")
            kanji_dict[header] = kanji_data
        grade = kanji_dict["grade"]
        del kanji_dict["grade"]
        kanjis_dict[grade].append(kanji_dict)
    return kanjis_dict

def jukugo_csv_to_json(path):
    csv_path = path_join(csv_path, "Kanji.csv")
    with open(path,
              newline='',
              encoding="utf8") as jukugo_csv_file:
        jukugo_reader = csv.reader(jukugo_csv_file, delimiter=";")
        jukugos_data = list(jukugo_reader)

def join_kanjis_jukugos(kanjis_dict, jukugo_dict):
    pass

def main(main_path):
    kanjis_dict = kanjis_csv_to_json(main_path)
    jukugo_dict = jukugo_csv_to_json(main_path)
    full_kanji_data = join_kanjis_jukugos(kanjis_dict, jukugo_dict)

if __name__ == "__main__":
    utils_path = path_join("src","utils")
    main(utils_path)
