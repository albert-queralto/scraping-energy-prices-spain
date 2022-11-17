import os
import sys
import datetime
import re
import pandas as pd

# Create list with all files in the save directory
path = "/home/albert/Desktop/Tipologia i cicle de vida de les dades/PRA1/"
full_path = os.path.join(path, 'data')
files = os.listdir(full_path)

for file in files:
    if file.endswith('.csv') and "renewable_generation" in file:
        energy_prices = pd.read_csv(os.path.join(full_path, f"{file}"), sep=",")

        print(energy_prices.columns)
        
        # combine as rows renewable generation (MW), wind generation, water generation into a single column and create a column that contains the column names
    
# # get the dates from the filenames in the full path folder
# dates = []
# for file in files:
#     date = re.findall(r'\d{1,2}-\d{1,2}-\d{4}', file)

#     # split date in day-month-year
#     day, month, year = date[0].split('-')
#     # add zero to the left of day and month if the length is not 2
#     if len(day) == 1:
#         day = '0' + day
#     if len(month) == 1:
#         month = '0' + month
#     # create date string
#     date = day + "-" + month + "-" + year
#     dates.append(date)

# # find missing dates in a period from 1-11-2020 to 31-10-2022
# start_date = datetime.date(2020, 11, 1)
# end_date = datetime.date(2022, 10, 31)
# delta = datetime.timedelta(days=1)
# dates_list = []
# while start_date <= end_date:
#     dates_list.append(start_date.strftime("%d-%m-%Y"))
#     start_date += delta

# # find the missing dates
# missing_dates = []
# for date_val in dates_list:
#     if date_val not in dates:
#         missing_dates.append(date_val)