import pandas as pd
import numpy as np
import re
import math
import sys
import os
from datetime import datetime

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',100)


def get_dates():
    folder_name = "/home/nonu/Desktop/data_/BN_FUT"
    arr = os.listdir(folder_name)
    arr = sorted(arr)
    print(arr)
    return arr

def check_expiry(d1,d2):
    d1 = datetime.fromisoformat(d1)
    try:
        d = datetime.fromisoformat(d2)
    except:
        d = datetime.strptime(d2, '%m/%d/%Y')

    if d1.date()==d.date():
        return True
    return False



def main():
    print(check_expiry("2020-01-01 09:15:59","1/1/2020"))

if __name__=="__main__":
    main()