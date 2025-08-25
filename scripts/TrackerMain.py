import time
import pandas as pd
from DataCleaning import DataCleaning
from DataTracking import DataTracking
import logging as l
import pathlib as p


log_dir = p.Path(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "fileLog.log"

l.basicConfig(filename=log_path,filemode='w',format="%(asctime)s-%(levelname)s-%(message)s",level=l.INFO)


def main() -> None:
    start = time.time()
    sensor_data = r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\dataset\VariablesAndSensorsData_2hours.txt"  #path of the dataset
    output_file=r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\output_data\sample_1.csv"                        #output file path for final readings
    '''
    part1 of task--> cleaning
    
    (working)
    '''
    
    # Create DataCleaning object :
    data_cleaner = DataCleaning(sensor_data)
    # Call clean_data method to get the DataFrame and pass it to DataTracking
    dataframe1 = data_cleaner.clean_data()
    # print(dataframe1)
    # Pass the cleaned DataFrame dataframe1 to DataTracking
    data_tracker = DataTracking(dataframe1)
    # print(data_tracker)
    '''
    part2 of task --> listing out In and Out
    
    (working)
    '''
    #tracker method : it prints sensor states   (call transitions & print fn here itself)
    transitions:list = data_tracker.get_sensor_state_transitions()
    # print(transitions)
    for sensor_name, state, timestamp in transitions:
            print(f"  - Sensor: {sensor_name}, State: {state}, Timestamp: {timestamp} - ")
    '''
    part3 of task -->matching and tracing
    
    (working)
    
    '''
    
    match_found = data_tracker.match_products()
    if not match_found.empty:
        for key, value in match_found.items():
            print(f"{key} -> {value}")
    else:
        print("match not found")
    match_found.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\abhi.csv",index=False,
    date_format="%Y-%m-%d %H:%M:%S")
    # filtered_output:dict=data_tracker.pad_lists()
    # final_df=pd.DataFrame(filtered_output)
    # print(final_df.head())
    # final_df.to_csv(r"C:\Users\lenovo.LALITH\Desktop\projects\evsl_tracker\abhishek.csv",index=False)
    # pd.DataFrame(filtered_output.keys()).to_csv(r"C:\Users\Abhishek\Desktop\evsl_tracker\last.csv",index=False)
    # sensor_states_df = pd.DataFrame(columns=[])
    # filtered_op=data_tracker.clear_residue()
    # print(filtered_op)
    
    stop = time.time()  #source time
    print(stop - start)

if __name__ == "__main__":
    main()
# #TODO: cpython in place of python
