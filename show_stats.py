from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import advertools
from PIL import ImageDraw
#Displays information about messages of user

def get_messages(df,selected_user):
    if selected_user == 'Overall':
        return len(df.message)
    else:
        return df[df['users']==selected_user].shape[0]

def count_words(df,selected_user):
    message_count = 0
    if selected_user == 'Overall':
        for message in df.message:
            message_count = message_count + len(message.split(' '))
        return message_count
    else:
        for message in df[df['users'] == selected_user].message:
            message_count = message_count + len(message.split(" "))
        return message_count

def count_media(df,selected_user):
    if selected_user == 'Overall':
        return df[df['message'] == '<Media omitted>'].shape[0]
    else:
        user = df[df['users'] == selected_user]
        user[user['message'] == "<Media omitted>"]
        return  user[user['message']=='<Media omitted>'].shape[0]
def extract_url(df,selected_user):
    extractor = URLExtract()
    links = extractor.find_urls(df.message.to_string())

    if selected_user == 'Overall':
        return len(links)
    else:
        data = df[df['users']==selected_user].message.to_string()
        return len(extractor.find_urls(data))

def fetch_busiest_users(df):
    user_info = df.users.value_counts().sort_values(ascending=False).head()
    return user_info


def create_wordcloud(selected_user,df):
    df["message"] = df.message.str.strip("\n").str.strip(" ")
    df = df[df['message'] != '<Media omitted>']
    if selected_user == 'Overall':
        wc = WordCloud(collocations=False, background_color="white", )
        text_c = re.sub('[^A-Za-z0-9°]+', ' ', df.message.to_string())
        text = " ".join(item for item in df['message'])
        image = wc.generate(text)
        return image
    else:
        df = df[df['message'] != 'You deleted this message']
        messages=df[df['users']==selected_user].message
        wc = WordCloud(collocations=False, background_color="white", )
        text = " ".join(item for item in messages)
        image = wc.generate(text)
        return image

def show_month_year_timelie(selected_user,df):
    month_year = []
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    date_df = df.groupby(['year', 'month']).count()['message'].reset_index()
    for i in range(date_df.shape[0]):
        date = date_df['month'][i] + "-" + str(date_df['year'][i])
        print(date)
        month_year.append(date)
    date_df['month_year'] = month_year

    date_df.drop(columns=['year', 'month'], inplace=True)

    return date_df


def show_weekly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    df['day_name'] = df['dates'].dt.day_name()
    weekly_df=df.groupby('day_name').count()['message'].reset_index().sort_values(by='message', ascending=True)

    return weekly_df

def show_montly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df

def show_daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
        daily_timeline = df.groupby(df.dates.dt.date).count()['message'].reset_index()
        return daily_timeline
    return df.groupby(df.dates.dt.date).count()['message'].reset_index()

def show_active_users_info(df):
    df["day_name"] = df.dates.dt.day_name()
    most_active_users = df.users.value_counts().head(10).reset_index()
    most_active_users.columns = ['Most_active_users', 'message']
    most_active_users = most_active_users[most_active_users.Most_active_users != 'group_notification']
    return most_active_users






