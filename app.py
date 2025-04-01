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
    st.dataframe(df.head())

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
        st.title("WhatsApp Group Engagement Analysis")

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


    # Word Cloud
    st.title("Word Cloud")
    wc_img = stats.createwordcloud(selected_user, df)

    # Display the Word Cloud image in Streamlit
    st.image(wc_img, caption='Word Cloud for Messages', use_column_width=True)


    # # Most Common Words
    # st.title("Most Common Words")
    # common_words = stats.getcommonwords(selected_user, df)
    # st.dataframe(common_words)

    # # Emoji Statistics
    # st.title("Emoji Statistics")
    # emoji_stats = stats.getemojistats(selected_user, df)
    # st.dataframe(emoji_stats)

    # # Monthly Timeline
    # st.title("Monthly Timeline")
    # month_time = stats.monthtimeline(selected_user, df)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.plot(month_time['Time'], month_time['Message'])
    # plt.xticks(rotation=45)
    # st.pyplot(fig)

    # # Activity Maps - Most Busy Day
    # st.title("Activity by Day")
    # busy_day = stats.weekactivitymap(selected_user, df)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.bar(busy_day.index, busy_day.values, color='purple')
    # plt.xticks(rotation='vertical')
    # st.pyplot(fig)

    # # Activity Maps - Most Busy Month
    # st.title("Activity by Month")
    # busy_month = stats.monthactivitymap(selected_user, df)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.bar(busy_month.index, busy_month.values, color='orange')
    # plt.xticks(rotation='vertical')
    # st.pyplot(fig)

    # # Sentiment Analysis - Sentiment Over Time
    # st.title("Sentiment Over Time")
    # sentiment_by_date = df.groupby('Only date')['sentiment'].mean()
    # fig, ax = plt.subplots(figsize=(10, 6))
    # sentiment_by_date.plot(kind='line', title='Group Sentiment Over Time', ax=ax)
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Sentiment')
    # st.pyplot(fig)

    # # Response Time Analysis
    # st.title("Response Time by User")
    # response_time_by_user = stats.fetchresponsebyuser(df)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # response_time_by_user.plot(kind='bar', title='Average Response Time by User', ax=ax)
    # ax.set_xlabel('User')
    # ax.set_ylabel('Response Time (seconds)')
    # st.pyplot(fig)

    # # Influencer Analysis - Top Influencers
    # st.title("Top Influencers")
    # top_influencers = stats.fetch_top_influencers(df)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # top_influencers.plot(kind='bar', title='Top 10 Influencers', ax=ax)
    # ax.set_xlabel('User')
    # ax.set_ylabel('Message Count')
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    # st.pyplot(fig)
