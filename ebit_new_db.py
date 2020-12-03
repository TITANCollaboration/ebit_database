from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')
# =======================================================
# Data connection to server
# Read username and password form external file "user.csv"
userpw_file = open('./user.csv')
user_pw = userpw_file.readline().split(',')
user, password = user_pw[0], user_pw[1]

# URL for local database
url_db = "postgres://" + user + ":" + password + "@titan24/ebit"

# SQL connection for database
engine = create_engine(url_db)
conn = engine.connect()

# ========================================================
# Data extraction from server
# Define Run number
run_id = 16

# Define a SQL query
# QUERY = "select data FROM mcs_data_types_mcs_measurement WHERE scan_index = " + str(sindex) + "ORDER BY step_index"
# QUERY = "select data FROM test1 WHERE scanid = " + str(sindex)

# Extract data from database, mcs_measurement table in this case.
data_query = ("select data FROM mcs_measurement where run_id = %d" % run_id)
data = pd.read_sql_query(data_query, engine)

# Convert into numpy array
# Data is received in dataframe format. Decouple it and convert to numpy array in a single step.
d = np.array(data[data.columns[0]][0])

# Extract dwell time
dwell_time_query = ("select dwell_time FROM mcs_measurement where run_id = %d" % run_id)
dwell_time = pd.read_sql_query(dwell_time_query, engine)
dwell_time = dwell_time[dwell_time.columns[0]].values[0]

# Define X-axis
# Dwell time is in nanosec. Divide by 1000 converts it to microsec.
x = dwell_time * np.linspace(1, len(d), len(d)) / 1000
plt.close('all')
plt.plot(x, d)
plt.show()
# def get_dims(spec):
#     return len(spec[spec.columns[0]][0])
#
#
# dwell_time = 0.08  # 80 ns
# spectrum_back = np.array(data[data.columns[0]][0])
# spectrum = np.array(data[data.columns[0]][1])
# spectrum_axis = np.arange(0, get_dims(data)) * dwell_time
# spectrum_clean = spectrum - spectrum_back
#
# plt.plot(spectrum_axis, spectrum, label='Data')
# plt.plot(spectrum_axis, spectrum_back, label='Background')
# plt.plot(spectrum_axis, spectrum_clean, label='Subtracted')
# plt.legend()
# plt.show()
# Close connection
conn.close()
