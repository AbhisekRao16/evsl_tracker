from typing import Dict, Tuple, List
import pandas as pd
import logging as l
import numpy as np
from datetime import datetime

class DataTracking:
    threshold: float = 0.5

    def __init__(self, sensor_data: pd.DataFrame) -> None:
        self.sensor_data = sensor_data
        self.sensor_transitions: List[Tuple[str, str, float]] = []
        self.product_matches: dict = {}

    def get_sensor_state_transitions(self) -> List[Tuple[str, str, float]]:
        sensor_transitions: List[Tuple[str, str, float]] = []
        timestamps: np.array = np.array(pd.to_datetime(self.sensor_data.iloc[:, 0], format='%d.%m.%Y %H:%M:%S.%f'))

        for sensor_name in self.sensor_data.columns[1:]:
            readings: np.array = np.array(self.sensor_data[sensor_name])

            try:
                current_states: np.array = readings.astype(float) >= self.threshold
            except ValueError:
                l.error(f"Warning: Unexpected non-numeric value in column {sensor_name}")
                continue

            state_changes = np.diff(current_states.astype(int))
            in_indices = np.where(state_changes == 1)[0] + 1
            out_indices = np.where(state_changes == -1)[0] + 1

            for i in in_indices:
                sensor_transitions.append((sensor_name, "In", timestamps[i]))

            for i in out_indices:
                sensor_transitions.append((sensor_name, "Out", timestamps[i]))

        self.sensor_transitions = sensor_transitions
        return sensor_transitions


    '''
    oldcode odesnot satisfy conditions sent by Sai Sir(change functionality)
    
    '''

    # def match_products(self) -> pd.DataFrame:
    #     product_matches: Dict[str, List[float]] = {}
    #     current_product: Dict[str, np.datetime64] = {}

    #     last_entry_time = {}
    #     last_exit_time = {}
    #     previous_entry_time = None

    #     self.sensor_transitions.sort(key=lambda x: x[2])
    #     for sensor_name, state, timestamp in self.sensor_transitions:
    #         l.info(f"Processing transition: {sensor_name}, {state}, timestamp: {timestamp}")

    #         if state == "In":
    #             if previous_entry_time is not None:
    #                 last_entry = last_entry_time.get(sensor_name, np.datetime64('NaT'))

    #                 if timestamp <= last_entry:
    #                     l.error(f"Entry time for sensor {sensor_name} not greater than previous sensor's entry time.")
    #                     continue

    #             current_product[sensor_name] = np.datetime64(timestamp)
    #             last_entry_time[sensor_name] = np.datetime64(timestamp)
    #             previous_entry_time = np.datetime64(timestamp)
    #             self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))

    #         elif state == "Out":
    #             if sensor_name in current_product:
    #                 current_entry = current_product[sensor_name]

    #                 if timestamp <= current_entry:
    #                     l.error(f"Exit time for sensor {sensor_name} not greater than entry time.")
    #                     continue

    #             self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))
    #             current_product.pop(sensor_name, None)
    #             last_exit_time[sensor_name] = np.datetime64(timestamp)

    #     columns = ["Product"]
    #     for sensor in self.sensor_data.columns[1:]:
    #         columns.extend([f"{sensor} in", f"{sensor} out"])

    #     data = []
    #     num_products = len(self.sensor_transitions) // 2
    #     for product_id in range(num_products):
    #         row = [product_id + 1]
    #         for sensor_name in self.sensor_data.columns[1:]:
    #             if sensor_name in self.product_matches and len(self.product_matches[sensor_name]) > 2 * product_id + 1:
    #                 in_time = self.product_matches[sensor_name][2 * product_id]
    #                 out_time = self.product_matches[sensor_name][2 * product_id + 1]
    #             else:
    #                 in_time, out_time = None, None
    #             row.extend([in_time, out_time])
    #         data.append(row)

    #     df = pd.DataFrame(data, columns=columns)

    #     df = df.sort_values(by ="Product")
    #     df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_output_sample_ABHISEK.csv", index=False, date_format='%Y-%m-%d %H:%M:%S.%f')

    #     self.product_matches = product_matches

    #     print(df.head())
    #     return df.head()

    '''
    new approach almost same but satisfies condition1
    '''
    def match_products(self) -> pd.DataFrame:
        product_matches: Dict[str, List[float]] = {}
        current_product: Dict[str, np.datetime64] = {}

        last_entry_time = {}
        last_exit_time = {}
        previous_entry_time = None

        self.sensor_transitions.sort(key=lambda x: x[2])
        for sensor_name, state, timestamp in self.sensor_transitions:
            l.info(f"Processing transition: {sensor_name}, {state}, timestamp: {timestamp}")

            if state == "In":
                # Check if the entry time for the current sensor is greater than or equal to the previous sensor's entry time
                if previous_entry_time is not None and timestamp < previous_entry_time:
                    l.error(f"Entry time for sensor {sensor_name} not greater than previous sensor's entry time.")
                    continue

                current_product[sensor_name] = np.datetime64(timestamp)  # Update current product with sensor entry time
                last_entry_time[sensor_name] = np.datetime64(timestamp)  # Update last entry time for this sensor
                previous_entry_time = np.datetime64(timestamp)  # Update for next comparison
                self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))  # Add entry time to product matches

            elif state == "Out":
                if sensor_name in current_product:
                    current_entry = current_product[sensor_name]

                    # Ensure exit time is greater than entry time for the same sensor
                    if timestamp <= current_entry:
                        l.error(f"Exit time for sensor {sensor_name} not greater than entry time.")
                        continue

                    self.product_matches.setdefault(sensor_name, []).append(np.datetime64(timestamp))  # Add exit time to product matches
                    current_product.pop(sensor_name, None)  # Remove sensor from current product as it exited
                    last_exit_time[sensor_name] = np.datetime64(timestamp)  # Update last exit time for this sensor

        columns = ["Product"]
        for sensor in self.sensor_data.columns[1:]:
            columns.extend([f"{sensor} in", f"{sensor} out"])

        data = []
        num_products = len(self.sensor_transitions) // 2
        for product_id in range(num_products):
            row = [product_id + 1]
            for sensor_name in self.sensor_data.columns[1:]:
                if sensor_name in self.product_matches and len(self.product_matches[sensor_name]) > 2 * product_id + 1:
                    in_time = self.product_matches[sensor_name][2 * product_id]
                    out_time = self.product_matches[sensor_name][2 * product_id + 1]
                else:
                    in_time, out_time = None, None
                row.extend([in_time, out_time])
            data.append(row)

        df = pd.DataFrame(data, columns=columns)

        df = df.sort_values(by="Product")
        df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_out_put.csv", index=False, date_format='%Y-%m-%d %H:%M:%S.%f')
        self.product_matches = product_matches
        
        print(df.head())
        return df.head()
 


    def pad_lists(self) -> dict:
        fill_value = None
        max_len = 0

        if self.product_matches:
            max_len = max(len(l) for l in self.product_matches.values())

        return {key: value + [fill_value] * (max_len - len(value)) for key, value in self.product_matches.items()}




















































































































































# from typing import Dict, Tuple, List
# import pandas as pd
# import logging as l
# import numpy as np
# from datetime import datetime
# output=r"C:\Users\Abhishek\Desktop\evsl_tracker\output.csv"
# '''
# Code with the data matching algorithm (with type hinting)
# Includes two methods:
# one for tracking(get_sensor_state_transitions()) and the other one for matching(match_products())
# '''

# '''
# #TODO:
#         Exit time for a sensor should always be greater than the entry time.
#         Entry time for a sensor should always be greater than the entry time for the previous sensor.
# '''


# '''
# Logger configuration
# '''
# l.basicConfig(
#     level=l.INFO,  # Set logging level (e.g., INFO, WARNING, DEBUG)
#     filename="files_tracking.log", 
#     format='%(asctime)s - %(levelname)s - %(message)s')  # Customize log message format


# class DataTracking:
#     threshold: float = 0.5
#     '''
#     Takes clean data as input
#     '''

#     def __init__(self, sensor_data: pd.DataFrame) -> None:
#         """
#         :param sensor_data: DataFrame containing sensor data
#         Reads sensor data
#         """
#         self.sensor_data = sensor_data
#         self.sensor_transitions: List[Tuple[str, str, float]] = []
#         self.product_matches:dict={}
        
#     def get_sensor_state_transitions(self)->List[Tuple[str, str, float]]:
#         """ uses numerical array(np.array) which is used in place of old list[] based storage (optimized version)

#         Returns:
#             list  [str,str,float]
#         """        
#         sensor_transitions: List[Tuple[str, str, float]] = []
#         timestamps:np.array = np.array(self.sensor_data.iloc[:, 0])

#         for sensor_name in self.sensor_data.columns[1:]:
#             readings:np.array = np.array(self.sensor_data[sensor_name])

#             # Handle non-numeric values and convert to boolean array
#             try:
#                 current_states:np.array = readings.astype(float) >= self.threshold
#             except ValueError:
#                 l.error(f"Warning: Unexpected non-numeric value in column {sensor_name}")
#                 continue

#             # Detect changes in state
#             state_changes = np.diff(current_states.astype(int)) #converts to int value(bool to int )
#             in_indices = np.where(state_changes == 1)[0] + 1
#             out_indices = np.where(state_changes == -1)[0] + 1
#             # Append 'In' transitions
#             for i in in_indices:
#                 sensor_transitions.append((sensor_name, "In", timestamps[i]))

#             # Append 'Out' transitions
#             for i in out_indices:
#                 sensor_transitions.append((sensor_name, "Out", timestamps[i]))

#         self.sensor_transitions = sensor_transitions
#         # print(sensor_transitions)
#         return sensor_transitions
#     def match_products(self) -> pd.DataFrame:
#         product_matches: Dict[str, List[float]] = {}
#         current_product: Dict[str, float] = {}

#         last_entry_time = {}  # Added to track the last entry time for each sensor
#         last_exit_time = {}  # Added to track the last exit time for each sensor
#         previous_entry_time = None  # Added to track the entry time of the previous sensor

#         # Sort transitions to ensure the correct order
#         self.sensor_transitions.sort(key=lambda x: x[2])
#         for sensor_name, state, timestamp in self.sensor_transitions:
#             l.info(f"Processing transition: {sensor_name}, {state}, {timestamp}")

#             if isinstance(timestamp, str):
#                 timestamp = datetime.strptime(timestamp, "%d.%m.%Y %H:%M:%S.%f").timestamp()

#             if state == "In":
#                 if previous_entry_time is not None:
#                     last_entry = last_entry_time.get(sensor_name, 0)
#                     if isinstance(last_entry, str):
#                         last_entry = datetime.strptime(last_entry, "%d.%m.%Y %H:%M:%S.%f").timestamp()

#                     if timestamp <= last_entry:
#                         l.error(f"Entry time for sensor {sensor_name} not greater than previous sensor's entry time.")
#                         continue

#                 current_product[sensor_name] = timestamp
#                 last_entry_time[sensor_name] = timestamp
#                 previous_entry_time = timestamp
#                 self.product_matches.setdefault(sensor_name, []).append(timestamp)

#             elif state == "Out":
#                 if sensor_name in current_product:
#                     current_entry = current_product[sensor_name]
#                     if isinstance(current_entry, str):
#                         current_entry = datetime.strptime(current_entry, "%d.%m.%Y %H:%M:%S.%f").timestamp()

#                     if timestamp <= current_entry:
#                         l.error(f"Exit time for sensor {sensor_name} not greater than entry time.")
#                         continue

#                 self.product_matches.setdefault(sensor_name, []).append(timestamp)
#                 current_product.pop(sensor_name, None)
#                 last_exit_time[sensor_name] = timestamp
#                 '''
#                 to convert to df including sensor name and state at same place
#                 '''
#         # Convert to DataFrame with sensor name and state in the same place
#         columns = ["Product"]
#         for sensor in self.sensor_data.columns[1:]:
#             columns.extend([f"{sensor} in", f"{sensor} out"])

#         data = []
#         for sensor_name in self.sensor_data.columns[1:]:
#             if sensor_name not in product_matches or len(product_matches[sensor_name]) < 2:
#                 continue  # Skip if there are no matches or less than 2 transitions for this sensor

#             # Assuming each sensor has equal number of "In" and "Out" transitions
#             num_transitions = len(product_matches[sensor_name]) // 2

#             for product_id in range(num_transitions):
#                 row = [product_id + 1]
#                 in_time = product_matches[sensor_name][2 * product_id] if len(product_matches[sensor_name]) > 2 * product_id else None
#                 out_time = product_matches[sensor_name][2 * product_id + 1] if len(product_matches[sensor_name]) > 2 * product_id + 1 else None
#                 row.extend([in_time, out_time])
#                 data.append(row)
        
#         df = pd.DataFrame(product_matches, columns=columns)
#         # Ensure the data is correctly ordered
#         df = df.sort_values(by="Product")
#         # Save the DataFrame to CSV
#         df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\evsl_ouput_sample.csv", index=False)
#         self.product_matches = product_matches
#         '''
#         possibility of error ---1
#         '''
#         print(df.head())
#         return df.head()
    
#     def pad_lists(self)->dict:
#         """to make the df(out) have equal no. of rows

#         Returns:
#             dictionary
#         Pad lists in product_matches to have equal lengths.

#         Returns:
#             A dictionary with padded lists.
#         """
#         fill_value = None
#         max_len = 0

#         if self.product_matches:
#             max_len = max(len(l) for l in self.product_matches.values())

#         return {key: value + [fill_value] * (max_len - len(value)) for key, value in self.product_matches.items()}



































































