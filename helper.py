import string
import emoji
import pandas as pd
from collections import Counter

from urlextract import URLExtract
extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # 1. fetch total number of messages
    num_msg = df.shape[0]

    # 2. fetch total numbers of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. fetch the number of media messages
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch the number of links
    urls = []
    for message in df['message']:
       urls.extend(extractor.find_urls(message))

    return num_msg, len(words), num_media_msg, len(urls)

def most_active_users(df):
    x = df[df['user'] != 'group_notification']['user'].value_counts()
    active_users = x.head()
    new_df = round((df[df['user'] != 'group_notification']['user'].value_counts() / df.shape[0]) * 100,
                   2).reset_index().rename(columns={'user': 'Users', 'count': 'Percentage'})

    return active_users, new_df

def most_common_words(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # 1. remove group notification
    temp = df[df['user'] != 'group_notification']

    # 2. remove media omitted message
    temp = temp[temp['message'] != '<Media omitted>\n']

    # 3. remove the stop words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    # remove punctuations
    punct = string.punctuation
    temp['message'] = temp['message'].apply(lambda x: x.translate(str.maketrans('', '', punct)))

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for messages in df['message']:
        emojis.extend([c for c in messages if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0: 'Emojis', 1: 'Count'})

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # now we merge the year and the month
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_time = df.groupby(['dates']).count()['message'].reset_index()

    return daily_time

def active_weeks(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def active_months(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
