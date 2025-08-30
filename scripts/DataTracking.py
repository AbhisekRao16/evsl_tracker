import pandas as pd
import logging as l
import numpy as np

class DataTracking:
    threshold: float = 0.5
    def __init__(self, sensor_data: pd.DataFrame) : #dataframe from the datacleaning class
        self.sensor_data = sensor_data
        self.sensor_transitions: list = [] #list of transition for products based on time : In and Out
        self.product_matches: dict = {} #key: value pair : for a particular sensor In and Out are captured
        self.df=None
        self.l = l.getLogger(__name__)  # <-- add this
        self.l.setLevel(l.INFO)


    def __str__(self):
        return str(self.sensor_data)
    """
    for get_sensor_state_transitions()
    Detect state changes (In/Out) for each sensor over time.

    This method:
        - Converts the first column of self.sensor_data to datetime.
        - Thresholds each sensor column to ON/OFF using self.threshold.
        - Identifies times when a sensor switches ON ("In") or OFF ("Out").
        - Stores all transitions as tuples of (sensor_name, state, timestamp).
        - Sorts transitions chronologically and saves to self.sensor_transitions.

    Returns:
        list:
            A list of tuples in the form (sensor_name, "In"/"Out", timestamp).

    Notes:
        - If non-numeric values are present in a sensor column, that column is skipped.
        - If the first reading is ON, an initial "In" transition is added at the first timestamp.
    """
    def get_sensor_state_transitions(self) -> list:
        
            sensor_transitions: list = []

            # More robust timestamp parsing
            timestamps: np.array = pd.to_datetime(
                self.sensor_data.iloc[:, 0],
                errors='coerce'
            ).to_numpy()

            for sensor_name in self.sensor_data.columns[1:]:
                self.l.info(f"Processing sensor: {sensor_name}")
                readings: np.array = self.sensor_data[sensor_name].to_numpy()

                # Convert to float safely
                try:
                    current_states: np.array = readings.astype(float) >= self.threshold
                except ValueError:
                    self.l.error(f"Warning: Unexpected non-numeric value in column {sensor_name}")
                    continue

                # Add initial "In" if first reading already high
                if current_states[0]:
                    sensor_transitions.append((sensor_name, "In", timestamps[0]))

                # Detect state changes
                state_changes = np.diff(current_states.astype(int))
                in_indices = np.where(state_changes == 1)[0] + 1
                out_indices = np.where(state_changes == -1)[0] + 1

                for i in in_indices:
                    sensor_transitions.append((sensor_name, "In", timestamps[i]))
                for i in out_indices:
                    sensor_transitions.append((sensor_name, "Out", timestamps[i]))

            # Sort transitions chronologically
            sensor_transitions.sort(key=lambda x: x[2])

            self.sensor_transitions = sensor_transitions
            return sensor_transitions


    def match_products(self) -> pd.DataFrame:
        """
    Filter out products with negligible sensor times.

    This method:
        - Converts all in/out columns of self.df to datetime.
        - Calculates time differences (exit - entry) for each sensor.
        - Removes rows where time difference is less than 1 second.
        - Saves the filtered DataFrame to CSV and updates self.df.

    Returns:
        pd.DataFrame:
            Filtered DataFrame containing only valid rows.

    Notes:
        - Assumes self.df is already created by match_products().
        - Keeps only rows with realistic In/Out durations.
    """
        product_matches: dict = {}
        current_product: dict = {}
        previous_entry_time = None

        entry_time_errors = []
        exit_time_errors = []

        self.sensor_transitions.sort(key=lambda x: x[2])
        
        # Sort sensors from 8 to 1
        sensor_order = sorted(self.sensor_data.columns[1:], key=lambda x: int(x.split()[-1]), reverse=True)
        
        for sensor_name, state, timestamp in self.sensor_transitions:
            if state == "In":
                if previous_entry_time is not None and timestamp < previous_entry_time:
                    entry_time_errors.append((sensor_name, timestamp, previous_entry_time))
                    continue

                current_product[sensor_name] = np.datetime64(timestamp)
                previous_entry_time = np.datetime64(timestamp)
                self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))

            elif state == "Out":
                if sensor_name in current_product:
                    current_entry = current_product[sensor_name]

                    if timestamp <= current_entry:
                        exit_time_errors.append((sensor_name, timestamp, current_entry))
                        continue

                    self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))
                    current_product.pop(sensor_name, None)

        columns = ["Product"]
        for sensor in sensor_order:
            columns.extend([f"{sensor} in", f"{sensor} out"])

        data = []
        num_products = len(self.sensor_transitions) // 2
        for product_id in range(num_products):
            row = [product_id + 1]
            for sensor_name in sensor_order:
                if sensor_name in self.product_matches and len(self.product_matches[sensor_name]) > 2 * product_id + 1:
                    in_time = self.product_matches[sensor_name][2 * product_id]
                    out_time = self.product_matches[sensor_name][2 * product_id + 1]
                else:
                    in_time, out_time = None, None
                row.extend([in_time, out_time])
            data.append(row)

        df = pd.DataFrame(data, columns=columns)
        df = df.sort_values(by="Product")
        # df.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\evsl_out.csv", index=False, date_format='%Y-%m-%d %H:%M:%S.%f')
        self.product_matches = product_matches
        self.df=df
        # print(self.df.head())

        if entry_time_errors:
            print("Entry time errors:")
            for sensor_name, timestamp, previous_entry_time in entry_time_errors:
                print(f"Entry time for sensor {sensor_name} ({timestamp}) is not greater than previous sensor's entry time ({previous_entry_time}).")

        if exit_time_errors:
            print("Exit time errors:")
            for sensor_name, timestamp, current_entry in exit_time_errors:
                print(f"Exit time for sensor {sensor_name} ({timestamp}) is not greater than entry time ({current_entry}).")

        return df
    
    def clear_residue(self)->pd.DataFrame:
    # Assuming the DataFrame has columns for entry and exit times of each sensor
        '''
        filters out the values with smaller/negligible time difference
        returns: dataframe
        '''
        entry_columns = [col for col in self.df.columns if 'in' in col]
        exit_columns = [col for col in self.df.columns if 'out' in col]

        for entry_col, exit_col in zip(entry_columns, exit_columns):
            self.df = self.df.copy()
            self.df[entry_col] = pd.to_datetime(self.df[entry_col])
            self.df[exit_col] = pd.to_datetime(self.df[exit_col])
            
            # Calculate the time difference in seconds
            time_diff = (self.df[exit_col] - self.df[entry_col]).dt.total_seconds()
            
            # Filter out rows where the time difference is less than 1 second
            self.df = self.df[time_diff >= 1]
            # self.df.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\final_filter_check.csv",index=False)
        return self.df
