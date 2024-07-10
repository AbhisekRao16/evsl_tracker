from typing import Dict, Tuple, List
import pandas as pd
import logging as l

'''
Code with the data matching algorithm (with type hinting)
Includes two methods: one for tracking(get_sensor_state_transitions()) and the other one for matching(match_found())
'''

'''
Logger configuration
'''
l.basicConfig(
    level=l.INFO,  # Set logging level (e.g., INFO, WARNING, DEBUG)
    filename="files_tracking.log",format='%(asctime)s - %(levelname)s - %(message)s')  # Customize log message format


class DataTracking:
    threshold: float = 0.5

    '''
    Takes clean data as input
    '''

    def __init__(self, sensor_data: pd.DataFrame) -> None:
        """
        :param sensor_data: DataFrame containing sensor data
        Reads sensor data
        """
        self.sensor_data = sensor_data
        self.sensor_transitions: List[Tuple[str, str, float]] = []

    def get_sensor_state_transitions(self) -> List[Tuple[str, str, float]]:
        """
        Analyzes sensor readings and returns a list of sensor state transitions.

        Returns:
            list: A list of tuples containing (sensor_name, state, timestamp).
        """
        sensor_transitions: List[Tuple[str, str, float]] = []
        for sensor_name in self.sensor_data.columns[1:]:
            readings: List[float] = self.sensor_data[sensor_name].tolist()
            previous_state: int = 0
            for i, data in enumerate(readings):
                # Skip processing of timestamps (already in the first column)
                if i == 0:
                    continue

                try:
                    current_state: int = int(float(data) >= self.threshold)
                except ValueError:
                    l.error(f"Warning: Unexpected non-numeric value in column {sensor_name}")
                    continue

                state_change: int = current_state ^ previous_state
                if state_change:
                    timestamp: float = self.sensor_data.iloc[i, 0]
                    if current_state:
                        sensor_transitions.append((sensor_name, "In", timestamp))
                    else:
                        sensor_transitions.append((sensor_name, "Out", timestamp))
                previous_state = current_state

        self.sensor_transitions = sensor_transitions
        return sensor_transitions

    def match_products(self) -> Dict[Tuple[str, float], List[Tuple[str, str, float]]]:
        """
        Matches products based on sensor transitions.
        gives the  final state transition required 

        Returns:
            Dict[Tuple[str, float], List[Tuple[str, str, float]]]: Matched products with their transitions.
        """
        product_matches: Dict[Tuple[str, float], List[Tuple[str, str, float]]] = {}
        current_product: Tuple[str, float] = None

        for sensor_name, state, timestamp in self.sensor_transitions:
            l.info(f"Processing transition: {sensor_name}, {state, {timestamp}}")
            if state == "In":
                current_product = (sensor_name, timestamp)
                product_matches[current_product] = [(sensor_name, state, timestamp)]
            elif state == "Out" and current_product:
                if current_product[0] == sensor_name:
                    product_matches[current_product].append((sensor_name, state, timestamp))
                    current_product = None
        # print(product_matches)
        return product_matches