

import datetime
import time

hour = "21"
min = "50"
sec = "30"
while(1):
    dt = datetime.datetime.now()
    if str(dt.hour)==hour:
        if str(dt.minute)==min:
            if str(dt.second) == sec:
                print(dt)
                time.sleep(1)
                break
            time.sleep(0.1)
        time.sleep(25)
    time.sleep(900)
