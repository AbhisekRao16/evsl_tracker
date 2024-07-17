import time
import pandas as pd
from DataCleaning import DataCleaning
from DataTracking import DataTracking
import logging as l
import numpy as np
l.basicConfig(filename='files_tracking.log',
              filemode='r', 
              format="%(asctime)s-%(levelname)s-%(message)s",
              level=l.INFO)
def main() -> None:
    start = time.time()
    sensor_data = r"C:\Users\Abhishek\Desktop\evsl_tracker\VariablesAndSensorsData_2hours.txt"  #path of the dataset
    output_file=r"C:\Users\Abhishek\Desktop\evsl_tracker\OutputFile.csv"                        #output file path for final readings
    '''
    part1 of tak--> cleaning and tracking based on "In" and "Out"
    
    (working)
    '''
    # Create DataCleaning object : 
    data_cleaner = DataCleaning(sensor_data)
    # Call clean_data method to get the DataFrame and pass it to DataTracking
    dataframe1 = data_cleaner.clean_data()
    # Pass the cleaned DataFrame dataframe1 to DataTracking
    data_tracker = DataTracking(dataframe1)
    '''
    part2 of task --> matching 
    
    (working)
    '''
    #tracker method : it prints sensor states   (call transitions & print fn here itself)
    transitions:list = data_tracker.get_sensor_state_transitions()
    # for sensor_name, state, timestamp in transitions:
    #         print(f"  - Sensor: {sensor_name}, State: {state}, Timestamp: {timestamp}")
    '''
    part3 of task -->tracing
    
    (working)
    
    '''
    match_found = data_tracker.match_products()
    filtered_output:dict=data_tracker.pad_lists()
    # final_df=pd.DataFrame(filtered_output)
    # final_df.to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\last_df_modified.csv",index=False)
    # pd.DataFrame(filtered_output.keys()).to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\last.csv",index=False)
    # sensor_states_df = pd.DataFrame(columns=[])
    if not match_found.empty:
        for key, value in match_found.items():
            print(f"{key} -> {value}")
    else: 
        print("match not found")
    
    stop = time.time()  #source time5
    print(stop - start)

if __name__ == "__main__":
    main()
#TODO: cpython in place of python
