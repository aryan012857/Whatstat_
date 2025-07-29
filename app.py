import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("💬 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📂 Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    try:
        data = bytes_data.decode("utf-8")
    except UnicodeDecodeError:
        data = bytes_data.decode("ISO-8859-1")  # or "utf-16"
    df = preprocessor.preprocess(data)

    # fetch the unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Show Analysis WRT", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats
        st.title("📌 Chat Statistics")
        num_msg, words, num_media_msg, urls = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("### 💬 Total Messages")
            st.title( num_msg)

        with col2:
            st.markdown("### 📝 Total Words")
            st.title(words)

        with col3:
            st.markdown("### 📸 Media Shared")
            st.title(num_media_msg)

        with col4:
            st.markdown("### 🔗 Links Shared")
            st.title(urls)

        # Timeline analysis
        st.title("📅 Timeline Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("📆 **Monthly Analysis**")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            plt.plot(timeline['time'], timeline['message'])
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("📅 **Daily Analysis**")
            daily_time = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            plt.plot(daily_time['dates'], daily_time['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Activity map
        st.title("🗓️ Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("📈 **Active Months**")
            active_month = helper.active_months(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values, color='r')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("📊 **Active Days**")
            active_day = helper.active_weeks(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_day.index, active_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Most active users
        if selected_user == "Overall":
            st.title("👥 Most Active Users")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("🏆 **Top 5 Most Active Users**")
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation= 'vertical')
                st.pyplot(fig)

            with col2:
                st.markdown("📋 **User Activity Dataset**")
                st.dataframe(new_df)

        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        st.title("🔤 Most Common Words")
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🗣️ **Top 20 Most Used Words**")
            most_common_df.columns = ['Words', 'Count']
            ax.barh(most_common_df['Words'], most_common_df['Count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("📄 **Words Dataset**")
            st.dataframe(most_common_df)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("😊 Emoji Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("😀 **Top 5 Emojis Used**")
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels= emoji_df['Emojis'].head(), autopct='%.0f%%')
            st.pyplot(fig)

        with col2:
            st.markdown("📊 **Emoji Dataset**")
            st.dataframe(emoji_df)
