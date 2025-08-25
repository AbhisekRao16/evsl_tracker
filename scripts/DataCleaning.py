import pandas as pd
import logging as l

class DataCleaning:
    def __init__(self, sensor_data) -> None:
        self.df = None #drop and add
        self.sensor_data = sensor_data
        self.l = l.getLogger(__name__)

    def clean_data(self) -> pd.DataFrame:
        """
        func: cleans data pandas and gives required dataset in dataframe

        """
        try:
            # Read CSV data into a DataFrame (assuming comma-separated values)
            df = pd.read_csv(self.sensor_data, delimiter="\t")
            # Select required columns and handle potential errors
            required_columns = ["Time", "Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4",
                                "Sensor 5", "Sensor 6", "Sensor 7", "Sensor 8"]
            df = df[required_columns]
            df["Sensor 1"] = df["Sensor 1"].round().astype("Int64") #added this as some values got null or float values intead of integer
            self.df = df
            self.df.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\clean.csv")
            # print(df.dtypes)
            return self.df
        except FileNotFoundError as e:
            self.l.error(f"Sensor data file not found: {self.sensor_data}", exc_info=True)

        except pd.errors.ParserError as e:
            self.l.error(f"Error parsing sensor data: {e}", exc_info=True)
            raise ValueError(f"Error parsing sensor data: {e}") from e
