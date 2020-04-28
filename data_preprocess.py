import pandas as pd
import numpy as np
import os

# Finds all the csv files within the directory and stores them in a list
files = []
basepath = 'COVID-19/csse_covid_19_data/csse_covid_19_daily_reports'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)) and entry != '.gitignore' and entry != 'README.md':
        files.append(entry)

files.sort()

# The data headers changed in the csv files so this sets which one is what
pre_files = files[0:60]
post_files = files[60:]

# Declaring Variables
dates = []
total_cases = []
total_deaths = []
total_recovered = []
new_cases_per_day = []
deaths_per_day = []
recovered_per_day = []

# loops trough all the files in the directory pulling out the data needed.
for file in files:
    data = pd.read_csv(
        './COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/' + file)
    if file in pre_files:
        us = data['Country/Region'] == 'US'
        state = pd.notnull(data['Province/State'])
    elif file in post_files:
        us = data['Country_Region'] == 'US'
        state = pd.notnull(data['Province_State'])
    new_data = data[state & us]
    total_cases.append(new_data['Confirmed'].sum())
    total_deaths.append(new_data['Deaths'].sum())
    total_recovered.append(new_data['Recovered'].sum())
    if len(total_deaths) != 1:
        deaths_per_day.append(new_data['Deaths'].sum() - total_deaths[-2])
        new_cases_per_day.append(new_data['Confirmed'].sum() - total_cases[-2])
        recovered_per_day.append(
            new_data['Recovered'].sum() - total_recovered[-2])
    dates.append(file[:10])

df_all = pd.DataFrame(list(zip(dates, new_cases_per_day, deaths_per_day, recovered_per_day, total_cases, total_deaths, total_recovered)), columns=[
                      'Dates', 'New Cases Per Day', 'Deaths Per Day', 'Recovered Per Day', 'Total Cases', 'Total Deaths', 'Total Recovered'])

df_all.to_csv('./data/' + dates[-1] + '.csv', index=False, header=True)
