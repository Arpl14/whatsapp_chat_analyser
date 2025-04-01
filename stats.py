import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
from urlextract import URLExtract
import matplotlib.pyplot as plt 
from io import BytesIO
import re
from textblob import TextBlob
import numpy as np



extract = URLExtract()

# Fetch statistics (group-level and individual user statistics)
def fetchstats(selected_user, df):
    # Group-level statistics: Total engagement, most active user
    if selected_user == 'Overall':
        # Group by User and count messages
        user_engagement = df['User'].value_counts()

        # Remove 'Group Notification' from the group stats and user engagement bar chart
        user_engagement = user_engagement[user_engagement.index != 'Group Notification']

        # Most active user
        most_active_user = user_engagement.idxmax()
        most_active_user_messages = user_engagement.max()

        # Total messages and links for the entire group
        total_messages = df.shape[0]
        total_links = sum(df['Message'].apply(lambda x: len(extract.find_urls(x))))

        # Return group-level stats
        group_stats = {
            "user_engagement": user_engagement,
            "most_active_user": most_active_user,
            "most_active_user_messages": most_active_user_messages,
            "total_messages": total_messages,
            "total_links": total_links
        }
        
        return group_stats

    # Individual user statistics
    df_user = df[df['User'] == selected_user] if selected_user != 'Overall' else df

    # Number of messages, total words, and links
    num_messages = df_user.shape[0]
    words = []
    for message in df_user['Message']:
        words.extend(message.split())

    # Counting the number of links shared
    links = []
    for message in df_user['Message']:
        links.extend(extract.find_urls(message))

    # Return individual stats
    individual_stats = {
        "num_messages": num_messages,
        "num_words": len(words),
        "links": len(links)
    }

    return individual_stats

def createwordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # List of words/phrases to exclude from the word cloud
    exclude_words = ['omitted', 'image', 'sticker', 'gif']

    # Regex pattern to match words containing 'image', 'sticker', 'gif', or 'omitted' (case insensitive)
    exclude_pattern = re.compile(r'\b(?:' + '|'.join(exclude_words) + r')\w*\b', re.IGNORECASE)

    # Filter out the unwanted words using the regex pattern
    filtered_messages = df['Message'].apply(lambda x: ' '.join([word for word in x.split() if not exclude_pattern.search(word)]))

    # Generate the Word Cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(filtered_messages.str.cat(sep=" "))

    # Save the word cloud image to a BytesIO object
    img_buf = BytesIO()
    df_wc.to_image().save(img_buf, format='PNG')  # Save as PNG format
    img_buf.seek(0)

    return img_buf


# Existing functions here...

def message_frequency_by_month(df):
    # Ensure the 'Only date' column is in datetime format
    df['Only date'] = pd.to_datetime(df['Only date'], errors='coerce')

    # Group by Year and Month to count messages
    df['Month_Year'] = df['Only date'].dt.to_period('M')  # Convert to Month-Year format
    message_frequency_by_month_year = df.groupby('Month_Year').count()['Message']

    # Find the top 5 peaks
    top_5_peaks = message_frequency_by_month_year.nlargest(5)

    # Return the message frequency data and top 5 peaks
    return message_frequency_by_month_year, top_5_peaks


# Function to calculate sentiment of a message
def get_sentiment(text):
    # Check if text is a string (non-null)
    if isinstance(text, str):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    return 0  # Return 0 sentiment for non-string entries (such as NaN)

# Function to calculate group sentiment over time
def group_sentiment(df):
    df['sentiment'] = df['Message'].apply(get_sentiment)
    sentiment_by_date = df.groupby('Only date')['sentiment'].mean()
    
    return sentiment_by_date

# Function to calculate individual sentiment by user
def sentiment_by_user(df):
    df['sentiment'] = df['Message'].apply(get_sentiment)
    sentiment_by_user = df[df['User'] != 'Group Notification'].groupby('User')['sentiment'].mean()
    
    return sentiment_by_user

# Function to handle sentiment plotting consistently
def plot_group_sentiment(sentiment_by_date, selected_user):
    # Sentiment by date (group sentiment over time)
    fig, ax = plt.subplots(figsize=(10, 6))  # Consistent size
    sentiment_by_date.plot(kind='line', ax=ax, title=f'{selected_user} Sentiment Over Time' if selected_user != 'Overall' else 'Group Sentiment Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust the plot to avoid cutoff
    return fig

# Function to handle sentiment by user plotting consistently
def plot_sentiment_by_user(sentiment_by_user):
    fig2, ax2 = plt.subplots(figsize=(10, 6))  # Consistent size
    sentiment_by_user.plot(kind='barh', color='skyblue', ax=ax2, title='Sentiment by User')
    ax2.set_xlabel('Average Sentiment')
    ax2.set_ylabel('User')
    plt.tight_layout()  # Adjust the plot to avoid cutoff
    return fig2

# # Emoji statistics
# def getemojistats(selecteduser, df):
#     if selecteduser != 'Overall':
#         df = df[df['User'] == selecteduser]

#     emojis = []
#     for message in df['Message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

#     emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emojidf

# # Monthly Timeline
# def monthtimeline(selecteduser, df):
#     if selecteduser != 'Overall':
#         df = df[df['User'] == selecteduser]

#     temp = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
#     time = []
#     for i in range(temp.shape[0]):
#         time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))
#     temp['Time'] = time
#     return temp

# # Most common words
# def getcommonwords(selecteduser, df):
#     file = open('stop_hinglish.txt', 'r')
#     stopwords = file.read().split('\n')

#     if selecteduser != 'Overall':
#         df = df[df['User'] == selecteduser]

#     words = []
#     for message in df['Message']:
#         for word in message.lower().split():
#             if word not in stopwords:
#                 words.append(word)

#     mostcommon = pd.DataFrame(Counter(words).most_common(20))
#     return mostcommon
