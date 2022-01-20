import pandas as pd
import numpy as np
import re
import math
import sys
import os
import calendar
from datetime import datetime
import get_dates

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',100)

# df = pd.read_csv("/home/nonu/Desktop/data_/BN_FUT/_2020-01-01/BANKNIFTY-I.csv")
# print(df)
def SLhit(SL,Low):
    return SL>Low

def extract_time(timestamp):
    pattern = "(\d{2}:\d{2})"
    result = re.findall(pattern,timestamp)
    return result[0]

loc = "/home/nonu/Desktop/data_/BN_FUT/"
dates = get_dates.get_dates()

in_trade = False
prev_week_high = 0
curr_week_high = 10000000
capital = 450000
SL = 0
lots = 0
value = 0
prev_week_number = 0
curr_week_number = 1

l=[]


for date in dates:
    df = pd.read_csv(loc+date+"/"+"BANKNIFTY-I.csv")
    Day = df.at[1,'day_of_week']
    isexpiry = get_dates.check_expiry(df.at[1,"datetime"],df.at[1,"expiry_date"])
    curr_week_number = df.at[1,"week_number"]
    if curr_week_number!=prev_week_number:
        prev_week_number = curr_week_number
        prev_week_high = curr_week_high
        curr_week_high = 0

    metadata = {"Date":date,"Capital":0,"InTrade":in_trade,"Day":Day,"Closing":0,"PositionValue":0,"lots":0,"Expiry":isexpiry,"SL":SL,
                "currweekhigh":curr_week_high,"prevweekhigh":prev_week_high,"netvalue":capital+value}

    for idx,row in df.iterrows():
        if in_trade:
            if SLhit(SL,row["low"]):
                in_trade = False
                capital = capital + SL*lots
                lots = 0
                SL = 0
            else:
                if isexpiry:
                    Time = extract_time(row["datetime"])
                    if Time=="15:30":
                        df2 = pd.read_csv(loc+date+"/"+"BANKNIFTY-II.csv")
                        new_buy = df2["open"].iloc[-1]
                        capital = capital + row["open"]*lots
                        lots = capital//new_buy
                        capital = capital - new_buy*lots

            curr_week_high = max(curr_week_high,row["high"])


        else:
            Time = extract_time(row["datetime"])
            if Day=="Friday" and Time=="15:30":
                if row["open"]>prev_week_high:
                    lots = capital//row["open"]
                    capital = capital - lots*row["open"]
                    in_trade = True
                    SL = row["open"] - 0.02*row["open"]
            curr_week_high = max(curr_week_high, row["high"])

        value = row["close"]*lots

        metadata["Closing"] = row["close"]
    metadata["Capital"] = capital
    metadata["PositionValue"] = value
    metadata["lots"] = lots
    metadata["SL"] = SL
    metadata["InTrade"] = in_trade
    metadata["currweekhigh"] = curr_week_high
    metadata["prevweekhigh"] = prev_week_high
    metadata["netvalue"] =  capital + value

    print(metadata)
    l.append(metadata)

df = pd.DataFrame(l)
print(df)
df.to_excel("/home/nonu/Desktop/data_/"+"WeeklyPosSys.xlsx")




