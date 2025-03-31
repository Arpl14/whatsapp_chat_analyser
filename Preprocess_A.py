
import pandas as pd
import re
from datetime import datetime

def gettimeanddate(string):
    # Remove the square brackets and the non-breaking space
    string = string.strip('[]').replace(' ', ' ')

    # Split the string by comma to get the date and time
    date, time = string.split(',')

    # Trim any extra spaces and remove trailing ']'
    time = time.strip().rstrip(']')

    # Convert the time to 24-hour format using datetime
    time_24hr = datetime.strptime(time, '%I:%M:%S %p').strftime('%H:%M')

    return date + " " + time_24hr

def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\w{2}\]\s'  # Date-Time Pattern
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages,
                       'message_date': dates})

    df['message_date'] = df['message_date'].apply(lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    # Splitting the message to extract the user and message content
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['User'] = users
    df['message'] = messages

    df['message'] = df['message'].apply(lambda text: text.split('\n')[0])

    df = df.drop(['user_messages'], axis=1)
    df = df[['message', 'date', 'User']]
    df = df.rename(columns={'message': 'Message', 'date': 'Date'})

    # Adding time and date-related features
    df['Only date'] = pd.to_datetime(df['Date']).dt.date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['Date']).dt.day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    return df