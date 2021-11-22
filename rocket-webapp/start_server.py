import subprocess
import threading
import time


def ping():
    while True:
        print("Pinging ...") # do actual API pinging stuff here
        time.sleep(10)

t = threading.Thread(target=ping)
t.start() # this will run the `ping` function in a separate thread

# now start the django server
subprocess.call(['python3', 'manage.py', 'runserver', '6002'])