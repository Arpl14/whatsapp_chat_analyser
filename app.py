# import streamlit as st
# import preprocess
# import stats
# import matplotlib.pyplot as plt

# # Title for the Streamlit app
# st.sidebar.title("WhatsApp Chat Analyzer")

# # File uploader to upload WhatsApp group chat file
# uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp group chat file", type=["txt"])

# # Check if a file has been uploaded
# if uploaded_file is not None:
#     # Convert the uploaded file's byte content into text
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")

#     # Preprocess the uploaded WhatsApp chat data
#     df = preprocess.preprocess(data)

#     # Display the first few rows of the processed DataFrame
#     st.dataframe(df.head(50))

#     # Get unique users excluding 'Group Notification'
#     user_list = df['User'].unique().tolist()
#     user_list = [user for user in user_list if user != 'Group Notification']  # Remove group notifications
#     user_list.insert(0, 'Overall')  # Add 'Overall' as the first option for overall analysis

#     # Sidebar selection for users
#     selected_user = st.sidebar.selectbox("Select a user for analysis", user_list)

#     # Fetch group-level statistics (if 'Overall' is selected)
#     group_stats = stats.fetchstats(selected_user, df)

#     # Show group-level statistics (if 'Overall' is selected)
#     if selected_user == 'Overall':
#         st.title("Group Sentiment Analysis")
#         st.write(f"Most active user: {group_stats['most_active_user']} with {group_stats['most_active_user_messages']} messages")
#         st.write(f"Total messages in the group: {group_stats['total_messages']}")
#         st.write(f"Total links shared in the group: {group_stats['total_links']}")

#         # Display user engagement (number of messages for each user)
#         st.write("User Engagement:")
#         st.bar_chart(group_stats['user_engagement'])

#     # Show individual user statistics (messages, links, and words)
#     else:
#         st.title(f"WhatsApp Chat Analysis for {selected_user}")
#         individual_stats = group_stats

#         st.write(f"Number of messages: {individual_stats['num_messages']}")
#         st.write(f"Total number of words: {individual_stats['num_words']}")
#         st.write(f"Links shared: {individual_stats['links']}")

#     # Word Cloud for the selected user
#     st.title("Word Cloud")
#     wc_img = stats.createwordcloud(selected_user, df)
#     st.image(wc_img, caption='Word Cloud for Messages', use_column_width=True)

#     # Message Frequency by Month-Year
#     st.title("Message Frequency by Month-Year")
#     # Filter the data based on the selected user
#     if selected_user != 'Overall':
#         df_filtered = df[df['User'] == selected_user]
#     else:
#         df_filtered = df

#     # Get message frequency and top 5 peaks
#     message_freq_data, top_5_peaks = stats.message_frequency_by_month(df_filtered)

#     # Plot the message frequency by Month-Year
#     fig, ax = plt.subplots(figsize=(10, 6))
#     message_freq_data.plot(kind='line', ax=ax, title='Message Frequency by Month-Year')

#     # Add labels for the top 5 peaks
#     for peak in top_5_peaks.index:
#         ax.text(peak, top_5_peaks[peak], str(top_5_peaks[peak]), ha='center', color='red', fontweight='bold')

#     # Customizing the plot
#     ax.set_xlabel('Month-Year')
#     ax.set_ylabel('Message Count')
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     # Display the plot in Streamlit
#     st.pyplot(fig)



#     # Get the day of the week activity (most active day)
#     activity_by_day = stats.weekactivitymap(df)

#     # Plotting Activity by Day of the Week
#     st.title("Activity by Day of the Week")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.bar(activity_by_day.index, activity_by_day.values, color='skyblue')
#     ax.set_xlabel('Day of the Week')
#     ax.set_ylabel('Message Count')
#     ax.set_title('Messages Sent per Day of the Week')
#     plt.xticks(rotation=45)
#     st.pyplot(fig)


#     # # Add to your existing code where you're processing the file and user selection
#     # if selected_user == 'Overall':
#     # # Get the most common emojis from the data
#     #     emoji_df = stats.get_most_common_emojis(df)
    
#     # # Display the top 10 most common emojis in a table
#     # st.title("Most Common Emojis")
#     # st.dataframe(emoji_df)

    
#     # Sentiment Analysis: Group Sentiment Over Time
#     st.title("Sentiment Analysis Trend")

#     # Sentiment by date (group sentiment over time)
#     if selected_user != 'Overall':
#         df_filtered = df[df['User'] == selected_user]  # Filter for specific user if not Overall

#     # Group Sentiment Over Time Plot
#     sentiment_by_date = stats.group_sentiment(df_filtered)
#     fig = stats.plot_group_sentiment(sentiment_by_date, selected_user)
#     st.pyplot(fig)

#     # Sentiment by User (only for Overall)
#     if selected_user == 'Overall':
#         sentiment_by_user = stats.sentiment_by_user(df)

#         # Sentiment by User Horizontal Bar Plot
#         fig2 = stats.plot_sentiment_by_user(sentiment_by_user)
#         st.pyplot(fig2)

#     # Topic Modeling and Word Clouds
#     st.title("Topic Modeling and Word Clouds")

#     # Generate word clouds for the top topics (up to 4 topics)
#     wordclouds = stats.generate_topics_and_wordclouds(df, num_topics=4)

#     # Arrange the word clouds side by side
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.image(wordclouds[0], caption="Topic 1")
 
#     with col2:
#         st.image(wordclouds[1], caption="Topic 2")

#     with col3:
#         st.image(wordclouds[2], caption="Topic 3")

#     with col4:
#         st.image(wordclouds[3], caption="Topic 4")

#     # User Segmentation
#     st.title("User Segmentation")

# # Add the segmentation plot if the selected user is 'Overall'
# if selected_user == 'Overall':
#     # Generate user segmentation plot
#     segmentation_fig = stats.user_segmentation(df)
#     st.pyplot(segmentation_fig)

#     # Display network analysis graph only for the 'Overall' user
#     st.title("User Interaction Network")
#     # Generate network graph for group
#     network_fig = stats.network_analysis(df)
#     st.pyplot(network_fig)

#     # Display the user with the maximum responses
#     most_active_user, most_active_user_responses = stats.max_responses_user(df)
#     st.write(f"Most active user: {most_active_user} with {most_active_user_responses} responses.")
#     st.write("The color of the nodes represents the activity level of each user. The colour scale for nodes is (blue -> pink -> orange -> yellow), with blue being least responsive and yellow being most responsive. The node size is also based on the number of messages they sent. "
#              "\n\nSimilarly, the arrows denote responsiveness between the two users they connect. The arrow colour scale is (blue -> red -> green), with blue being least responsive and green being most responsive. The arrow direction shows the message direction.")
# else:
#     # Do nothing for individual user selection, no title or graph displayed
#     pass

#     # # Generate user segmentation plot
#     # segmentation_fig = stats.user_segmentation(df)
#     # st.pyplot(segmentation_fig)

    

#     # # Display network analysis graph only for the 'Overall' user
#     # if selected_user == 'Overall':
#     #     st.title("User Interaction Network")
#     #     # Generate network graph for group
#     #     network_fig = stats.network_analysis(df)
#     #     st.pyplot(network_fig)

#     #     # Display the user with the maximum responses
#     #     most_active_user, most_active_user_responses = stats.max_responses_user(df)
#     #     st.write(f"Most active user: {most_active_user} with {most_active_user_responses} responses.")
#     #     st.write("The color of the nodes represents the activity level of each user. The colour scale for nodes is (blue -> pink -> orange -> yellow), with blue being least responsive and yellow being most responsive. The node size is also based on the number of messages they sent. "
#     #      "\n\nSimilarly, the arrows denote responsiveness between the two users they connect. The arrow colour scale is (blue -> red -> green), with blue being least responsive and green being most responsive. The arrow direction shows the message direction.")




import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt

# Title for the Streamlit app
st.sidebar.title("WhatsApp Chat Analyzer")

# File uploader to upload WhatsApp group chat file
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp group chat file", type=["txt"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Convert the uploaded file's byte content into text
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the uploaded WhatsApp chat data
    df = preprocess.preprocess(data)

    # Display the first few rows of the processed DataFrame
    st.dataframe(df.head(50))

    # Get unique users excluding 'Group Notification'
    user_list = df['User'].unique().tolist()
    user_list = [user for user in user_list if user != 'Group Notification']  # Remove group notifications
    user_list.insert(0, 'Overall')  # Add 'Overall' as the first option for overall analysis

    # Sidebar selection for users
    selected_user = st.sidebar.selectbox("Select a user for analysis", user_list)

    # Fetch group-level statistics (if 'Overall' is selected)
    group_stats = stats.fetchstats(selected_user, df)

    # Show group-level statistics (if 'Overall' is selected)
    if selected_user == 'Overall':
        st.title("Group Sentiment Analysis")
        st.write(f"Most active user: {group_stats['most_active_user']} with {group_stats['most_active_user_messages']} messages")
        st.write(f"Total messages in the group: {group_stats['total_messages']}")
        st.write(f"Total links shared in the group: {group_stats['total_links']}")

        # Display user engagement (number of messages for each user)
        st.write("User Engagement:")
        st.bar_chart(group_stats['user_engagement'])

    # Show individual user statistics (messages, links, and words)
    else:
        st.title(f"WhatsApp Chat Analysis for {selected_user}")
        individual_stats = group_stats

        st.write(f"Number of messages: {individual_stats['num_messages']}")
        st.write(f"Total number of words: {individual_stats['num_words']}")
        st.write(f"Links shared: {individual_stats['links']}")

    # Word Cloud for the selected user
    st.title("Word Cloud")
    wc_img = stats.createwordcloud(selected_user, df)
    st.image(wc_img, caption='Word Cloud for Messages', use_column_width=True)

    # Message Frequency by Month-Year
    st.title("Message Frequency by Month-Year")
    # Filter the data based on the selected user
    if selected_user != 'Overall':
        df_filtered = df[df['User'] == selected_user]
    else:
        df_filtered = df

    # Get message frequency and top 5 peaks
    message_freq_data, top_5_peaks = stats.message_frequency_by_month(df_filtered)

    # Plot the message frequency by Month-Year
    fig, ax = plt.subplots(figsize=(10, 6))
    message_freq_data.plot(kind='line', ax=ax, title='Message Frequency by Month-Year')

    # Add labels for the top 5 peaks
    for peak in top_5_peaks.index:
        ax.text(peak, top_5_peaks[peak], str(top_5_peaks[peak]), ha='center', color='red', fontweight='bold')

    # Customizing the plot
    ax.set_xlabel('Month-Year')
    ax.set_ylabel('Message Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Get the day of the week activity (most active day)
    activity_by_day = stats.weekactivitymap(df)

    # Plotting Activity by Day of the Week
    st.title("Activity by Day of the Week")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(activity_by_day.index, activity_by_day.values, color='skyblue')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Message Count')
    ax.set_title('Messages Sent per Day of the Week')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Sentiment by date (group sentiment over time)
    if selected_user != 'Overall':
        df_filtered = df[df['User'] == selected_user]  # Filter for specific user if not Overall


    # Sentiment Analysis: Group Sentiment Over Time
    st.title("Sentiment Analysis Trend")

    
    # Group Sentiment Over Time Plot
    sentiment_by_date = stats.group_sentiment(df_filtered)
    fig = stats.plot_group_sentiment(sentiment_by_date, selected_user)
    st.pyplot(fig)

    # Sentiment by User (only for Overall)
    if selected_user == 'Overall':
        sentiment_by_user = stats.sentiment_by_user(df)

        # Sentiment by User Horizontal Bar Plot
        fig2 = stats.plot_sentiment_by_user(sentiment_by_user)
        st.pyplot(fig2)

    # Topic Modeling and Word Clouds
    st.title("Topic Modeling and Word Clouds")

    # Generate word clouds for the top topics (up to 4 topics)
    wordclouds = stats.generate_topics_and_wordclouds(df, num_topics=4)

    # Arrange the word clouds side by side
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image(wordclouds[0], caption="Topic 1")
 
    with col2:
        st.image(wordclouds[1], caption="Topic 2")

    with col3:
        st.image(wordclouds[2], caption="Topic 3")

    with col4:
        st.image(wordclouds[3], caption="Topic 4")

    # User Segmentation
    st.title("User Segmentation")

    # Add the segmentation plot if the selected user is 'Overall'
    if selected_user == 'Overall':
        # Generate user segmentation plot
        segmentation_fig = stats.user_segmentation(df)
        st.pyplot(segmentation_fig)

        # Display network analysis graph only for the 'Overall' user
        st.title("User Interaction Network")
        # Generate network graph for group
        network_fig = stats.network_analysis(df)
        st.pyplot(network_fig)

        # Display the user with the maximum responses
        most_active_user, most_active_user_responses = stats.max_responses_user(df)
        st.write(f"Most active user: {most_active_user} with {most_active_user_responses} responses.")
        st.write("The color of the nodes represents the activity level of each user. The colour scale for nodes is (blue -> pink -> orange -> yellow), with blue being least responsive and yellow being most responsive. The node size is also based on the number of messages they sent. "
                 "\n\nSimilarly, the arrows denote responsiveness between the two users they connect. The arrow colour scale is (blue -> red -> green), with blue being least responsive and green being most responsive. The arrow direction shows the message direction.")
else:
    # Do nothing for individual user selection, no title or graph displayed
    pass
