import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import show_stats
import seaborn as sns
import numpy as np
import pandas as pd
st.title("Data analysis")
st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    # Converting bytes into utf-8 format

    data = bytes_data.decode('utf-8')

    df=preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = preprocessor.fetch_unique_users(df).tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    st.sidebar.write(selected_user)

    message_count = show_stats.get_messages(df, selected_user)
    words_count = show_stats.count_words(df,selected_user)
    media_count = show_stats.count_media(df, selected_user)
    links_count = show_stats.extract_url(df,selected_user)
    show_busies_users = show_stats.fetch_busiest_users(df)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        # If clicked then perform analysis
        col1, col2, col3, col4 = st.columns(4)



        with col1:

            st.header("Total Messages")
            st.title(message_count)

        with col2:
            st.header("Total Words")
            st.title(words_count)

        with col3:
            st.header("Media Shared")
            st.title(message_count)

        with col4:
            st.header("Links Shared")
            st.title(links_count)

        # Busiest users in group

        col5, col6 = st.columns(2, gap="large")



        if selected_user == "Overall":
               with col5:
                   st.markdown("<br>", unsafe_allow_html=True)
                   #st.title("Busiest Users")
                   st.markdown('<h1 style="color:#007FFF"> Busiest Users </h1>', unsafe_allow_html=True)

                   #fig,ax = plt.subplots()
                   #ax.bar(show_busies_users.index,show_busies_users.values)
                   #plt.xticks(rotation='vertical')
                   #st.pyplot(fig)
                   users_info = df.users.value_counts().sort_values(ascending=False).head(6).reset_index()
                   st.bar_chart(users_info,width=0, height=0)

               with col6:
                   st.markdown("<br>", unsafe_allow_html=True)
                   st.markdown('<h1 style="color:#007FFF"> Frequent Users Data </h1>', unsafe_allow_html=True)
                   try:
                       st.dataframe(users_info)
                   except Exception:
                       pass
        else:
            with st.container():
                st.markdown("<br>", unsafe_allow_html=True)
                st.title("Users messages")
                st.dataframe(df[df['users']==selected_user])


        st.markdown("<br>", unsafe_allow_html=True)
        st.title("Frequent Words")
        word_img = show_stats.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(word_img)
        st.pyplot(fig)

        # Most common words

        most_common_words=preprocessor.most_common_words(selected_user,df)

        col6, col7 = st.columns(2,gap="large")
        st.markdown("<br>", unsafe_allow_html=True)
        with col6:
             st.title("Frequent Words Data")
             st.dataframe(most_common_words)

        with col7:
            st.title("Total Emojis Count")
            st.dataframe(preprocessor.extract_emoji(selected_user,df))

        st.title("Timeline Analysis")

        st.title("Monthly activity")

        with st.container():
            df = show_stats.show_montly_activity(selected_user,df)
            fig, ax = plt.subplots()
            sns.barplot(x=df.month.value_counts().index, y=df.month.value_counts().values, saturation=1, ax=ax,palette=sns.color_palette("Set2"))
            plt.xlabel("Month")
            plt.ylabel("Messages Count")
            plt.xticks(rotation=90);
            st.pyplot(fig)

        st.title("Month & Yearly activity")
        col8, col9 = st.columns(2)
        date_df = show_stats.show_month_year_timelie(selected_user, df)

        with col8:
            st.dataframe(date_df)


        with col9:

            fig , ax = plt.subplots()

            sns.lineplot(x=date_df['month_year'], y=date_df['message'],ax=ax,palette=sns.color_palette("pastel"),color="green")
            plt.xticks(rotation=90);
            st.pyplot(fig)


        st.title("Weekly timeline")
        weekly_timeline = show_stats.show_weekly_timeline(selected_user,df)
        with st.container():
            fig,ax = plt.subplots()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.grid(True,which="both")
            sns.lineplot(x=weekly_timeline['day_name'], y=weekly_timeline['message'], color='tomato', linestyle='--',ax=ax);
            plt.xticks(rotation=90)
            st.pyplot(fig)


        st.title("Daily timeline")

        day_timeline = show_stats.show_daily_timeline(selected_user, df)

        with st.container():
            sns.set(style="darkgrid")
            fig, ax = plt.subplots(figsize=(12, 8))

            sns.lineplot(x=day_timeline.dates , y=day_timeline.message, linestyle="dotted", marker='o', markersize=10,
                         linewidth=3, color='teal', ax=ax)
            st.pyplot(fig)


        st.title("Active users timeline")

        col11, col12 = st.columns(2)
        can_show_info = False
        most_active_users = show_stats.show_active_users_info(df)
        with col11:
            st.dataframe(most_active_users['Most_active_users'])

            active_user=st.selectbox(label="Select user", options=most_active_users.Most_active_users.value_counts().index)

           # if st.button("Show analysis"):
            #    can_show_info=True


        with col12:
            if st.button("Show analysis"):
                    user_data=df[df['users']==active_user]
                    user_data=user_data.groupby("day_name").count()['message'].reset_index()
                    sns.set_style(style="darkgrid")
                    fig,ax=plt.subplots()

                    sns.barplot(x=user_data.day_name,y=user_data.message,ax=ax)
                    st.pyplot(fig)








