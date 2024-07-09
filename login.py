from PIL import Image
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import read_person_data as rpd
import ekgdata as ekg
import person
import os
import subprocess
import sys
import webbrowser
import datetime
# Lade alle Personen
person_names = rpd.get_person_list(rpd.load_person_data())


#Login funktion som kollar om användaren finns i databasen och om lösenordet stämmer
#st.set_page_config(layout="centered", page_title="Welcome", page_icon=":open_hands:")

st.title("Login")

def login_tab1_content():
    
    # Dropdown-Menü für den Benutzernamen mit Vorschlägen
        username = st.selectbox("Benutzername", person_names)
    
    # Texteingabefeld für neuen Benutzernamen
    
    # Passwort-Eingabefeld
        password = st.text_input("Passwort", type="password")



    # Button zum Einloggen
        login_page = st.button("Login")
    # Button zum Speichern eines neuen Benutzernamens
    
    # Verarbeiten der Anmeldeinformationen, wenn der Button gedrückt wird
    
        if login_page:
        # Überprüfen, ob der Benutzername und das Passwort übereinstimmen
            if username in person_names and password == "password":
                st.success("Erfolgreich eingeloggt")
                return username
            else:
                st.error("Falscher Benutzername oder falsches Passwort")
                return "error"
           

def login_tab2_content():
    firstname = st.text_input("Vorname")
    lastname = st.text_input("Nachname")
    date_of_birth = st.number_input("Geburtsjahr", min_value=1900, max_value=2024, step=1)
    # Funktion, um eine neue Person hinzuzufügen
    save = st.button("Speichern")
    if save:
        if save:
            # Erstellen eines neuen Person-Objekts mit den eingegebenen Daten
            new_person = person.Person(
            id=len(person_names) + 1,
            date_of_birth=date_of_birth,
            firstname=firstname,
            lastname=lastname,
            picture_path="data/pictures/tb.jpg",
            ekg_tests=[]
            )
            
            # Hinzufügen des aktuellen Datums zum neuen Person-Objekt
            current_date = datetime.date.today().strftime("%d.%m.%Y")
            new_person.ekg_tests.append({
            "id": len(person_names) + 1,
            "date": current_date,
            "result_link": "data/ekg_data/01_Ruhe.txt"
            })
            
            # Speichern des neuen Person-Objekts in der JSON-Datei
            with open("path/to/your/json/file.json", "a") as file:
                json.dump(new_person.to_dict(), file)
                file.write("\n")
            
            # Erfolgsmeldung anzeigen
            st.success("Person erfolgreich gespeichert")
            # Erstellen eines neuen Person-Objekts mit den eingegebenen Daten
            new_person = person.Person(
                id=len(person_names) + 1,
                date_of_birth=date_of_birth,
                firstname=firstname,
                lastname=lastname,
                picture_path="data/pictures/tb.jpg",
                ekg_tests=[]
            )
            
            # Hinzufügen des aktuellen Datums zum neuen Person-Objekt
            current_date = datetime.date.today().strftime("%d.%m.%Y")
            new_person.ekg_tests.append({
                "id": 1,
                "date": current_date,
                "result_link": "data/ekg_data/01_Ruhe.txt"
            })
            
            # Speichern des neuen Person-Objekts in der JSON-Datei
            with open("path/to/your/json/file.json", "a") as file:
                json.dump(new_person.to_dict(), file)
                file.write("\n")
            
            # Erfolgsmeldung anzeigen
            st.success("Person erfolgreich gespeichert")

   
 

    

def login_page():

    # Tab-Titel definieren
    tab_titles = ['Benutzer aufrufen', 'Benutzer erstellen']

    # Tabs erstellen
    tabs = st.tabs(tab_titles)

    # Inhalt für jeden Tab hinzufügen
    with tabs[0]:
        login_tab1_content()

    with tabs[1]:
        login_tab2_content()


