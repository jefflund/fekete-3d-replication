import time
import pandas
import datetime

#f - open("log_experiment.txt", 'r')

a = datetime.datetime.now()
b = datetime.datetime.now()
c = a-b
d = divmod(c.days * 86400 + c.seconds, 60)

fp = open("log_a.txt","w")
fp.write(str(a) + " - initial time" + "\n")
fp.write(str(b) + " - final time" + "\n")
fp.write(str(c) + " - diff time" + "\n")
fp.write(str(d) + " - diff in seconds" + "\n")
fp.close()

