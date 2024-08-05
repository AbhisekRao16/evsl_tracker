import time
import pandas as pd
from DataCleaning import DataCleaning
from DataTracking import DataTracking
import logging as logging
import logging.config
# import logging.handlers
import numpy as np
# logging.getLogger("main")
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s : %(message)s",
        }
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "logs/sample-logs/main.log",
            "maxBytes": 1000,
            "backupCount": 5,
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["stderr", "file"],
        }
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger("root")
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
    (with old XOR logic)
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
    filtered_op=data_tracker.clear_residue()
    # print(filtered_op)
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
