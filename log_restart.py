import datetime
import time


import time
from datetime import datetime

# Get the current timestamp
timestamp = time.time()
# Convert the timestamp to a datetime object
current_datetime = datetime.fromtimestamp(timestamp)
# Print the current date and time
data = (f"restart at: , {current_datetime}\n")
f = open('log_restart.txt','a')
f.write(str(data))
f.close()
