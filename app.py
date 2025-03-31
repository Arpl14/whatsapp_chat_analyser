import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

# File uploader to upload WhatsApp chat file
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp group chat file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    # Convert the bytecode to text
    data = bytes_data.decode("utf-8")

    # Process the data with the preprocess function
    df = preprocess.preprocess(data)

    # Display the first few rows of the DataFrame
    st.dataframe(df.head())

    # Get unique users
    user_list = df['User'].unique().tolist()
    user_list = [user for user in user_list if user != 'Group Notification']  # Remove group notifications
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Select a user for analysis", user_list)

    # Show basic stats
    num_messages, num_words, media_omitted, links = stats.fetchstats(selected_user, df)

    st.title(f"WhatsApp Chat Analysis for {selected_user}")
    st.write(f"Number of messages: {num_messages}")
    st.write(f"Total number of words: {num_words}")
    st.write(f"Media omitted: {media_omitted}")
    st.write(f"Links shared: {links}")

    # Word Cloud
    st.title("Word Cloud")
    wc_img = stats.createwordcloud(selected_user, df)
    st.image(wc_img)

    # Most Common Words
    st.title("Most Common Words")
    common_words = stats.getcommonwords(selected_user, df)
    st.dataframe(common_words)

    # Emoji Statistics
    st.title("Emoji Statistics")
    emoji_stats = stats.getemojistats(selected_user, df)
    st.dataframe(emoji_stats)

    # Monthly Timeline
    st.title("Monthly Timeline")
    month_time = stats.monthtimeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(month_time['Time'], month_time['Message'])
    st.pyplot(fig)