import pandas as pd
import numpy as np

class ab:
    def __init__(self,path):
        self.path=path
        self.sensor_data=None
        self.sensor_transitions=[]
    
    def change_frame(self):
        df = pd.read_csv(self.path, delimiter="\t")
        colm= ["Time","Sensor 1","Sensor 2","Sensor 3","Sensor 4","Sensor 5","Sensor 6","Sensor 7","Sensor 8"]
        df=df[colm]
        self.sensor_data=df
        return self.sensor_data

    def get_sensor_state_transitions(self,sensor_data) -> list:
                threshold=0.5
                sensor_transitions: list = []

                # More robust timestamp parsing
                timestamps: np.array = pd.to_datetime(
                    sensor_data.iloc[:, 0],
                    errors='coerce'
                ).to_numpy()

                for sensor_name in sensor_data.columns[1:]:
                    print(f"Processing sensor: {sensor_name}")
                    readings: np.array = sensor_data[sensor_name].to_numpy()

                    # Convert to float safely
                    try:
                        current_states: np.array = readings.astype(float) >= threshold
                    except ValueError:
                        print(f"Warning: Unexpected non-numeric value in column {sensor_name}")
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

                # self.sensor_transitions = sensor_transitions
                return sensor_transitions

path= r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\dataset\VariablesAndSensorsData_2hours.txt"
Ab=ab(path)
sensor_data=Ab.change_frame()
sample_=Ab.get_sensor_state_transitions(sensor_data)
for i in sample:
    print(i," ")