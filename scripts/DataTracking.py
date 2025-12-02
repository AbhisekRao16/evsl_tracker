import pandas as pd
import logging as l
import numpy as np


class DataTracking:

    threshold: float = 0.5

    def __init__(self, sensor_data_df: pd.DataFrame):
        self.sensor_data = sensor_data_df
        self.sensor_transitions = []
        self.product_matches = {}
        self.df = None

        self.l = l.getLogger(__name__)
        self.l.setLevel(l.INFO)

    def __str__(self):
        return str(self.sensor_data)

    # --------------------------------------------------------
    # TRANSITION EXTRACTION
    # --------------------------------------------------------
    def get_sensor_state_transitions(self) -> list:

        transitions = []

        timestamps = pd.to_datetime(
            self.sensor_data.iloc[:, 0],
            errors='coerce'
        ).to_numpy()

        for sensor_name in self.sensor_data.columns[1:]:

            self.l.info(f"Processing sensor: {sensor_name}")

            readings = self.sensor_data[sensor_name].to_numpy()

            try:
                current_states = readings.astype(float) >= self.threshold
            except ValueError:
                self.l.error(f"Non-numeric values in column {sensor_name}")
                continue

            # Initial state
            if current_states[0]:
                transitions.append((sensor_name, "In", timestamps[0]))

            # State changes
            diff = np.diff(current_states.astype(int))
            ins = np.where(diff == 1)[0] + 1
            outs = np.where(diff == -1)[0] + 1

            for i in ins:
                transitions.append((sensor_name, "In", timestamps[i]))
            for i in outs:
                transitions.append((sensor_name, "Out", timestamps[i]))

        transitions.sort(key=lambda x: x[2])
        self.sensor_transitions = transitions
        return transitions

    # --------------------------------------------------------
    # MATCH PRODUCTS
    # --------------------------------------------------------
    def match_products(self) -> pd.DataFrame:

        current_product = {}
        previous_entry = None

        entry_errors = []
        exit_errors = []

        self.sensor_transitions.sort(key=lambda x: x[2])

        sensor_order = sorted(
            self.sensor_data.columns[1:],
            key=lambda x: int(x.split()[-1]),
            reverse=True
        )

        for sensor_name, state, timestamp in self.sensor_transitions:

            if state == "In":

                if previous_entry is not None and timestamp < previous_entry:
                    entry_errors.append((sensor_name, timestamp, previous_entry))
                    continue

                self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))
                current_product[sensor_name] = np.datetime64(timestamp)
                previous_entry = np.datetime64(timestamp)

            elif state == "Out":

                if sensor_name not in current_product:
                    continue

                entry_time = current_product[sensor_name]

                if timestamp <= entry_time:
                    exit_errors.append((sensor_name, timestamp, entry_time))
                    continue

                self.product_matches[sensor_name].append(np.datetime64(timestamp))
                current_product.pop(sensor_name, None)

        # Build DataFrame
        columns = ["Product"]
        for s in sensor_order:
            columns.extend([f"{s} in", f"{s} out"])

        num_products = len(self.sensor_transitions) // 2
        data = []

        for pid in range(num_products):
            row = [pid + 1]
            for s in sensor_order:
                if s in self.product_matches and len(self.product_matches[s]) > pid * 2 + 1:
                    row.extend([
                        self.product_matches[s][pid * 2],
                        self.product_matches[s][pid * 2 + 1]
                    ])
                else:
                    row.extend([None, None])
            data.append(row)

        self.df = pd.DataFrame(data, columns=columns)

        return self.df

    # --------------------------------------------------------
    # CLEAR RESIDUE
    # --------------------------------------------------------
    def clear_residue(self) -> pd.DataFrame:

        df = self.df.copy()

        entry_cols = [c for c in df.columns if "in" in c]
        exit_cols = [c for c in df.columns if "out" in c]

        final_mask = pd.Series([True] * len(df))

        # Build a single mask
        for e_col, o_col in zip(entry_cols, exit_cols):
            df[e_col] = pd.to_datetime(df[e_col])
            df[o_col] = pd.to_datetime(df[o_col])

            diff = (df[o_col] - df[e_col]).dt.total_seconds()
            valid = diff >= 1

            final_mask &= valid

        # Apply final mask once
        self.df = df[final_mask]
        return self.df
