
# Streamlit Dashboard README

## Technische Punkte

### Profilverwaltung
- **Welcome Page mit Login-Option:**
  - Eingabefelder für Name und Geburtsjahr
  - Falls das Profil nicht vorhanden ist, wird ein neues Profil im Dictionary abgespeichert
  - Die Profil-ID wird in einer Selectbox angezeigt

### Tab1: Main Dashboard
- Nach erfolgreichem Login wird das Hauptdashboard angezeigt
- Verkürzen der Ladezeiten
- Anzeigen des Profilbildes im Dashboard
- Detailinformationen als Hover-Funktion verfügbar (ID, Geburtsdatum)
- Schieberegler zur Bestimmung des darzustellenden Zeitraums


### Tab2: Leistungsanalyse
- **Gewichtseingabefeld:**
  - Analyse der relativen Leistung in W/kg
- **FTP Eingabefeld:**
  - Zur "Time-In-Zone"-Analyse
- **Leistungskurve:**
  - Anzeige der Leistungskurve
- **Maximal-/Bestwerte Liste:**
  - Liste der Maximal- und Bestwerte aus der Datei
  - Zoom-Option bei Klick auf die Werte --> Darstellung der W
- **Leistungsverteilung Balkendiagramm**
  - inklusive Schieberegler zur Bestimmung der "Balkenbreite" (z.B. 25W)
    
### Drag and Drop
- Implementieren einer Drag-and-Drop-Funktionalität, um Benutzerinteraktionen zu erleichtern
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

