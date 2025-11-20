from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Count words
    words = []
    for message in df['message']:
        if isinstance(message, str):
            words.extend(message.split())

    # Count media messages
    num_media_messages = df[
        df['message'].str.contains('Media omitted', case=False, na=False)
    ].shape[0]

    # Count links
    links = []
    for message in df['message']:
        if isinstance(message, str):
            links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    user_counts = df['user'].value_counts()
    df_percentage = (user_counts / df.shape[0] * 100).reset_index()
    df_percentage.columns = ['name', 'percentage']
    top_users = user_counts.head()
    return top_users, df_percentage


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        if isinstance(message, str):
            words.extend(message.lower().split())

    most_common = Counter(words).most_common(20)
    common_df = pd.DataFrame(most_common, columns=['word', 'count'])

    return common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def Daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    Daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return Daily_timeline


# ---------------------- NEW FUNCTION -----------------------
def most_busy_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    busy_day = df['day_name'].value_counts()

    return busy_day

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    # Filter for selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create pivot table: Day vs Hour
    user_heatmap = df.pivot_table(
        index='day_name', 
        columns='hour', 
        values='message', 
        aggfunc='count'
    ).fillna(0)

    return user_heatmap
