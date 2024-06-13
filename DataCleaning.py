import pandas as pd


class DataCleaning:
    def __init__(self, sensor_data):
        self.df = None
        self.sensor_data = sensor_data

    def clean_data(self):
        df = pd.read_csv(self.sensor_data, delimiter="\t")
        required_columns = ["Time", "Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7",
                            "Sensor 8"]
        df = df[required_columns]
        self.df = df

        return self.df
