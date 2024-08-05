import pandas as pd
import numpy as np
import logging as logging

class DataTracking:
    threshold: float = 0.5

    def __init__(self, sensor_data: pd.DataFrame) -> None:
        self.sensor_data = sensor_data
        self.sensor_transitions: list = []
        self.product_matches: dict = {}
        self.df = None

    def get_sensor_state_transitions(self) -> list:
        sensor_transitions = []
        timestamps = np.array(pd.to_datetime(self.sensor_data.iloc[:, 0], format='%d.%m.%Y %H:%M:%S.%f'))
        for sensor_name in self.sensor_data.columns[1:]:
            readings = np.array(self.sensor_data[sensor_name])
            previous_state = 0
            for i, data in enumerate(readings):
                current_state = int(float(data) >= self.threshold)
                state_change = current_state ^ previous_state
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
        previous_entry_time = {}
        entry_time_errors = []
        exit_time_errors = []

        self.sensor_transitions.sort(key=lambda x: x[2])
        sensor_order = sorted(self.sensor_data.columns[1:], key=lambda x: int(x.split()[-1]), reverse=True)

        for sensor_name, state, timestamp in self.sensor_transitions:
            timestamp = np.datetime64(timestamp)
            if state == "In":
                prev_sensor_idx = sensor_order.index(sensor_name) + 1
                if prev_sensor_idx < len(sensor_order):
                    prev_sensor_name = sensor_order[prev_sensor_idx]
                    if prev_sensor_name in previous_entry_time and timestamp < previous_entry_time[prev_sensor_name]:
                        entry_time_errors.append((sensor_name, timestamp, previous_entry_time[prev_sensor_name]))
                        continue
                current_product[sensor_name] = timestamp
                previous_entry_time[sensor_name] = timestamp
                self.product_matches.setdefault(sensor_name, []).append(timestamp)

            elif state == "Out":
                if sensor_name in current_product:
                    current_entry = current_product[sensor_name]
                    if timestamp <= current_entry:
                        exit_time_errors.append((sensor_name, timestamp, current_entry))
                        continue
                    self.product_matches.setdefault(sensor_name, []).append(timestamp)
                    current_product.pop(sensor_name, None)

        columns = ["Product"]
        for sensor in sensor_order:
            columns.extend([f"{sensor} in", f"{sensor} out"])

        data = []
        num_products = len(self.sensor_transitions) // (2 * len(sensor_order))
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
        self.product_matches = product_matches
        self.df = df
        print(self.df.head())
        return df.head()

    def pad_lists(self) -> dict:
        fill_value = None
        max_len = 0

        if self.product_matches:
            max_len = max(len(l) for l in self.product_matches.values())

        return {key: value + [fill_value] * (max_len - len(value)) for key, value in self.product_matches.items()}

    def clear_residue(self):
        for sensor_name in self.sensor_data.columns[1:]:
            in_col = f"{sensor_name} in"
            out_col = f"{sensor_name} out"

            self.df[in_col] = pd.to_datetime(self.df[in_col])
            self.df[out_col] = pd.to_datetime(self.df[out_col])

            time_diff = (self.df[out_col] - self.df[in_col]).dt.total_seconds()

            indices_to_remove = time_diff[time_diff < 1].index

            self.df.loc[indices_to_remove, in_col] = pd.NaT
            self.df.loc[indices_to_remove, out_col] = pd.NaT

        self.df.fillna(value=pd.NaT, inplace=True)
        self.df.dropna(subset=self.df.columns[1:], how='all', inplace=True)
        print(self.df)
        self.df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_tracker_output_excel\abhisek_evsl.csv", index=False, date_format='%Y-%m-%d %H:%M:%S.%f')
        return self.df
