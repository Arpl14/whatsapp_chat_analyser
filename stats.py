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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import networkx as nx
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D



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


# Function to generate word cloud from topic words
def generate_wordcloud(topic_idx, topic, vectorizer):
    # Get the top words for the topic
    topic_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]
    
    # Remove the word "omitted" from the list if it exists
    topic_words = [word for word in topic_words if word != 'omitted']
    
    # Join the words and create a string for wordcloud
    topic_text = ' '.join(topic_words)
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(topic_text)

    # Save the wordcloud to a BytesIO object
    img_buf = BytesIO()
    wordcloud.to_image().save(img_buf, format='PNG')
    img_buf.seek(0)
    
    return img_buf

# Function to extract topics and generate word clouds
def generate_topics_and_wordclouds(df, num_topics=4):
    # Vectorize the messages to a TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Message'])
    
    # Apply LDA to extract topics
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(X)
    
    # Store the word clouds for each topic
    wordclouds = []
    for topic_idx, topic in enumerate(lda.components_):
        wordcloud = generate_wordcloud(topic_idx, topic, vectorizer)
        wordclouds.append(wordcloud)
    
    return wordclouds










# Function for user segmentation using KMeans clustering
def user_segmentation(df):
    # Filter out 'Group Notification' users
    user_data = df[df['User'] != 'Group Notification']

    # Segment users based on activity (message count, sentiment)
    user_data = user_data.groupby('User').agg({'Message': 'count', 'sentiment': 'mean'}).reset_index()

    # Normalize the data
    scaler = StandardScaler()
    user_data[['Message', 'sentiment']] = scaler.fit_transform(user_data[['Message', 'sentiment']])

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    user_data['Cluster'] = kmeans.fit_predict(user_data[['Message', 'sentiment']])

    # Visualize the clusters
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(user_data['Message'], user_data['sentiment'], c=user_data['Cluster'], cmap='viridis')

    # Adding labels for each user (first two words of the user's name)
    for i in range(len(user_data)):
        user_name = user_data['User'].iloc[i]
        label = ' '.join(user_name.split()[:2])  # Take the first two words
        ax.text(user_data['Message'].iloc[i], user_data['sentiment'].iloc[i], label, 
                 fontsize=9, alpha=0.7, ha='right', color='black')

    ax.set_title('User Segmentation')
    ax.set_xlabel('Message Count')
    ax.set_ylabel('Average Sentiment')
    plt.colorbar(scatter, label='Cluster')

    return fig








# # Function to generate a network graph for the group
# def network_analysis(df):
#     # Create an undirected graph
#     G = nx.Graph()  # If you want a directed graph, use nx.DiGraph()

#     # Filter out 'Group Notification' users from the dataframe
#     filtered_df = df[df['User'] != 'Group Notification' ]

#     # Loop through the filtered messages and create edges between users
#     for idx in range(1, len(filtered_df)):
#         user1 = filtered_df['User'].iloc[idx-1]
#         user2 = filtered_df['User'].iloc[idx]
        
#         # Avoid self-responses (no edge between the same user)
#         if user1 != user2:
#             if G.has_edge(user1, user2):
#                 G[user1][user2]['weight'] += 1  # Increment edge weight if the edge already exists
#             else:
#                 G.add_edge(user1, user2, weight=1)  # Add edge with initial weight

#     # Visualize the graph with the required properties
#     plt.figure(figsize=(14, 14))

#     # Get the number of responses per user (for node color gradient)
#     user_response_count = {user: G.degree(user) for user in G.nodes}

#     # Get the edge weight for adjusting edge color intensity
#     edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

#     # Get the color gradient based on user responses
#     node_color = [user_response_count[user] for user in G.nodes]
#     node_size = [500 + 10 * user_response_count[user] for user in G.nodes]  # Size of the node based on number of responses

#     # Draw the graph with custom settings
#     node_scatter = nx.draw(G, with_labels=True, node_size=node_size, node_color=node_color, 
#                            cmap=plt.cm.YlOrRd, font_size=12, font_weight='bold', 
#                            edge_color=edge_weights, width=3, edge_cmap=plt.cm.RdYlGn,  
#                            alpha=0.7, edge_vmin=0, edge_vmax=max(edge_weights), arrows=True, arrowsize=15)

#     # Create a ScalarMappable for the node color scale
#     norm_node = mcolors.Normalize(vmin=min(node_color), vmax=max(node_color))
#     sm_node = plt.cm.ScalarMappable(cmap=plt.cm.YlOrRd, norm=norm_node)
#     sm_node.set_array([])  # Empty array for the colorbar

#     # # Add a color bar for the nodes
#     # cbar_node = plt.colorbar(sm_node, ax=plt.gca(), label='Node Activity Level')

#     # Title for the graph
#     plt.title('Who Responds to Whom: User Interaction Network', fontsize=16)

#     # Show the graph
#     plt.show()

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Function to generate the network analysis
def network_analysis(df):
    # Create a directed graph
    G = nx.DiGraph()

    # Filter out 'Group Notification' users
    filtered_df = df[df['User'] != 'Group Notification']

    # Loop through the filtered messages and create edges between users
    for idx in range(1, len(filtered_df)):
        user1 = filtered_df['User'].iloc[idx-1]
        user2 = filtered_df['User'].iloc[idx]
        
        # Avoid self-responses (no edge between the same user)
        if user1 != user2:
            if G.has_edge(user1, user2):
                G[user1][user2]['weight'] += 1  # Increment edge weight if the edge already exists
            else:
                G.add_edge(user1, user2, weight=1)  # Add edge with initial weight

    # Visualize the graph with the required properties
    plt.figure(figsize=(14, 14))

    # Get the number of responses per user (for node color gradient)
    user_response_count = {user: G.out_degree(user) for user in G.nodes}

    # Get the edge weight for adjusting edge color intensity
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

    # Get the color gradient for nodes (more active users are green, less active are purple)
    node_color = [user_response_count[user] for user in G.nodes]
    node_size = [500 + 50 * user_response_count[user] for user in G.nodes]  # Size of the node based on activity level

    # Draw the graph with custom settings
    edge_colors = [mcolors.to_rgba(plt.cm.brg(weight / max(edge_weights))[:3]) for weight in edge_weights]

    # Draw the graph with varying edge colors based on response frequency
    nx.draw(G, with_labels=True, node_size=node_size, node_color=node_color, 
            cmap=plt.cm.plasma, font_size=12, font_weight='bold', 
            edge_color=edge_colors, width=3, edge_cmap=plt.cm.brg, 
            alpha=0.6, arrows=True, arrowsize=8)

    # Title for the graph
    plt.title('Who Responds to Whom: User Interaction Network', fontsize=16)

    # Show the graph
    plt.show()

# def getemojistats(selecteduser, df):
#     if selecteduser != 'Overall':
#         df = df[df['User'] == selecteduser]

#     emojis = []
#     for message in df['Message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

#     emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emojidf


