FROM python:3.7
WORKDIR /app
COPY . .
RUN pip install pandas prefect numpy
CMD ["python","TrackerMain.py"]