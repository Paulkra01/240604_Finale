import json
import pandas as pd

# open JSON file
def load_person_data():
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data # type dict

def get_person_list(person_data):
    """A Function that takes the Persons-Dictionary and returns a List auf all person names"""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return list_of_names


def find_person_data_by_name(suchstring): # in der Form "Nachname, Vorname"    
    person_data = load_person_data()
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        print(eintrag)
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print()

            return eintrag
    else:
        return {}