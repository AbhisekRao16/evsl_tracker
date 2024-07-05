import pandas as pd

import logging as l
class DataCleaning:
    def __init__(self, sensor_data) -> None:
        self.df = None
        self.sensor_data= sensor_data
        self.logger = l.getLogger(__name__)

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
            self.df = df
            return self.df
        except FileNotFoundError as e:
            self.logger.error(f"Sensor data file not found: {self.sensor_data}", exc_info=True)
            raise
        except pd.errors.ParserError as e:
            self.logger.error(f"Error parsing sensor data: {e}", exc_info=True)
            raise ValueError(f"Error parsing sensor data: {e}") from e