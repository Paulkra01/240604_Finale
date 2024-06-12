import streamlit_authenticator as stauth
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

#Login funktion som kollar om användaren finns i databasen och om lösenordet stämmer
def login():st.set_page_config(layout="wide")

# Lade alle Personen
person_names = rpd.get_person_list(rpd.load_person_data())


# Anlegen diverser Session States
## Gewählte Versuchsperson
if 'aktuelle_versuchsperson' not in st.session_state:
    st.session_state.aktuelle_versuchsperson = 'None'

## Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

col1, col2, col3 = st.columns(3) 
    
with col1:  
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            'Versuchsperson',
            options = person_names, key="sbVersuchsperson")
        # Name der Versuchsperson
        selected_person = st.session_state.aktuelle_versuchsperson

with col2:
    person_birthyear = rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)['date_of_birth']
    st.write(f"Geburtsjahr: {person_birthyear} ")

with col3:
     person_id = rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["id"]