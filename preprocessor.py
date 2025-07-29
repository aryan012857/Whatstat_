import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}[   ]?[ap]m\s-\s'

    # Print all the messages
    messages = re.split(pattern, data)[1:]

    # Print all the dates
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract year from the date
    df['year'] = df['date'].dt.year

    # Extract month name from date
    df['month'] = df['date'].dt.month_name()

    # Extract day
    df['day'] = df['date'].dt.day

    # Extract hours
    df['hour'] = df['date'].dt.hour

    # Extract minutes
    df['minute'] = df['date'].dt.minute

    # Extract month number
    df['month_num'] = df['date'].dt.month

    # Extract only date
    df['dates'] = df['date'].dt.date

    # Extract day name from the date
    df['day_name'] = df['date'].dt.day_name()

    return df

