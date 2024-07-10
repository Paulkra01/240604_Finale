from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import read_person_data as rpd
import ekgdata as ekg
import pandas as pd
import datetime
import fitdata as fit
st.set_page_config(layout="wide",page_title="Hauptseite", page_icon=":bar_chart:")
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
            'name': user_id,  
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
                st.sidebar.subheader(f'Herzlich Willkommen {username}')
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
                                current_year = datetime.datetime.now().year
                                age = current_year - int(person_birthyear)
                                st.write(f"Geburtsjahr: {person_birthyear}")
                                st.write(f"Alter: {age}")

                        # Öffne EKG-Daten
                        # TODO: Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
                        # Vergleiche Bild und Person 
                                current_egk_data = ekg.EKGdata(rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["ekg_tests"][0])

                                ekg_names = [ekg_test["result_link"].split("/")[-1].split(".")[0] for ekg_test in rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["ekg_tests"]]

                        # Selectbox für Auswahl des EKG-Tests erstellen
                                st.session_state.aktuelles_ekg = st.selectbox(
                                    'EKG',
                                    options = ekg_names, key="sbEKG")
                        
                        

                            with col3:

                        # Pfad zur Bilddatei
                                if st.session_state.aktuelle_versuchsperson in person_names:
                                    st.session_state.picture_path = rpd.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["picture_path"]

                                image = Image.open(st.session_state.picture_path)
                                st.image(image, caption=st.session_state.aktuelle_versuchsperson)
                        
     ### EKG-Daten als Matplotlib Plot anzeigen
                    # Nachdem die EKG, Daten geladen wurden
                    # Erstelle den Plot als Attribut des Objektes
                            if st.button("Graphen laden"):
                                fig = current_egk_data.make_plot()
                        # Zeige den Plot an 
                                st.plotly_chart(fig, use_container_width=True)




                #'''Zusatzaufgabe: Datenanalyse von fit-Dateien'''


                def tab2_content():
                    
                            st.header("Leistungsanalyse von Athlet*innen")

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                ftp = st.slider('ftp in W', 0, 500, 350)
                        


                            with col2:
                                max_hr = st.slider('max heartrate in bpm', 0, 240, 195)

                            with col3:
                                weight = st.slider('weight in kg:', 0, 200, 72)


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
                               



                                display_mode = st.toggle("W/kg")

                                # Erstelle und zeige das Liniendiagramm für die Bestwerte basierend auf der Auswahl an
                                if display_mode:
                                    best_values_plot = fit.create_PC(best_values_wkg)
                                else:
                                    best_values_plot = fit.create_PC(best_values)

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
                    st.error('Falsches Passwort')
        else:
            with info:
                st.warning('Username nicht gefunden')
    else:
        with info:
            st.warning('Bitte einloggen')

except Exception as e:
    st.error(f'Error: {e}')








    #

# %% Herzrate bestimmen
# Schätze die Herzrate 
#current_egk_data.estimate_hr()
# Zeige die Herzrate an
#st.write("Herzrate ist: ", int(current_egk_data.heat_rate))