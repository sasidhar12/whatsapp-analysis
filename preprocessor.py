import pandas as pd
import re
import emoji
from collections import Counter
def preprocess(data:str):

    # Reading Data from the file

    # removing any spaces
    data = data.strip()

    pattern = "\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s.[pm|am]"

    # splitting data based on pattern
    messages = re.split(pattern, data)[1:]

    # Extracting dates based on above pattern
    dates = re.findall(pattern, data)

    # Changing feature names
    df = pd.DataFrame({'user_message': messages, 'user_dates': dates})

    df['user_dates'] = pd.to_datetime(df['user_dates'])

    df.rename({'user_dates': 'dates'}, axis=1, inplace=True)

    users,messages = split_user_message(df)
    df['users'] = users
    df['users']=df['users'].str.strip(' ')
    df['message'] = messages
    df['message'] =df['message'].str.strip('- ')
    df['message']=df['message'].str.strip('\n')
    df.drop('user_message',axis=1,inplace=True)

    # updating Dates

    df['year'] = pd.DatetimeIndex(df['dates']).year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df.dates.dt.hour
    df['minute'] = df.dates.dt.minute

    return df



def split_user_message(df):
    users = []
    messages = []

    user_message_pattern = '-(.*?):'

    for message_ in df['user_message']:
        entry = re.split(user_message_pattern, message_)

        if entry[1:]:
            user = entry[1]
            msg = entry[2]

            users.append(user)
            messages.append(msg)
        else:
            users.append('group_notification')
            messages.append(entry[0])
    return users,messages

def fetch_unique_users(df):
    return df.users.unique()


def most_common_words(selected_user,df):
        stopwords=[]
        stopwords_list=[]
        with open("stopwords.txt",encoding="utf-8") as file:
            stopwords_data = file.read()
            stopwords = stopwords_data.split("\n")

        for word in stopwords:
            stopwords_list.append(word.strip(" "))

        # Remove Group notifications ex: group exit, group name changed
        # remove Media ommited
        # remove stop words
        word_list = []
        df = df[df['message'] != '<Media omitted>']
        df = df[df['message'] != 'You deleted this message']
        df["message"] = df.message.str.strip("\n").str.strip(" ")
        if selected_user != "Overall":

            temp_df= df[df['users']==selected_user]
            #temp_df = temp_df[temp_df['users'] != 'group_notification']
        else:
            temp_df = df.copy()

        for message in temp_df['message']:
            for word in message.lower().split(" "):
                if word not in stopwords_list:
                    word_list.append(word)

        return_df = pd.DataFrame(Counter(word_list).most_common(29))
        return_df.columns = ["Words", "Frequency"]
        return return_df


def extract_emoji(selected_user,df):
    if selected_user != 'Overall':
        emojis = []
        df = df[df.users == selected_user]
        for message in df.message:
            for word in message:
                if emoji.is_emoji(word):
                    emojis.extend(word)

        df = pd.DataFrame(Counter(emojis).most_common(20), columns=['Emoji', 'Frequency'])
    else:
        emojis = []
        for message in df.message:
            for word in message:
                if emoji.is_emoji(word):
                    emojis.extend(word)

        df = pd.DataFrame(Counter(emojis).most_common(20), columns=['Emoji', 'Frequency'])

    return df