import fitparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_fitfile(file):
    """Lade und analysiere eine FIT-Datei."""
    fitfile = fitparse.FitFile(file)

    # Initialisiere Listen zum Speichern von Zeit-, Leistungs- und Herzfrequenzwerten
    time_values = []
    power_values = []
    hr_values = []

    # Extrahiere die Daten aus der FIT-Datei
    for record in fitfile.get_messages('record'):
        record_dict = record.get_values()
        if 'timestamp' in record_dict and 'power' in record_dict:
            time_values.append(record_dict['timestamp'])
            power_values.append(record_dict['power'])
        if 'timestamp' in record_dict and 'heart_rate' in record_dict:
            hr_values.append(record_dict['heart_rate'])

    return time_values, power_values, hr_values

def create_power_plot(time_values, power_values):
    """Erstelle einen Plotly-Graphen für Leistungswerte."""
    df = pd.DataFrame({
        'Time': time_values,
        'Power': power_values
    })

    fig = px.line(df, x='Time', y='Power', title='Power über Zeit')
    return fig

def calculate_time_in_zones(values, zones):
    """Berechne die Zeit in den verschiedenen Zonen."""
    time_in_zones = {zone: 0 for zone in zones}

    for value in values:
        for zone, (lower, upper) in zones.items():
            if lower <= value < upper:
                time_in_zones[zone] += 1
                break

    # Konvertiere die Zeit in Sekunden zu Minuten
    time_in_zones = {zone: time / 60 for zone, time in time_in_zones.items()}
    return time_in_zones

def create_time_in_zone_bar_chart(time_in_zones, title, c=None):
    df = pd.DataFrame(list(time_in_zones.items()), columns=['Zone', 'Time (min)'])
    if c:
        fig = px.bar(df, x='Zone', y='Time (min)', title=title, labels={'Time (min)': 'Time (min)'}, color=c)
    else:
        fig = px.bar(df, x='Zone', y='Time (min)', title=title, labels={'Time (min)': 'Time (min)'})
    return fig

def get_power_zones(ftp):
    """Definiere die Leistungszonen nach Coggan basierend auf FTP."""
    zones = {
        'active recovery': (0, 0.55 * ftp),
        'endurance': (0.55 * ftp, 0.75 * ftp),
        'tempo': (0.75 * ftp, 0.90 * ftp),
        'threshold': (0.90 * ftp, 1.05 * ftp),
        'VO2max': (1.05 * ftp, 1.20 * ftp),
        'anaerobic': (1.20 * ftp, 1.50 * ftp),
        'neuromuscular': (1.50 * ftp, float('inf'))
    }
    return zones

def get_heart_rate_zones(max_hr):
    """Definiere die Herzfrequenzzonen basierend auf maximaler Herzfrequenz."""
    zones = {
        'Zone 1': (0, 0.60 * max_hr),
        'Zone 2': (0.60 * max_hr, 0.70 * max_hr),
        'Zone 3': (0.70 * max_hr, 0.80 * max_hr),
        'Zone 4': (0.80 * max_hr, 0.90 * max_hr),
        'Zone 5': (0.90 * max_hr, float('inf'))
    }
    return zones



def calculate_continuous_best_values(time_values, power_values):
    """Berechne fortlaufende Bestwerte für jedes mögliche Zeitintervall."""
    df = pd.DataFrame({
        'Time': time_values,
        'Power': power_values
    })
    
    max_interval = len(df)
    best_values = []

    for interval in range(1, max_interval + 1):
        rolling_mean = df['Power'].rolling(window=interval).mean().max()
        best_values.append((interval, rolling_mean))

    return best_values

def create_PC(best_values):
    """Erstelle ein Liniendiagramm der fortlaufenden Bestwerte über verschiedene Zeitfenster."""
    df = pd.DataFrame(best_values, columns=['Interval (s)', 'Best Power (W)'])
    # fig = px.line(df, x='Interval (s)', y='Best Power (W)', title='Fortlaufende Bestwerte über verschiedene Zeitfenster', labels={'Best Power (W)': 'Best Power (W)'})
    
    fig = px.area(df, x='Interval (s)', y='Best Power (W)', title='Fortlaufende Bestwerte über verschiedene Zeitfenster')
    fig.update_traces(fillcolor="rgba(185, 217, 230, 0.8)", line_color="rgba(93, 157, 181, 0.8)")
    
    fig.add_trace(go.Scatter(x=df['Interval (s)'], y=df['Best Power (W)'], name="Watt"))
    fig.update_layout(hovermode='x unified')
    
    fig.update_layout(
        xaxis_title="Time / s",
        yaxis_title="Power / W",
        # xaxis_type="log"
    )
    
    return fig