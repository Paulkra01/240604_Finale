# DashboardProjekt

## Voraussetzungen

- Python (mindestens Version 3.6)
- Git

## Schritte zur Einrichtung

1. **Repository klonen**

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Virtuelle Umgebung erstellen und aktivieren**

    **Auf Windows:**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    **Auf macOS und Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Abhängigkeiten installieren**

    ```bash
    pip install -r requirements.txt
    ```

4. **Hauptskript ausführen**

    ```bash
    python main.py
    ```

## Hinweise

- Bei Problemen mit der Installation oder Ausführung, sicherstellen, dass alle Voraussetzungen erfüllt sind und die virtuelle Umgebung korrekt aktiviert ist.



# Ablauf Auf unserem Streamlit-Dashboard

## Login

### Profilverwaltung
- **Welcome Page mit Login-Option:**
  - Eingabefelder für Username und passwort
  - Falls das Profil nicht vorhanden ist, wird ein neues Profil im MongoDB (Atlas) angelegt mit
                - Email
                - Username
                - Passwort
                - Geburtsdatum
    (Falls das Profil erstellen nicht funktioniert gelangt man mit username: test und password: 123456 trotzdem auf das Hauptdashboard)
    (sollte aber funktionieren)


### Tab1: Main Dashboard
- Nach erfolgreichem Login wird das Hauptdashboard angezeigt
- leider konnten wir die langen Ladezeiten nicht verkürzen
- Anzeigen des Profilbildes im Dashboard



### Tab2: Leistungsanalyse fit-Datei
- **Gewicht Eingabefeld:**
  - Analyse der relativen Leistung in W/kg
- **FTP + maxHF Eingabefeld:**
  - zur "Time-In-Zone"-Analyse
- **Leistungskurve:**
  - Anzeige der Leistungskurve wahlweise in W oder W/kg
- **"Time-in-Zone" Analyse**
  - Zeit in Leistungszonen
  - Zeit in Herzfrequenzzonen
-**"Mit Hilfe der Schieberegler kann die eingefügte .fit datei personalisiert verändert werden"**
    
### Drag and Drop / Upload-Button
- Drag-and-Drop-Box, einfach ein fit-file hineinziehen (auch gerne das aus unserem Repository)
- "clear"-Funktion löscht das fit-file

## Gestalterische Punkte

### Mobile Ansicht
- Optimierung für die Ansicht auf mobilen Geräten mit add_device_dection Funktion
- Integrierter "Back-to-Top"-Button für eine verbesserte Navigation bei Tablets oder handys



