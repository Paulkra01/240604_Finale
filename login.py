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
import streamlit_authenticator as stauth
import re
from deta import Deta
from pymongo import MongoClient
# Create a Deta instance
import re
import streamlit as st
from pymongo import MongoClient
# MongoDB Client Setup
client = MongoClient("mongodb+srv://jannisphl:Loewe2001@cluster0.woh3y3w.mongodb.net/")
db = client["meine_datenbank"]
collection = db["daten"]

def insert_user(email, username, password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items


def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        # Add User to DB
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(email, username, hashed_password[0])
                                        st.success('Account created successfully!!')
                                        st.balloons()
                                    else:
                                        st.warning('Passwords Do Not Match')
                                else:
                                    st.warning('Password is too Short')
                            else:
                                st.warning('Username Too short')
                        else:
                            st.warning('Username Already Exists')

                    else:
                        st.warning('Invalid Username')
                else:
                    st.warning('Email Already exists!!')
            else:
                st.warning('Invalid Email')

        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            st.form_submit_button('Sign Up')
#     # Button zum Einloggen
#         login_page = st.button("Login")
#     # Button zum Speichern eines neuen Benutzernamens
    
#     # Verarbeiten der Anmeldeinformationen, wenn der Button gedrückt wird
    
#         if login_page:
#         # Überprüfen, ob der Benutzername und das Passwort übereinstimmen
#             if username in person_names and password == "password":
#                 st.success("Erfolgreich eingeloggt")
#                 return username
#             else:
#                 st.error("Falscher Benutzername oder falsches Passwort")
#                 return "error"
           

# def login_tab2_content():
#     firstname = st.text_input("Vorname")
#     lastname = st.text_input("Nachname")
#     date_of_birth = st.number_input("Geburtsjahr", min_value=1900, max_value=2024, step=1)
#     # Funktion, um eine neue Person hinzuzufügen
#     save = st.button("Speichern")
#     if save:
#         if save:
#             # Erstellen eines neuen Person-Objekts mit den eingegebenen Daten
#             new_person = person.Person(
#             id=len(person_names) + 1,
#             date_of_birth=date_of_birth,
#             firstname=firstname,
#             lastname=lastname,
#             picture_path="data/pictures/tb.jpg",
#             ekg_tests=[]
#             )
            
#             # Hinzufügen des aktuellen Datums zum neuen Person-Objekt
#             current_date = datetime.date.today().strftime("%d.%m.%Y")
#             new_person.ekg_tests.append({
#             "id": len(person_names) + 1,
#             "date": current_date,
#             "result_link": "data/ekg_data/01_Ruhe.txt"
#             })
            
#             # Speichern des neuen Person-Objekts in der JSON-Datei
#             with open("path/to/your/json/file.json", "a") as file:
#                 json.dump(new_person.to_dict(), file)
#                 file.write("\n")
            
#             # Erfolgsmeldung anzeigen
#             st.success("Person erfolgreich gespeichert")
#             # Erstellen eines neuen Person-Objekts mit den eingegebenen Daten
#             new_person = person.Person(
#                 id=len(person_names) + 1,
#                 date_of_birth=date_of_birth,
#                 firstname=firstname,
#                 lastname=lastname,
#                 picture_path="data/pictures/tb.jpg",
#                 ekg_tests=[]
#             )
            
#             # Hinzufügen des aktuellen Datums zum neuen Person-Objekt
#             current_date = datetime.date.today().strftime("%d.%m.%Y")
#             new_person.ekg_tests.append({
#                 "id": 1,
#                 "date": current_date,
#                 "result_link": "data/ekg_data/01_Ruhe.txt"
#             })
            
#             # Speichern des neuen Person-Objekts in der JSON-Datei
#             with open("path/to/your/json/file.json", "a") as file:
#                 json.dump(new_person.to_dict(), file)
#                 file.write("\n")
            
#             # Erfolgsmeldung anzeigen
#             st.success("Person erfolgreich gespeichert")

   
 

    

# def login_page():

#     # Tab-Titel definieren
#     tab_titles = ['Benutzer aufrufen', 'Benutzer erstellen']

#     # Tabs erstellen
#     tabs = st.tabs(tab_titles)

#     # Inhalt für jeden Tab hinzufügen
#     with tabs[0]:
#         login_tab1_content()

#     with tabs[1]:
#         login_tab2_content()


