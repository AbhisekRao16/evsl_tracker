import pandas as pd

from DataCleaning import DataCleaning


class DataTracking(DataCleaning):
    threshold = 0.5

    def __init__(self, sensor_data):
        super().__init__(sensor_data)
        self.sensor_data = sensor_data

    def print_sensor_states(self, df):
        """
        Analyzes sensor readings from a DataFrame and prints In/Out transitions with timestamps for each sensor.

        Args:
            sensor_df (pd.DataFrame): A DataFrame containing sensor data with columns for sensor names and readings.
            timestamp_col_index (int, optional): The index of the column containing timestamps. Defaults to 0.
            :param df:
        """

        for sensor_name in df.columns[1:]:  # Skip timestamp column
            readings = df[sensor_name].tolist()
            previous_state = 0  # Initialize previous state (0: below, 1: above)
            sensor_states = []
            count = 0
            count_out = 0
            for i, data in enumerate(readings):
                # Skip processing of timestamps (already in first column)
                if i == 0 and df.columns[0] == data:
                    continue

                try:
                    current_state = int(float(data) >= self.threshold)  # Convert reading to 0 or 1
                except ValueError:
                    print(f"Warning: Unexpected non-numeric value in column {sensor_name}")
                    continue

                state_change = current_state ^ previous_state  # XOR detects transition (0^1 or 1^0)
                if state_change:
                    if current_state:
                        timestamp = df.iloc[i, 0]
                        sensor_states.append(f"Sensor: {sensor_name} - In ({timestamp})")
                        count = count + 1
                    else:
                        timestamp = df.iloc[i, 0]
                        sensor_states.append(f"Sensor: {sensor_name} - Out ({timestamp})")
                        count_out = count_out+1
                previous_state = current_state

            # Print only In/Out Times with timestamps for the current sensor
            if sensor_states:
                print(f"Sensor: {sensor_name}")
                # print("In/Out Times:")
                for state in sensor_states:
                    print(f"\t{state}")
            print(count)
            print(count_out)