import time
from DataCleaning import DataCleaning
from DataTracking import DataTracking
import logging as l

l.basicConfig(filename='files_tracking.log', filemode='r',
              format="%(asctime)s-%(levelname)s-%(message)s",
              level=l.INFO)


# l.debug("This is a debug message.")
# l.info("This is an informational message.")
# l.warning("This is a warning message.")
# l.error("This is an error message.")
# l.critical("This is a critical message.")


def main() -> None:
    t = time.time()
    sensor_data = r"C:\Users\Abhishek\Desktop\evsl_tracker\VariablesAndSensorsData_2hours.txt"  #path of the dataset
    # Create DataCleaning object : 
    data_cleaner = DataCleaning(sensor_data)
    # Call clean_data method to get the DataFrame and pass it to DataTracking
    dataframe1 = data_cleaner.clean_data()
    # Pass the cleaned DataFrame dataframe1 to DataTracking
    data_tracker = DataTracking(dataframe1)
    #tracker method : it prints sensor states   (call transitions & print fn here itself)
    data_tracker.print_sensor_states()
    s = time.time()  #source time
    print(s - t)


if __name__ == "__main__":
    main()
#TODO: cpython in place of python
