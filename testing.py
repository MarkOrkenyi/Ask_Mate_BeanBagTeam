import datetime
import time
time_ = time.time()
print(time_)
# decode
dt_time = datetime.datetime.fromtimestamp(time_)
print(dt_time)
stringtime = datetime.datetime.strftime(dt_time, ("%Y-%m-%d %H:%M:%S"))
print(stringtime)
# encode
dt_time_e = datetime.datetime.strptime(stringtime, ("%Y-%m-%d %H:%M:%S"))
print(dt_time_e)
tuple_ = dt_time_e.timetuple()
print(tuple_)
timestamp = time.mktime(tuple_)
print(timestamp)
print("********************************")
