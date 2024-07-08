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

# Lade alle Personen
person_names = rpd.get_person_list(rpd.load_person_data())
print (person_names) 

#Login funktion som kollar om användaren finns i databasen och om lösenordet stämmer
st.set_page_config(layout="centered", page_title="Welcome", page_icon=":open_hands:")

st.title("Login")

def tab1_content():
    
    # Dropdown-Menü für den Benutzernamen mit Vorschlägen
    username = st.selectbox("Benutzername", person_names)

    # Texteingabefeld für neuen Benutzernamen
    
    # Passwort-Eingabefeld
    password = st.text_input("Passwort", type="password")



    # Button zum Einloggen
    login_button = st.button("Login")
    # Button zum Speichern eines neuen Benutzernamens
    
    if login_button:
        if st.button("Zur Login-Seite wechseln"):
            st.experimental_set_query_params(page= "main.py")
    # Verarbeiten der Anmeldeinformationen, wenn der Button gedrückt wird
    if login_button:
        if username == "user1" and password == "password":
            st.success("Erfolgreich eingeloggt")
            # Weitere Aktionen nach erfolgreichem Login
        else:
            st.error("Falscher Benutzername oder falsches Passwort")

def tab2_content():
    # Eingabefelder für neuen Benutzernamen und Geburtsdatum
    firstname = st.text_input("Vorname")
    lastname = st.text_input("Nachname")
    date_of_birth = st.text_input("Geburtsjahr") 
    
    # Button zum Speichern
    save_button = st.button("Speichern")

    if save_button:
        # Lade vorhandene Benutzerdaten
        person_data = rpd.load_person_data()

        # Generiere eine neue ID für den Benutzer
        if person_data:
            new_id = max(person_data.keys()) + 1
        else:
            new_id = 1
        
        # Erstelle ein neues Person-Objekt mit den eingegebenen Daten
        new_person = person.Person(new_id, firstname, lastname, date_of_birth)
        
        # Lade vorhandene Benutzerdaten
        person_data = rpd.load_person_data()

        # Füge den neuen Eintrag zur Datenbank hinzu
        person_data[new_id] = new_person.to_dict()

        # Speichere die aktualisierten Benutzerdaten
        rpd.save_person_data(person_data)
# Verarbeiten des neuen Benutzernamens, wenn der Button gedrückt wird
 

    

def main():

    # Tab-Titel definieren
    tab_titles = ['Benutzer aufrufen', 'Benutzer erstellen']

    # Tabs erstellen
    tabs = st.tabs(tab_titles)

    # Inhalt für jeden Tab hinzufügen
    with tabs[0]:
        tab1_content()

    with tabs[1]:
        tab2_content()

if __name__ == "__main__":
    main()