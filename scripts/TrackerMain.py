import time
import pandas as pd
from DataCleaning import DataCleaning
from DataTracking import DataTracking
import logging as l
import pathlib as p
import prefect as pr

log_dir = p.Path(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "fileLog.log"

l.basicConfig(filename=log_path,filemode='w',format="%(asctime)s-%(levelname)s-%(message)s",level=l.INFO)


def main() -> None:
    start = time.time()
    sensor_data = r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\dataset\VariablesAndSensorsData_2hours.txt"  #path of the dataset
    # output_file=r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\sample_1.csv"                        #output file path for final readings
    '''
    part1 of task--> cleaning
    
    (working)
    '''
    
    # Create DataCleaning object :
    data_cleaner = DataCleaning(sensor_data) #object:data_cleaner
    # Call clean_data method to get the DataFrame and pass it to DataTracking
    dataframe1 = data_cleaner.clean_data()
    dataframe1.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\clean_data\clean.csv",index=False,date_format="%Y-%m-%d %H:%M:%S")
    # print(dataframe1)
    # Pass the cleaned DataFrame dataframe1 to DataTracking
    data_tracker = DataTracking(dataframe1) #data__tracker: object
    # print(data_tracker)
    '''
    part2 of task --> listing out In and Out
    
    (working)
    '''
    #tracker method : it prints sensor states   (call transitions & print fn here itself)
    transitions:list = data_tracker.get_sensor_state_transitions()
    # print(transitions)
    for sensor_name, state, timestamp in transitions:
            l.info(f"  - Sensor: {sensor_name}, State: {state}, Timestamp: {timestamp} - ")
    '''
    part3 of task -->matching and tracing
    
    (working)
    
    '''
    
    match_found:pd.Dataframe = data_tracker.match_products()
    if not match_found.empty:
        for key, value in match_found.items():
            l.info(f"{key} -> {value}")
    else:
        l.error("match not found")
    match_found.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\tracked_data\match_products.csv",index=False,date_format="%Y-%m-%d %H:%M:%S")
    '''
    get the final required output as a dataframe converted into a csv file :final_output.csv

    '''

    filtered_op:pd.DataFrame=data_tracker.clear_residue()
    filtered_op.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\tracked_data\final_output.csv",index=False,date_format="%Y-%m-%d %H:%M:%S")
    # print(filtered_op)
    
    stop = time.time()  #source time
    print(f"batch processing time: {stop - start}")

if __name__ == "__main__":
    main()
# #TODO: cpython in place of python
