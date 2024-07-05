from DataCleaning import DataCleaning
import logging as l
'''
code with the data matching algorithm(have included type hinting)
has two methods: one for tracking and other one for matching
TODO:pending task:tracing section
'''

<<<<<<< HEAD
l.basicConfig(
    level=l.INFO,  # Set logging level (e.g., INFO, WARNING, DEBUG)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize log message format
)
=======

#code with the data matching algorithm
>>>>>>> 010afcfcad907c01c11db0c1b1442103e698da74
class DataTracking(DataCleaning):
    threshold: float = 0.5

    def __init__(self, sensor_data) -> None:
        """
        :param sensor_data:
        reads sensor data
        """
        super().__init__(sensor_data)
        self.sensor_data = sensor_data

    def get_sensor_state_transitions(self) -> list[tuple[str, str, float]]:  #tracking
        """
        Analyzes sensor readings and returns a list of sensor state transitions.

        Returns:
            list: A list of tuples containing (sensor_name, state, timestamp).
        """
<<<<<<< HEAD
        sensor_transitions: list = []
        for sensor_name in self.sensor_data.columns[1:]:
            readings: list = self.sensor_data[sensor_name].tolist()
            previous_state: int = 0
=======

        for sensor_name in df.columns[1:]:  # Skip timestamp column
            readings = df[sensor_name].tolist()
            previous_state = 0  # Initialize previous state (0: below, 1: above)
            sensor_states = []
>>>>>>> 010afcfcad907c01c11db0c1b1442103e698da74
            for i, data in enumerate(readings):
                # Skip processing of timestamps (already in first column)
                if i == 0 and self.sensor_data.columns[0] == data:
                    continue

                try:
                    current_state: int = int(float(data) >= self.threshold)
                except ValueError:
                    print(f"Warning: Unexpected non-numeric value in column {sensor_name}")
                    self.logger.error(f"Sensor data file not found: {self.sensor_data}", exc_info=True)
                    continue

                state_change: int = current_state ^ previous_state
                if state_change:
                    if current_state:
<<<<<<< HEAD
                        timestamp: float = self.sensor_data.iloc[i, 0]
                        sensor_transitions.append((sensor_name, "In", timestamp))
                    else:
                        timestamp = self.sensor_data.iloc[i, 0]
                        sensor_transitions.append((sensor_name, "Out", timestamp))
=======
                        timestamp = df.iloc[i, 0]
                        sensor_states.append((sensor_name, "In", timestamp))
                    else:
                        timestamp = df.iloc[i, 0]
                        sensor_states.append((sensor_name, "Out", timestamp))
>>>>>>> 010afcfcad907c01c11db0c1b1442103e698da74
                previous_state = current_state
        return sensor_transitions

<<<<<<< HEAD
    def print_sensor_transitions(self, transitions: list[tuple[str, str, float]]) -> None:  #matching
        """
        Prints sensor state transitions in a user-friendly format.

        Args:
            transitions (list): A list of tuples containing (sensor_name, state, timestamp).
        """
        # l.INFO("info msg")
        if not transitions:
            print("No sensor state transitions found.")
            return
        try:
            for sensor_name, state, timestamp in transitions:
                print(f"Sensor number: {sensor_name} - {state}: {timestamp}")
        except ValueError as e:
            print(f"Warning: Unexpected non-numeric value ")

    def print_sensor_states(self) -> None:
        """
        Calls get_sensor_state_transitions and print_sensor_transitions methods.
        """
        transitions = self.get_sensor_state_transitions()
        self.print_sensor_transitions(transitions)
=======
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
>>>>>>> 010afcfcad907c01c11db0c1b1442103e698da74
