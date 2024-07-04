from DataCleaning import DataCleaning


#code with the data matching algorithm
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
                        sensor_states.append((sensor_name, "In", timestamp))
                    else:
                        timestamp = df.iloc[i, 0]
                        sensor_states.append((sensor_name, "Out", timestamp))
                previous_state = current_state

            # Matching entry and exit timestamps (highlighted section)
            if sensor_states:
                # Sort sensor states by timestamp
                sensor_states.sort(key=lambda x: x[2])

                # Iterate through states, matching entry with following exit
                for i in range(len(sensor_states)):
                    if sensor_states[i][1] == "In":
                        for j in range(i + 1, len(sensor_states)):
                            if sensor_states[j][0] == sensor_states[i][0] and sensor_states[j][1] == "Out":
                                entry_time = sensor_states[i][2]
                                exit_time = sensor_states[j][2]
                                print(f"Sensor number: {sensor_states[i][0]} - Entry: {entry_time}, Exit: {exit_time}")
                                break
                break
