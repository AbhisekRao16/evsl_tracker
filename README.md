

---

# EVSL Tracker

Track sensor state transitions (In/Out) and match product movement using Python.
--------------------------------------------------------------------------------------

This project processes raw sensor data, cleans it, detects sensor state transitions, and matches products across multiple sensors. The results are stored in a structured CSV for further analysis.

The workflow consists of three main parts:

1. **Data Cleaning** – Load and format raw sensor data.
2. **Data Tracking** – Detect "In" and "Out" transitions for each sensor.
3. **Product Matching** – Build a time-matched table showing when products enter and exit each sensor.

---

## **Features**

* Cleans raw tab-separated sensor logs into a usable DataFrame.
* Detects ON/OFF transitions for each sensor using a configurable threshold.
* Matches products by aligning "In" and "Out" events chronologically.
* Exports results to CSV with timestamps in ISO format.
* Built-in logging for debugging.

---

## **Project Structure**

```
evsl_tracker/
│
├── DataCleaning.py       # Cleans and structures raw data
├── DataTracking.py       # Tracks transitions and matches products
├── main.py               # Runs the full workflow
│
├── dataset/
│   └── VariablesAndSensorsData_2hours.txt   # Sample raw sensor data
│
├── output_data/
│   └── evsl_out.csv      # Final matched results
│
├── logs/
│   └── fileLog.log       # Runtime logs
│
└── README.md             # Project documentation
```

---

## **Usage**

### **1. Prepare the dataset**

Place your raw sensor file (tab-separated) in the `dataset/` folder. Ensure it contains these columns:

```
Time, Sensor 1, Sensor 2, Sensor 3, Sensor 4, Sensor 5, Sensor 6, Sensor 7, Sensor 8
```

### **2. Run the main script**

```bash
python main.py
```

### **3. Output**

* Cleaned data is saved to:

  ```
  evsl_tracker/clean.csv
  ```
* Matched In/Out product data is saved to:

  ```
  evsl_tracker/abhi.csv
  ```
* Logs are written to:

  ```
  evsl_tracker/logs/fileLog.log
  ```

---

## **Code Workflow**

### **1. Data Cleaning**

* Loads tab-separated data.
* Keeps only required sensor columns.
* Converts inconsistent values in `Sensor 1` to integers.

### **2. Transition Detection**

* For each sensor, detects when state changes from OFF → ON ("In") or ON → OFF ("Out").
* Stores results as a chronological list of `(sensor_name, state, timestamp)`.

### **3. Product Matching**

* Aligns "In" and "Out" events to track products moving through sensors.
* Generates a DataFrame with columns:

  ```
  Product, Sensor 8 in, Sensor 8 out, ..., Sensor 1 in, Sensor 1 out
  ```

---

## **Example Output (CSV)**

```csv
Product,Sensor 8 in,Sensor 8 out,Sensor 7 in,Sensor 7 out,...
1,2025-08-25 10:00:00,2025-08-25 10:05:00,2025-08-25 10:06:00,2025-08-25 10:09:00,...
2,2025-08-25 10:10:00,2025-08-25 10:15:00,2025-08-25 10:16:00,2025-08-25 10:19:00,...
```

---

## **Logging**

The system logs key steps to `logs/fileLog.log`:

* Which sensors are processed.
* Any non-numeric readings skipped.
* Entry/exit time errors.



---


