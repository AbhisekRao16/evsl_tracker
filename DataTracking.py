import pandas as pd
import logging as logging
import numpy as np

class DataTracking:
    threshold: float = 0.5
    def __init__(self, sensor_data: pd.DataFrame) -> None:
        self.sensor_data = sensor_data
        self.sensor_transitions: list = []
        self.product_matches: dict = {}
        self.df=None

    def get_sensor_state_transitions(self) -> list:
        sensor_transitions = []
        timestamps = np.array(pd.to_datetime(self.sensor_data.iloc[:, 0], format='%d.%m.%Y %H:%M:%S.%f'))#convetrted tio timestamp to get familiar with values
        for sensor_name in self.sensor_data.columns[1:]:
            readings = np.array(self.sensor_data[sensor_name])
            previous_state = 0  # Initialize previous state (0: below, 1: above)
            for i, data in enumerate(readings):
                current_state = int(float(data) >= self.threshold)  # Convert reading to 0 or 1
                state_change = current_state ^ previous_state  # XOR detects transition (0^1 or 1^0)
                if state_change:
                    timestamp = timestamps[i]
                    if current_state:
                        sensor_transitions.append((sensor_name, "In", timestamp))
                    else:
                        sensor_transitions.append((sensor_name, "Out", timestamp))
                previous_state = current_state

        self.sensor_transitions = sensor_transitions
        return sensor_transitions
    
    def match_products(self) -> pd.DataFrame:
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
        df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_tracker_output_excel\evsl_out_ABHI.csv", index=False, date_format='%Y-%m-%d %H:%M:%S.%f')
        self.product_matches = product_matches
        self.df=df
        print(self.df.head())

        if entry_time_errors:
            print("Entry time errors:")
            for sensor_name, timestamp, previous_entry_time in entry_time_errors:
                print(f"Entry time for sensor {sensor_name} ({timestamp}) is not greater than previous sensor's entry time ({previous_entry_time}).")

        if exit_time_errors:
            print("Exit time errors:")
            for sensor_name, timestamp, current_entry in exit_time_errors:
                print(f"Exit time for sensor {sensor_name} ({timestamp}) is not greater than entry time ({current_entry}).")
                logging.info("entering value")
        return df.head()

    def pad_lists(self) -> dict:
        fill_value = None
        max_len = 0

        if self.product_matches:
            max_len = max(len(l) for l in self.product_matches.values())

        return {key: value + [fill_value] * (max_len - len(value)) for key, value in self.product_matches.items()}
   
    # def clear_residue(self):
    # # Assuming the DataFrame has columns for entry and exit times of each sensor
    #     '''
    #     filters out the values with smaller/negligible time difference
    #     returns: dataframe
    #     '''
    #     entry_columns = [col for col in self.df.columns if 'in' in col]
    #     exit_columns = [col for col in self.df.columns if 'out' in col]

    #     for entry_col, exit_col in zip(entry_columns, exit_columns):
    #         self.df[entry_col] = pd.to_datetime(self.df[entry_col])
    #         self.df[exit_col] = pd.to_datetime(self.df[exit_col])
            
    #         # Calculate the time difference in seconds
    #         time_diff = (self.df[exit_col] - self.df[entry_col]).dt.total_seconds()
            
    #         # Filter out rows where the time difference is less than 1 second
    #         self.df = self.df[time_diff >= 1]
    #         self.df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_tracker_output_excel\final_filter.csv",index=False)   
    #     return self.df
    def clear_residue(self):
        """
        Filters out timestamp pairs with a small time difference.
        """
        for sensor_name in self.sensor_data.columns[1:]:
            in_col = f"{sensor_name} in"
            out_col = f"{sensor_name} out"

            self.df[in_col] = pd.to_datetime(self.df[in_col])
            self.df[out_col] = pd.to_datetime(self.df[out_col])

           
            time_diff = (self.df[out_col] - self.df[in_col]).dt.total_seconds()


            indices_to_remove = time_diff[time_diff < 1].index  # Find indices where time difference is less than 1 second

            # Remove the corresponding in and out timestamps
            self.df.loc[indices_to_remove, in_col] = pd.NaT
            self.df.loc[indices_to_remove, out_col] = pd.NaT

        # Optionally, fill missing values or remove rows with all missing in/out pairs
        # self.df.fillna(value=pd.NaT, inplace=True)
        # self.df.dropna(subset=self.df.columns[1:], how='all', inplace=True)
        print(self.df)
        self.df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_tracker_output_excel\check.csv")
        return self.df