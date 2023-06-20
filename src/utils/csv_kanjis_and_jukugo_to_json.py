import re
import csv
import json

from os.path import join as path_join

def kanjis_csv_to_json(csv_path):
    csv_path = path_join(csv_path, "Kanji.csv")
    with open(csv_path,
              newline='',
              encoding="utf8") as kanji_csv_file:
        kanjis_reader = csv.reader(kanji_csv_file, delimiter=";")
        kanjis_data = list(kanjis_reader)

    # Obtain the first row which are the headers, normalizes the id
    # name to "id", generates a kanji dict with the grades as the keys
    kanjis_headers = kanjis_data[0]
    kanjis_headers[0] = "id"
    kanjis_data = kanjis_data[1:]
    kanjis_dict = {number:[] for number in range(1,8)}
    
    # Clean the headers names
    new_kanjis_headers = []
    for header in kanjis_headers:
        new_header = header.lower().replace(" ", "_")
        new_header = re.sub(r"(\d)", r"_\1_", new_header)
        new_kanjis_headers.append(new_header)
    kanjis_headers = new_kanjis_headers

    for kanji in kanjis_data:
        kanji_dict = {}
        for index, header in enumerate(kanjis_headers):
            kanji_data = kanji[index]
            # Clean the data, leave and empty string if there is
            # no data, remove the '\t' or tab spaces, if the data
            # has many elements in it separated by semicolon or
            # commas convert the data into a list
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

            # Normalize the name_of_radical into lists
            if header == "name_of_radical":
                kanji_data = ([kanji_data]
                              if isinstance(kanji_data, str)
                              else kanji_data)
                header = "radical"
            # Set a translation header and put the kun and on
            # translations as part of the translation header
            elif "translation" in header:
                new_kanji_data = []
                # Normalize the data into lists, empty or otherwise
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
            # Set a reading header and put the kun and on
            # readings as part of the reading header
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
                    if isinstance(kanji_data, list):
                        for index, reading in enumerate(kanji_data):
                            if "[" and "]" in reading:
                                kanji_data[index] = reading.replace("[","").replace("]","")
                        reading_data[reading_type].extend(kanji_data)
                    else:
                        reading_data[reading_type].append(kanji_data)
                kanji_data = reading_data
            # Set the sounds as a list of 7 elements, whith a sound
            # if there's one or just an empty string.
            elif "sound" in header:
                sound_dict = {}
                if "sounds" in kanji_dict:
                    sound_dict = kanji_dict["sounds"]
                index_search = re.search(r"\d{1}", header)
                index = (index_search.group()
                         if index_search is not None
                         else None)
                if index is None:
                    raise ValueError(
                        f"Sounds header should have an index or " +
                        "numeric value, given {header}")
                try:
                    index = int(index) - 1
                    if 7 < index < 0:
                        raise Exception()
                except:
                    raise ValueError(
                        "Sounds header should have an index or numeric " +
                        "value bigger than 0 and larger than 7, " +
                        f"given {header}")
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
            # Normalize grades as integers
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
    csv_path = path_join(path, "Jukugo.csv")
    with open(csv_path,
              newline='',
              encoding="utf8") as jukugo_csv_file:
        jukugo_reader = csv.reader(jukugo_csv_file, delimiter=";")
        jukugos_data = list(jukugo_reader)

    # Obtain the first row which are the headers, normalizes the id
    # name to "id", generates a kanji dict with the grades as the keys
    jukugos_headers = jukugos_data[0]
    jukugos_headers[0] = "id"
    jukugos_data = jukugos_data[1:]
    jukugos_dict = {}
    
    # Clean the headers names
    new_jukugos_headers = []
    for header in jukugos_headers:
        new_header = header.lower().replace(" ", "_")
        if len(new_header) != 2 and new_header[-2:] == "id":
            new_header = new_header[:-2] + "_id"
        if new_header == "comp._word":
            new_header = "jukugo"
        new_jukugos_headers.append(new_header)
    jukugos_headers = new_jukugos_headers

    for jukugo in jukugos_data:
        jukugo_dict = {}
        for index, header in enumerate(jukugos_headers):
            if header in ["id", "frequency", "kanji"]:
                continue
            jukugo_data = jukugo[index]
            if header != "kanji_id":
                jukugo_dict[header] = jukugo_data
            else:
                if jukugo_data in jukugos_dict:
                    jukugos_dict[jukugo_data].append(jukugo_dict)
                else:
                    jukugos_dict[jukugo_data] = [jukugo_dict]
    return jukugos_dict

def join_kanjis_jukugos(kanjis_dict, jukugo_dict):
    for grade in kanjis_dict:
        for kanji in kanjis_dict[grade]:
            kanji_id = kanji["id"]
            kanji["jukugos"] = {"L":[], "R":[]}
            if kanji_id not in jukugo_dict.keys():
                continue
            # Gets all the jukugos for a given kanji, for
            # each one, takes the position, deletes it from
            # the jukugo data, and add's it in it's corresponding
            # position
            kanji_jukugos = jukugo_dict[kanji_id]
            for kanji_jukugo in kanji_jukugos:
                position = kanji_jukugo["position"]
                del kanji_jukugo["position"]
                kanji["jukugos"][position].append(kanji_jukugo)
            del kanji["id"]
    return kanjis_dict

def main(main_path):
    kanjis_dict = kanjis_csv_to_json(main_path)
    jukugo_dict = jukugo_csv_to_json(main_path)
    full_kanji_data = join_kanjis_jukugos(kanjis_dict, jukugo_dict)
    new_kanji_data_path_file = path_join(main_path,"kanji.json")
    with open(new_kanji_data_path_file, 'w', encoding='utf-8') as file:
        json.dump(full_kanji_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    utils_path = path_join("src","utils")
    main(utils_path)
