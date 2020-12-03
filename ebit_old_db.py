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

# URL for local titan database
url_db = "postgres://" + user + ":" + password + "@localhost/titan"

# SQL connection for database
engine = create_engine(url_db)
conn = engine.connect()

# ========================================================
# Data extraction from server
ScanIndex = 7258  # Charge bred Cs
# Test case
# ScanIndex = 6937  # ; LIndex = 14.0; HIndex = 50;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
#
# ScanIndex = 6882  #; LIndex = 19.5; HIndex = 40;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
# ScanIndex = 6876; LIndex = 20; HIndex = 40;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed BNG';
# ScanIndex = 6874; LIndex = 20; HIndex = 40;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed BNG';
# ScanIndex = 6839; LIndex = 15; HIndex = 40;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
# ScanIndex = 6892; LIndex = 14.0; HIndex = 40;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
# ScanIndex = 6907; LIndex = 14.0; HIndex = 40;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
# ScanIndex = 6936; LIndex = 14.0; HIndex = 50;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
# ScanIndex = 6937; LIndex = 14.0; HIndex = 50;
# GraphTitleString = 'RFA measurement - ^{85}Rb Charge breed';
# ScanIndex = 7325; LIndex = 10.0; HIndex = 30.0;
# GraphTitleString = 'RFA measurement - ^{133}Cs Charge breed'
# ScanIndex = 7333; LIndex = 16.6; HIndex = 20.0;
# GraphTitleString = 'RFA measurement - ^{133}Cs Charge breed BNG ON ';
# ScanIndex = 7339; LIndex = 10.0; HIndex = 35.0;
# GraphTitleString = 'RFA measurement - ^{39}K Charge breed';
# ScanIndex = 7369; LIndex = 29.0; HIndex = 40.0;
# GraphTitleString = 'RFA measurement - ^{39}K Reflected beam';
# ScanIndex = 7390; LIndex = 31.0; HIndex = 34.0;
# GraphTitleString = 'RFA measurement - ^{39}K Reflected beam';% 31 May 2018';
# ScanIndex = 7442; LIndex = 30.0; HIndex = 34.0;
# GraphTitleString = 'RFA measurement - ^{39}K Reflected beam BNG';% 31 May 2018';

# Query for dimTransitPoint table
QUERY = "select data FROM mcs_data_types_mcs_measurement WHERE scan_index = " + str(ScanIndex) + "ORDER BY step_index"
data = pd.read_sql_query(QUERY, engine)


def get_dims(spec):
    return len(spec[spec.columns[0]][0])


dwell_time = 0.08  # 80 ns
spectrum_back = np.array(data[data.columns[0]][0])
spectrum = np.array(data[data.columns[0]][1])
spectrum_axis = np.arange(0, get_dims(data)) * dwell_time
spectrum_clean = spectrum - spectrum_back

plt.plot(spectrum_axis, spectrum, label='Data')
plt.plot(spectrum_axis, spectrum_back, label='Background')
plt.plot(spectrum_axis, spectrum_clean, label='Subtracted')
plt.legend()
plt.show()
# Close connection
conn.close()
