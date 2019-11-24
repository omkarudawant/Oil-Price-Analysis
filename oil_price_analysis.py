# Packages for analysing the dataset
from warnings import filterwarnings
filterwarnings('ignore')
from datetime import datetime, timedelta, date

import pandas as pd
import numpy as np


def get_details(csv_path, start_date, end_date, percent_change, weekday=0):
    """
    This function returns the dates, percent changes, prices, etc. based on the percent change value given as input.

    csv_path: String, path to the csv dataset file. (Note: The file should have only two columns named `DATE` and 
    the symbol name)
    start_date: String, starting date for look back
    end_data: String, ending date for look back
    percent_change: float, the percent change value for look back
    weekday: int, default: 0 (Monday), It ranges through 0 to 4 (Monday to Friday)
    """
    # Preprocessing the data
    data = pd.read_csv(csv_path, index_col=[0])
    data.index = pd.to_datetime(data.index)
    data['DCOILWTICO'] = data['DCOILWTICO'][data['DCOILWTICO'] != '.'].astype(
        'float32')
    data.dropna(inplace=True)

    # Feature generation
    data['Difference'] = data['DCOILWTICO'].diff(periods=1)
    data['Perc_diff'] = data['DCOILWTICO'].pct_change(periods=1) * 100
    data.fillna(0, inplace=True)
    data['Day'] = pd.to_datetime(data.index).day
    data['Month'] = pd.to_datetime(data.index).month
    data['Weekday'] = pd.to_datetime(data.index).dayofweek
    data['Year'] = pd.to_datetime(data.index).year

    # Get results
    if weekday != 0:
        result = list(data.loc[(data['Perc_diff'] >= percent_change)
                               & (data['Weekday'] == weekday)]
                      [start_date:end_date]['Perc_diff'].index)
    else:
        result = list(
            data.loc[(data['Perc_diff'] >=
                      percent_change)][start_date:end_date]['Perc_diff'].index)
    return [i.strftime('%Y-%m-%d') for i in result]


def get_change(data, period, date):
    end_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=period)
    value = round(data[date:str(end_date).split(' ')[0]].mean(), 4)
    up_by = round(data[date:], 2)

    print(
        f'From {date} to {str(end_date).split(" ")[0]} when oil goes up by {up_by} '
        + f'the next {period} days the price changes by {value}')


def get20_change(data, month, year):
    # Preprocessing the data
    data = pd.read_csv(data, index_col=[0])
    data.index = pd.to_datetime(data.index)
    data['DCOILWTICO'] = data['DCOILWTICO'][data['DCOILWTICO'] != '.'].astype(
        'float32')
    data.dropna(inplace=True)

    # Feature generation
    data['Difference'] = data['DCOILWTICO'].diff(periods=1)
    data['Perc_diff'] = data['DCOILWTICO'].pct_change(periods=1) * 100
    data.fillna(0, inplace=True)
    
    data['Day'] = pd.to_datetime(data.index).day
    data['Month'] = pd.to_datetime(data.index).month
    data['Year'] = pd.to_datetime(data.index).year
    
    price_at_20 = data[data['Month'] == month]
    price_at_20 = price_at_20[price_at_20['Year'] == year]
    price_at_20 = price_at_20[(price_at_20['Day'] > 16) & (price_at_20['Day'] <= 24)]
    print(price_at_20)


csv_path = input('Enter path to csv file: ')
start_date = input('Enter start date for loop back: ')
end_date = input('Enter end date for loop back: ')
percent_change = float(input('Enter the percet change in oil price: '))
weekday = int(input('Enter weekday: '))

month = int(input('Enter month to see changes on 20th day: '))
year = int(input('Enter year to see changes on 20th day: '))


df = pd.read_csv(csv_path, index_col=[0])
df.index = pd.to_datetime(df.index)
df['DCOILWTICO'] = df['DCOILWTICO'][df['DCOILWTICO'] != '.'].astype('float32')
df.dropna(inplace=True)
df['Difference'] = df['DCOILWTICO'].diff(periods=1)
df['Perc_diff'] = df['DCOILWTICO'].pct_change(periods=1) * 100
df.fillna(0, inplace=True)
df['Day'] = pd.to_datetime(df.index).day
df['Month'] = pd.to_datetime(df.index).month
df['Weekday'] = pd.to_datetime(df.index).dayofweek
df['Year'] = pd.to_datetime(df.index).year


r = get_details(csv_path=csv_path,
                start_date=start_date,
                end_date=end_date,
                percent_change=percent_change,
                weekday=weekday)

period = int(input('Enter the number of days you want to see ahead: '))

print(r)
for i in r:
    get_change(data=df[['DCOILWTICO', 'Difference','Perc_diff']], period=1, date=i)
    print()

p = get20_change(data=csv_path, month=month, year=year)


