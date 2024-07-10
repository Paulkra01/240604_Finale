from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import read_person_data as rpd
import ekgdata as ekg
import datetime
import streamlit_authenticator as stauth
import re
from deta import Deta
from pymongo import MongoClient
# Create a Deta instance
import re
import streamlit as st
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import time
# MongoDB Client Setup
client = MongoClient("mongodb+srv://jannisphl:Loewe2001@cluster0.woh3y3w.mongodb.net/")
db = client["meine_datenbank"]
collection = db["daten"]



def insert_user(email, username, password):
    
    date_joined = str(datetime.datetime.now())

    return collection.insert_one({'email': email, 'username': username, 'password': password, 'date_joined': date_joined})

def fetch_users():
    try:
        # Alle Benutzer aus der Collection abrufen
        users = collection.find({})

        # Dictionary für die Benutzer initialisieren
        users_dict = {}

        # Daten in ein Dictionary umwandeln
        for user in users:
            users_dict[str(user.get('_id'))] = {
                'email': user.get('email'),
                'username': user.get('username'),
                'password': user.get('password'),
                'date_joined': user.get('date_joined')
            }

        return users_dict

    except Exception as e:
        print(f"Fehler beim Abrufen der Benutzer: {e}")
        return None

def get_user_emails():
    
    users = collection.find({})
    emails = []
    for user in users:
        emails.append(user.get('email'))
    return emails

def get_usernames():
    
    users = collection.find({})
    usernames = []
    for user in users:
        usernames.append(user.get('username'))
    return usernames

def validate_email(email):
    
    return True
    # return False

def validate_username(username):
    
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Profil erstellen]')
        email = st.text_input(':blue[Email]', placeholder='Email eingeben')
        username = st.text_input(':blue[Username]', placeholder='Gewünschten Username eingeben')
        password1 = st.text_input(':blue[Password]', placeholder='Passwort eingeben', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Passwort bestätigen', type='password')
        button = st.form_submit_button()
        if email and username and password1 and password2:
            if validate_email(email):
                emails = get_user_emails()
                if email not in emails:
                    if validate_username(username):
                        usernames = get_usernames()
                        if username not in usernames:
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        if button:
                                            # Add User to DB
                                            hashed_password = password2
                                            insert_user(email, username, hashed_password)
                                            with st.spinner('Account wird erstellt...'):
                                                time.sleep(2)
                                                
                                            st.success('Account erfolgreich erstellt !!')
                                            # st.balloons()
                                    else:
                                        st.warning('Passwort stimmt nicht überein')
                                else:
                                    st.warning('Passwort zu kurz')
                            else:
                                st.warning('Username zu kurz')
                        else:
                            st.warning('Username existirt bereits')
                    else:
                        st.warning('falscher Username')
                else:
                    st.warning('Email existiert bereits !')
            else:
                st.warning('falsche Email-Adresse')
        else:
            st.warning('Bitte alle Felder ausfüllen')

        



