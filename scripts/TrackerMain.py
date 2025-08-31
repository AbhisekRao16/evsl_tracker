import time
import pandas as pd
import logging as l
import pathlib as p
from DataCleaning import DataCleaning
from DataTracking import DataTracking
from prefect import flow, task

# Setup logging
log_dir = p.Path(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "fileLog.log"

l.basicConfig(filename=log_path, filemode='w', 
              format="%(asctime)s-%(levelname)s-%(message)s", 
              level=l.INFO)

sensor_data_path = r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\dataset\VariablesAndSensorsData_2hours.txt"

@task
def clean_data_task(sensor_data: str) -> pd.DataFrame:
    data_cleaner = DataCleaning(sensor_data) #object creation
    df = data_cleaner.clean_data()
    output_path = r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\clean_data\clean.csv"
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    return df

@task
def track_transitions_task(df: pd.DataFrame)-> list:
    data_tracker = DataTracking(df) #object creation
    transitions = data_tracker.get_sensor_state_transitions()
    for sensor_name, state, timestamp in transitions:
        l.info(f"Sensor: {sensor_name}, State: {state}, Timestamp: {timestamp}")
    return data_tracker

@task
def match_and_trace_task(data_tracker: DataTracking) -> pd.DataFrame:
    match_found = data_tracker.match_products() #object creation
    if not match_found.empty:
        for key, value in match_found.items():
            l.info(f"{key} -> {value}")
    else:
        l.error("match not found")
    output_path = r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\tracked_data\match_products.csv"
    match_found.to_csv(output_path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    return match_found

@task
def create_final_output_task(data_tracker: DataTracking)->pd.DataFrame:
    filtered_op = data_tracker.clear_residue()
    output_path = r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\tracked_data\final_output.csv"
    filtered_op.to_csv(output_path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    return filtered_op

@flow(name="evsl-tracker-flow")
def main():
    start = time.time()
    df = clean_data_task(sensor_data_path)
    data_tracker = track_transitions_task(df)
    match_and_trace_task(data_tracker)
    create_final_output_task(data_tracker)
    stop = time.time()
    print(f"batch processing time: {stop - start}")

if __name__ == "__main__":
    main()

