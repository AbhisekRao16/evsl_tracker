from typing import Dict, Tuple, List
import pandas as pd
import logging as l
import numpy as np

'''
Code with the data matching algorithm (with type hinting)
Includes two methods:
one for tracking(get_sensor_state_transitions()) and the other one for matching(match_products())
'''

'''
Logger configuration
'''
l.basicConfig(
    level=l.INFO,  # Set logging level (e.g., INFO, WARNING, DEBUG)
    filename="files_tracking.log", 
    format='%(asctime)s - %(levelname)s - %(message)s')  # Customize log message format


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
        
    def get_sensor_state_transitions(self)->List[Tuple[str, str, float]]:
        """ uses numerical array(np.array) which is used in place of old list[] based storage (optimized version)

        Returns:
            list  [str,str,int]
        """        
        sensor_transitions: List[Tuple[str, str, float]] = []
        timestamps:np.array = np.array(self.sensor_data.iloc[:, 0])

        for sensor_name in self.sensor_data.columns[1:]:
            readings:np.array = np.array(self.sensor_data[sensor_name])

            # Handle non-numeric values and convert to boolean array
            try:
                current_states:np.array = readings.astype(float) >= self.threshold
            except ValueError:
                l.error(f"Warning: Unexpected non-numeric value in column {sensor_name}")
                continue

            # Detect changes in state
            state_changes = np.diff(current_states.astype(int)) #converts to int value(bool to int )
            in_indices = np.where(state_changes == 1)[0] + 1
            out_indices = np.where(state_changes == -1)[0] + 1

            # Append 'In' transitions
            for i in in_indices:
                sensor_transitions.append((sensor_name, "In", timestamps[i]))

            # Append 'Out' transitions
            for i in out_indices:
                sensor_transitions.append((sensor_name, "Out", timestamps[i]))

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
            l.info(f"Processing transition: {sensor_name}, {state, {timestamp} }")
            if state == "In":
                current_product = (sensor_name, timestamp)
                product_matches[current_product] = [(sensor_name, state, timestamp)]
            elif state == "Out" and current_product:
                if current_product[0] == sensor_name:
                    product_matches[current_product].append((sensor_name, state, timestamp))
                    current_product = None
        return product_matches
