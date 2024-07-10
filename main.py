
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
import fitparse
import pandas as pd
import fitdata as fit
st.set_page_config(layout="wide",page_title="Hauptseite", page_icon=":bar_chart:")
import pickle
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import streamlit_authenticator as stauth
from device_dection import add_device_detection
from login import sign_up, fetch_users
import streamlit_authenticator as stauth

person_names = rpd.get_person_list(rpd.load_person_data())
# Führe die Geräteerkennungsfunktion aus
add_device_detection()


# Laden der Benutzerinformationen
try:
    users = fetch_users()

    # Extrahiere Benutzerinformationen aus der Datenbankabfrage
    usernames = [user['username'] for user in users.values()]
    passwords = [user['password'] for user in users.values()]

    credentials = {'usernames': {}}
    for user_id, user_data in users.items():
        credentials['usernames'][user_data['username']] = {
            'name': user_id,  # Verwende user_id als 'name' (besser wäre jedoch email oder eine eindeutige ID)
            'password': user_data['password']
        }

    # Initialisierung der Authenticator-Instanz mit fields-Argument
    fields = {
        'username': {'label': 'Username', 'type': 'text'},
        'password': {'label': 'Password', 'type': 'password'}
    }

    # Initialisierung der Authenticator-Instanz mit cookie_key-Argument
    cookie_key = 'abcdef'  # Ein zufällig generierter Schlüssel für Cookies
    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', cookie_key=cookie_key, cookie_expiry_days=4)

    # Login-Formular und Benutzerstatus überprüfen
    email, authentication_status, username = Authenticator.login(fields=fields)

    # Spalten für die Anzeige der Informationen
    info, info1 = st.columns(2)

    # Überprüfe den Authentifizierungsstatus und handle entsprechend
    if not authentication_status:
        sign_up()
    elif username:
        if username in usernames:
            if authentication_status:
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

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
                            if st.button("Graphen laden"):
                                fig = current_egk_data.make_plot()
                        # Zeige den Plot an 
                                st.plotly_chart(fig, use_container_width=True)




                #'''Zusatzaufgabe: Datenanalyse von fit-Dateien'''


                def tab2_content():
                    
                            st.header("Leistungsanalyse")

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                ftp = st.slider('FTP', 0, 500, 350)
                        


                            with col2:
                                max_hr = st.number_input('Geben Sie Ihre maximale Herzfrequenz ein:', min_value=0)

                            with col3:
                                weight = st.number_input('Geben Sie Ihr Körpergewicht in kg ein:', min_value=0)


                            st.title("FIT-Datei Drag-and-Drop")

                        # Datei-Uploader für FIT-Dateien
                            uploaded_file = st.file_uploader("Ziehe eine FIT-Datei hierher oder klicke, um eine Datei auszuwählen.", type=["fit"])

                            if uploaded_file is not None:
                        # Zeige Dateidetails an
                                st.write("Dateiname:", uploaded_file.name)
                                st.write("Dateigröße:", uploaded_file.size, "Bytes")

                        # Lade und analysiere die FIT-Datei
                                time_values, power_values, hr_values = fit.load_fitfile(uploaded_file)
                                # Berechne die fortlaufenden Bestwerte über alle Zeitintervalle
                                best_values = fit.calculate_continuous_best_values(time_values, power_values)
                                best_values_wkg = [(interval, power / weight if weight > 0 else 0) for interval, power in best_values]


                            if st.button("Graph laden"):
                                if ftp > 0 and max_hr > 0:
                                    # Erstelle einen Plotly-Graphen für die Leistungsdaten
                                    fig = fit.create_power_plot(time_values, power_values)
                                    st.plotly_chart(fig)

                                    # Berechne die Zeit in den verschiedenen Leistungszonen
                                    power_zones = fit.get_power_zones(ftp)
                                    time_in_power_zones = fit.calculate_time_in_zones(power_values, power_zones)

                                    # Berechne die Zeit in den verschiedenen Herzfrequenzzonen
                                    hr_zones = fit.get_heart_rate_zones(max_hr)
                                    time_in_hr_zones = fit.calculate_time_in_zones(hr_values, hr_zones)

                                    # Erstelle Balkendiagramme für die Zeit in den Zonen
                                    power_bar_chart = fit.create_time_in_zone_bar_chart(time_in_power_zones, 'Time in Power Zones')
                                    hr_bar_chart = fit.create_time_in_zone_bar_chart(time_in_hr_zones, 'Time in Heart Rate Zones')

                                    # Zeige die Balkendiagramme nebeneinander an
                                    col1, col2 = st.columns(2)
                                    col1.plotly_chart(power_bar_chart, use_container_width=True)
                                    col2.plotly_chart(hr_bar_chart, use_container_width=True)
                                else:
                                    st.error("Bitte geben Sie sowohl einen gültigen FTP-Wert als auch eine gültige maximale Herzfrequenz ein.")


                            # Auswahl der Darstellung für die Bestwerte (Watt oder W/kg) mit einem Toggle-Regler
                            if ftp > 0 and max_hr > 0 and uploaded_file is not None:
                                # display_mode = st.radio(
                                #     "Bestwerte anzeigen als:",
                                #     ("Watt", "W/kg"),
                                #     index=0,
                                #     horizontal=True
                                # )

                                # # Erstelle und zeige das Liniendiagramm für die Bestwerte basierend auf der Auswahl an
                                # if display_mode == "Watt":
                                #     best_values_plot = fit.create_continuous_best_values_plot(best_values)
                                # else:
                                #     best_values_plot = fit.create_continuous_best_values_plot(best_values_wkg)



                                display_mode = st.toggle("W/kg")

                                # Erstelle und zeige das Liniendiagramm für die Bestwerte basierend auf der Auswahl an
                                if display_mode:
                                    best_values_plot = fit.create_continuous_best_values_plot(best_values_wkg)
                                else:
                                    best_values_plot = fit.create_continuous_best_values_plot(best_values)

                                st.plotly_chart(best_values_plot)








                def main_page():
                                st.title('Datenauswertung')

                    # Tab-Titel definieren
                                tab_titles = ['EKG-Daten', 'Leistungsanalyse']

                    # Tabs erstellen
                                tabs = st.tabs(tab_titles)

                    # Inhalt für jeden Tab hinzufügen
                                with tabs[0]:
                                    tab1_content()

                                with tabs[1]:
                                    tab2_content()

                if __name__ == "__main__":
                            main_page()
            else:
                with info:
                    st.error('Incorrect Password or username')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')
    else:
        with info:
            st.warning('Please feed in your credentials')

except Exception as e:
    st.error(f'Error: {e}')
# Lade alle Personen



# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
#     login_page()

# if not st.session_state.logged_in:
#     st.sidebar.title("Login")
    
#     st.session_state.logged_in = True
#     st.sidebar.empty()

# else:
#     if st.session_state.logged_in:
    
    
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
                if st.button("Graphen laden"):
                    fig = current_egk_data.make_plot()
            # Zeige den Plot an 
                    st.plotly_chart(fig, use_container_width=True)




    #'''Zusatzaufgabe: Datenanalyse von fit-Dateien'''


    def tab2_content():
        
                st.header("Leistungsanalyse")
                st.write("test")

                col1, col2, col3 = st.columns(3)

                with col1:
                    ftp = st.number_input('Geben Sie Ihre Functional Threshold Power (FTP) ein:', min_value=0)
            


                with col2:
                    max_hr = st.number_input('Geben Sie Ihre maximale Herzfrequenz ein:', min_value=0)

                with col3:
                    weight = st.number_input('Geben Sie Ihr Körpergewicht in kg ein:', min_value=0)


                st.title("FIT-Datei Drag-and-Drop")

            # Datei-Uploader für FIT-Dateien
                uploaded_file = st.file_uploader("Ziehe eine FIT-Datei hierher oder klicke, um eine Datei auszuwählen.", type=["fit"])

                if uploaded_file is not None:
            # Zeige Dateidetails an
                    st.write("Dateiname:", uploaded_file.name)
                    st.write("Dateigröße:", uploaded_file.size, "Bytes")

            # Lade und analysiere die FIT-Datei
                    time_values, power_values, hr_values = fit.load_fitfile(uploaded_file)
                    # Berechne die fortlaufenden Bestwerte über alle Zeitintervalle
                    best_values = fit.calculate_continuous_best_values(time_values, power_values)
                    best_values_wkg = [(interval, power / weight if weight > 0 else 0) for interval, power in best_values]


                if st.button("Graph laden"):
                    if ftp > 0 and max_hr > 0:
                        # Erstelle einen Plotly-Graphen für die Leistungsdaten
                        fig = fit.create_power_plot(time_values, power_values)
                        st.plotly_chart(fig)

                        # Berechne die Zeit in den verschiedenen Leistungszonen
                        power_zones = fit.get_power_zones(ftp)
                        time_in_power_zones = fit.calculate_time_in_zones(power_values, power_zones)

                        # Berechne die Zeit in den verschiedenen Herzfrequenzzonen
                        hr_zones = fit.get_heart_rate_zones(max_hr)
                        time_in_hr_zones = fit.calculate_time_in_zones(hr_values, hr_zones)

                        # Erstelle Balkendiagramme für die Zeit in den Zonen
                        power_bar_chart = fit.create_time_in_zone_bar_chart(time_in_power_zones, 'Time in Power Zones')
                        hr_bar_chart = fit.create_time_in_zone_bar_chart(time_in_hr_zones, 'Time in Heart Rate Zones')

                        # Zeige die Balkendiagramme nebeneinander an
                        col1, col2 = st.columns(2)
                        col1.plotly_chart(power_bar_chart, use_container_width=True)
                        col2.plotly_chart(hr_bar_chart, use_container_width=True)
                    else:
                        st.error("Bitte geben Sie sowohl einen gültigen FTP-Wert als auch eine gültige maximale Herzfrequenz ein.")


                # Auswahl der Darstellung für die Bestwerte (Watt oder W/kg) mit einem Toggle-Regler
                if ftp > 0 and max_hr > 0 and uploaded_file is not None:
                    # display_mode = st.radio(
                    #     "Bestwerte anzeigen als:",
                    #     ("Watt", "W/kg"),
                    #     index=0,
                    #     horizontal=True
                    # )

                    # # Erstelle und zeige das Liniendiagramm für die Bestwerte basierend auf der Auswahl an
                    # if display_mode == "Watt":
                    #     best_values_plot = fit.create_continuous_best_values_plot(best_values)
                    # else:
                    #     best_values_plot = fit.create_continuous_best_values_plot(best_values_wkg)



                    display_mode = st.toggle("W/kg")

                    # Erstelle und zeige das Liniendiagramm für die Bestwerte basierend auf der Auswahl an
                    if display_mode:
                        best_values_plot = fit.create_continuous_best_values_plot(best_values_wkg)
                    else:
                        best_values_plot = fit.create_continuous_best_values_plot(best_values)

                    st.plotly_chart(best_values_plot)








    def main_page():
                    st.title('Datenauswertung')

        # Tab-Titel definieren
                    tab_titles = ['EKG-Daten', 'Leistungsanalyse']

        # Tabs erstellen
                    tabs = st.tabs(tab_titles)

        # Inhalt für jeden Tab hinzufügen
                    with tabs[0]:
                        tab1_content()

                    with tabs[1]:
                        tab2_content()

    if __name__ == "__main__":
                main_page()

# %% Herzrate bestimmen
# Schätze die Herzrate 
#current_egk_data.estimate_hr()
# Zeige die Herzrate an
#st.write("Herzrate ist: ", int(current_egk_data.heat_rate))