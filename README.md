
# Streamlit Dashboard README

## Technische Punkte

### Profilverwaltung
- **Welcome Page mit Login-Option:**
  - Eingabefelder für Name und Geburtsjahr
  - Falls das Profil nicht vorhanden ist, wird ein neues Profil im Dictionary abgespeichert


### Tab1: Main Dashboard
- Nach erfolgreichem Login wird das Hauptdashboard angezeigt
- Verkürzen der Ladezeiten
- Anzeigen des Profilbildes im Dashboard
- Detailinformationen als Hover-Funktion verfügbar (ID, Geburtsdatum)
- Schieberegler zur Bestimmung des darzustellenden Zeitraums


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
    
### Drag and Drop / Upload-Button
- Implementieren einer Drag-and-Drop-Funktionalität, um Benutzerinteraktionen zu erleichtern
- Erstellen einer Dropbox in beiden Tabs inklusive "clear"-Funktion

## Gestalterische Punkte

### Mobile Ansicht
- Optimierung für die Ansicht auf mobilen Geräten
- Integrierter "Back-to-Top"-Button für eine verbesserte Navigation

### Benutzerfreundlichkeit
- **Welcome Page:**
  - Einfache und intuitive Benutzerführung für den Login-Prozess
- **Profilinformationen:**
  - Klar dargestellte Profilbilder und detaillierte Informationen beim Hover
- **Tab2: Eingabefelder und Analysen:**
  - Benutzerfreundliche Eingabefelder für Gewicht und FTP-Werte
  - übersichtlich dargestellte Analyseergebnisse

### Interaktive Elemente
- **Zoom-Option:**
  - Interaktive Zoom-Funktion bei der Liste der Maximal-/Bestwerte

