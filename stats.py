import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
from urlextract import URLExtract
import matplotlib.pyplot as plt
from io import BytesIO
import re

extract = URLExtract()

# Fetch statistics (number of messages, media, links)
def fetchstats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # Counting the number of media files shared
    media_ommitted = df[df['Message'] == '<Media omitted>']

    # Counting the number of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), media_ommitted.shape[0], len(links)

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
