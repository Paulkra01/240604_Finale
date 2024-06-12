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

#Login funktion som kollar om användaren finns i databasen och om lösenordet stämmer
st.set_page_config(layout="centered", page_title="Welcome", page_icon=":open_hands:")

st.title("Login")


# Dropdown-Menü für den Benutzernamen mit Vorschlägen
username = st.selectbox("Benutzername", person_names)

# Texteingabefeld für neuen Benutzernamen
new_username = st.text_input("Neuer Benutzername")

# Passwort-Eingabefeld
password = st.text_input("Passwort", type="password")



# Button zum Einloggen
login_button = st.button("Login")
# Button zum Speichern eines neuen Benutzernamens
save_button = st.button("Als neues Profil speichern")

# Verarbeiten der Anmeldeinformationen, wenn der Button gedrückt wird
if login_button:
    if username == "user1" and password == "password":
        st.success("Erfolgreich eingeloggt")
        # Weitere Aktionen nach erfolgreichem Login
    else:
        st.error("Falscher Benutzername oder falsches Passwort")

# Verarbeiten des neuen Benutzernamens, wenn der Button gedrückt wird
if save_button and new_username:
    usernames.append(new_username)
    st.success(f"Neuer Benutzer '{new_username}' erfolgreich erstellt")