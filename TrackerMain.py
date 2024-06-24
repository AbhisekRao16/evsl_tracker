import time
from DataCleaning import DataCleaning
from DataTracking import DataTracking

#start time
t = time.time()



#path of the dataset
sensor_data = r"C:\Users\lenovo.LALITH\Desktop\voptimAI\sample-evonith\VariablesAndSensorsData_2hours.txt"

# Create DataCleaning object :data_cleaner
data_cleaner = DataCleaning(sensor_data)

# Call clean_data method to get the DataFrame and pass it to DataTracking
dataframe1 = data_cleaner.clean_data()
# Pass the cleaned DataFrame dataframe1 to DataTracking
data_tracker = DataTracking(dataframe1)
#tracker method : it prints sensor states
data_tracker.print_sensor_states(dataframe1)
#end time
s = time.time()
print(s - t)
#TODO: cpython in place of python