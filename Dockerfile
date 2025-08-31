#image of python (official)
FROM python:3.7 
#specify working directory inside the container :-/app
WORKDIR /app
#copy contents :- all first dot:-source, second dot:- location/desination
COPY . .
#run the cmds important to install dependencies
RUN pip install pandas prefect numpy
#run the final file
CMD ["python","TrackerMain.py"]