import time
from DataCleaning import DataCleaning
from DataTracking import DataTracking
import logging as l

l.basicConfig(filename='files_tracking.log', 
              filemode='r',format="%(asctime)s-%(levelname)s-%(message)s",
              level=l.INFO)

def main() -> None:
    t = time.time()
    sensor_data = r"C:\Users\Abhishek\Desktop\evsl_tracker\VariablesAndSensorsData_2hours.txt"  #path of the dataset
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
    #tracker method : it prints sensor states   (call transitions & print fn here itself)
    transitions=data_tracker.get_sensor_state_transitions()
    '''
    part2 of task --> matching
    (working)
    '''
    # for sensor_name, state, timestamp in transitions:
    #         print(f"  - Sensor: {sensor_name}, State: {state}, Timestamp: {timestamp}")
    '''
    part3 of task -->tracing
    (issue with state_transitions variable)
    
    '''
    match_found = data_tracker.match_products()
    if match_found:
        for key, value in match_found.items():
            print(key, "->", value)
    else:
        print("match not found")
    s = time.time()  #source time
    print(s - t)


if __name__ == "__main__":
    main()
#TODO: cpython in place of python
