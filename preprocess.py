import pandas as pd
import re
from datetime import datetime

# Function to get time and date in the desired format
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

# Function to preprocess the data
def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\w{2}\]\s'  # Date-Time Pattern
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages,
                       'message_date': dates})

    df['message_date'] = df['message_date'].apply(lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # List of phrases that should be classified as 'Group Notification'
    group_notification_phrases = [
        'Messages and calls are end-to-end encrypted',
        'created this group', 'added you'
    ]

    users = []
    messages = []

    # Splitting the message to extract the user and message content
    for message in df['user_messages']:
        # Check if the message contains any of the predefined phrases
        if any(phrase in message for phrase in group_notification_phrases):
            users.append('Group Notification')
            messages.append(message)
        else:
            # Split the message to extract the user and message
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:
                users.append(entry[1])  # Add the user
                messages.append(entry[2])  # Add the message
            else:
                # For any other type of message (like notifications), we classify as 'Group Notification'
                users.append('Group Notification')
                messages.append(entry[0])

    # Adding the 'User' and 'Message' columns to the dataframe
    df['User'] = users
    df['message'] = messages

    # Function to clean the message (removing extra newline characters)
    def getstring(text):
        return text.split('\n')[0]

    # Apply the cleaning function to the message column
    df['message'] = df['message'].apply(lambda text: getstring(text))

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
