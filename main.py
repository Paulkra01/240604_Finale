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


st.set_page_config(layout="wide",page_title="Hauptseite", page_icon=":bar_chart:")


# Lade alle Personen
person_names = rpd.get_person_list(rpd.load_person_data())

def tab1_content():
    st.header("EKG-Daten")
# Anlegen diverser Session States
## Gewählte Versuchsperson
    if 'aktuelle_versuchsperson' not in st.session_state:
        st.session_state.aktuelle_versuchsperson = 'None'

    ## Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    ## TODO: Session State für Pfad zu EKG Daten


    # Überschrift
    st.write("# EKG APP")
    st.write("## Versuchsperson auswählen")



    col1, col2, col3 = st.columns(3)

    with col1:
        # Selectbox erstellen
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            'Versuchsperson',
            options = person_names, key="sbVersuchsperson")
        # Name der Versuchsperson
        selected_person = st.session_state.aktuelle_versuchsperson
        # st.write("Der Name ist: ", st.session_state.aktuelle_versuchsperson)

        # TODO: Personendaten anzeigen
        person_birthyear = rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)['date_of_birth']
        st.write(f"Geburtsjahr: {person_birthyear} ")

        # Öffne EKG-Daten
        # TODO: Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
        # Vergleiche Bild und Person
        current_egk_data = ekg.EKGdata(rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["ekg_tests"][0])

        ekg_names = rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["ekg_tests"]
        # Selectbox für Auswahl des EKG-Tests erstellen
        st.session_state.aktuelles_ekg = st.selectbox(
            'EKG',
            options = ekg_names, key="sbEKG")
        


    with col3:

        # Pfad zur Bilddatei
        if st.session_state.aktuelle_versuchsperson in person_names:
            st.session_state.picture_path = rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["picture_path"]
            # st.write("Der Pfad ist: ", st.session_state.picture_path)



        from PIL import Image
        image = Image.open(st.session_state.picture_path)

    # # HTML String für Bild
    #     st.markdown(
    #         f"""
    #         <div style="display: flex; justify-content: center;">
    #             <img src="{st.session_state.picture_path}" alt="{st.session_state.aktuelle_versuchsperson}" style="max-width: 100%;">
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )

        st.image(image, caption=st.session_state.aktuelle_versuchsperson)
        # st.caption(st.session_state.aktuelle_versuchsperson)




    #%% EKG-Daten als Matplotlib Plot anzeigen
    # Nachdem die EKG, Daten geladen wurden
    # Erstelle den Plot als Attribut des Objektes
    fig = current_egk_data.make_plot()
    # Zeige den Plot an
    st.plotly_chart(fig, use_container_width=True)
def tab2_content():
    st.header("FIT-Dateien")

def main():
    st.title('Datenauswertung')

    # Tab-Titel definieren
    tab_titles = ['EKG-Daten', 'Fit-Dateien']

    # Tabs erstellen
    tabs = st.tabs(tab_titles)

    # Inhalt für jeden Tab hinzufügen
    with tabs[0]:
        tab1_content()

    with tabs[1]:
        tab2_content()

if __name__ == "__main__":
    main()

# %% Herzrate bestimmen
# Schätze die Herzrate 
#current_egk_data.estimate_hr()
# Zeige die Herzrate an
#st.write("Herzrate ist: ", int(current_egk_data.heat_rate))