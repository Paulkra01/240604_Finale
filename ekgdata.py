import json
import pandas as pd
import numpy as np
import plotly as pl
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as subplots
# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    @staticmethod
    def load_by_id(search_id, ekg_test=1):
        file = open("data/person_db.json")
        person_data = json.load(file)
        if search_id == "None":
            return {}

        for person in person_data:
            for ekg_test in person["ekg_tests"]:
                if ekg_test["id"] == search_id:
                    return ekg_test


    # @staticmethod
    # def find_peaks(search_id, ekg_test=1,respacing_factor= 5, threshold= 0.5):
    
    #     file = open("data/person_db.json")
    #     person_data = json.load(file)
    #     if search_id == "None":
    #         return {}

    #     for person in person_data:
    #         for ekg_test in person["ekg_tests"]:
    #             if ekg_test["id"] == search_id:
    #                 result_link = pd.read_csv(ekg_test["result_link"], sep='\t', header=None, names=['Messwerte in mV','Zeit in ms'])
                    
    #     result_link = result_link.iloc[::respacing_factor]
        
    #     # # # Filter the series
    #     result_link = result_link[result_link>threshold]
    #     peaks = []
    #     last = 0
    #     current = 0
    #     next = 0

    #     for index, row in result_link.iterrows():
    #         last = current
    #         current = next
    #         next = row['Messwerte in mV']

    #         if last < current and current > next and current > threshold:
    #          peaks.append(index-respacing_factor)
    #     return peaks            


    @staticmethod
    def find_peaks(df, threshold=350):
        ekg_values = df["Messwerte in mV"].values
        peaks = []
        for i in range(1, len(ekg_values) - 1):
            if ekg_values[i] > ekg_values[i - 1] and ekg_values[i] > ekg_values[i + 1] and ekg_values[i] > threshold:
                peaks.append(i)
        peaks_index = pd.Index(peaks, dtype=int)
        df["Peaks"] = np.nan #notanumber
        df.loc[peaks_index, "Peaks"] = df.loc[peaks_index, "Messwerte in mV"]

        return df, peaks

    @staticmethod
    def estimate_hr(series, threshold=350):
        # peaks = EKGdata.find_peaks(peaks)
        # result_link = EKGdata.find_peaks(result_link)
        # time = int(len(result_link) / 1000 / 60)
        # heart_rate = len(peaks) / time

        series_with_peaks, peaks = EKGdata.find_peaks(series, threshold)
        series_with_peaks["HeartRate"] = np.nan
        peak_intervals = np.diff(peaks)
        sampling_rate = 1000 
        heart_rates = 60 / (peak_intervals / sampling_rate)
        for i, peak in enumerate(peaks[1:], start=1):
            series_with_peaks.at[peak, "HeartRate"] = heart_rates[i-1]      
        return series_with_peaks

    @staticmethod
    def plot_time_series(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df["Time in ms"], y = df["Messwerte in mV"], name="Messwerte in mV"))
        return fig

## Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.result_link = ekg_dict["result_link"]
        self.df = pd.read_csv(self.result_link, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.peaks = []

    def make_plot(self):
        df_peaks_heartrate = EKGdata.estimate_hr(self.df)
        fig = subplots.make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=('EKG Signal', 'Heart Rate'))

        # Plot EKG Signal
        fig.add_trace(go.Scatter(x=df_peaks_heartrate.index, y=df_peaks_heartrate["Messwerte in mV"], mode='lines', name='Messwerte in mV'),
                    row=1, col=1)
        # Plot Peaks
        fig.add_trace(go.Scatter(x=df_peaks_heartrate.index, y=df_peaks_heartrate["Peaks"], mode='markers', name='Peaks', marker=dict(color='red')),
                    row=1, col=1)

        # Plot Heart Rate (nur an den Positionen der Peaks)
        fig.add_trace(go.Scatter(x=df_peaks_heartrate.index, y=df_peaks_heartrate["HeartRate"], mode='markers', name='Heart Rate', marker=dict(color='blue')),
                    row=2, col=1)

        # Verbinde die Herzfrequenzwerte nur an den Peaks
        peak_indices = df_peaks_heartrate.dropna(subset=["HeartRate"]).index
        fig.add_trace(go.Scatter(x=peak_indices, y=df_peaks_heartrate.loc[peak_indices, "HeartRate"], mode='lines', name='Heart Rate (Line)', line=dict(color='green')),
                    row=2, col=1)

        # Update Layout
        fig.update_layout(height=600, width=800, title_text="EKG Signal and Heart Rate")
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Messwerte in mV", row=1, col=1)
        fig.update_yaxes(title_text="Heart Rate (BPM)", row=2, col=1)
        return fig




if __name__ == "__main__":
    # print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    # print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    # print(EKGdata.load_by_id(1))
    # print(EKGdata.find_peaks(1))

# %% Funktionen