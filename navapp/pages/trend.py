import datetime
from datetime import datetime as dt

import altair as alt
import pandas as pd
import streamlit as st

from models.favorite import Favorite
from models.trend import Trend
from models.user import User
from models.website import Website


def show_trends():
    # count metric
    website_count = Website.find_website_count()
    categoriy_count = Website.find_category_count()
    totally_access_count = Trend.find_totally_count()
    weekly_access_count = Trend.find_weekly_count()
    daily_access_count = Trend.find_daily_count()
    user_count = User.find_user_count()

    metric_cols = st.columns(6)
    metric_cols[0].metric(label="Categories", value=categoriy_count)
    metric_cols[1].metric(label="Websites", value=website_count)
    metric_cols[2].metric(label="Total Access", value=totally_access_count)
    metric_cols[3].metric(label="Weekly Access", value=weekly_access_count)
    metric_cols[4].metric(label="Daily Access", value=daily_access_count)
    metric_cols[5].metric(label="Users", value=user_count)

    # weekly metric
    weekly_trends = Trend.find_weekly_trends()
    weekly_days = [x.strftime("%Y-%m-%d") for x in pd.date_range(dt.now() - datetime.timedelta(days=6), periods=7).tolist()]
    weekly_website_counts = dict()
    weekly_category_counts = dict()
    for trend in weekly_trends:
        trend_website = trend.website_name
        trend_category = trend.website_category
        trend_day = trend.created.strftime("%Y-%m-%d")

        if trend_website not in weekly_website_counts:
            weekly_website_counts[trend_website] = dict()
            weekly_website_counts[trend_website][trend_day] = 1
        elif trend_day not in weekly_website_counts[trend_website]:
            weekly_website_counts[trend_website][trend_day] = 1
        else:
            weekly_website_counts[trend_website][trend_day] += 1

        if trend_category not in weekly_website_counts:
            weekly_category_counts[trend_category] = dict()
            weekly_category_counts[trend_category][trend_day] = 1
        elif trend_day not in weekly_category_counts[trend_category]:
            weekly_category_counts[trend_category][trend_day] = 1
        else:
            weekly_category_counts[trend_category][trend_day] += 1

    weekly_website_frame = dict()
    weekly_category_frame = dict()
    for weekly_day in weekly_days:
        for weekly_website_count in weekly_website_counts:
            if weekly_website_count not in weekly_website_frame:
                weekly_website_frame[weekly_website_count] = list()
            if weekly_day not in weekly_website_counts[weekly_website_count]:
                weekly_website_frame[weekly_website_count].append(0)
            else:
                weekly_website_frame[weekly_website_count].append(weekly_website_counts[weekly_website_count][weekly_day])
        for weekly_category_count in weekly_category_counts:
            if weekly_category_count not in weekly_category_frame:
                weekly_category_frame[weekly_category_count] = list()
            if weekly_day not in weekly_category_counts[weekly_category_count]:
                weekly_category_frame[weekly_category_count].append(0)
            else:
                weekly_category_frame[weekly_category_count].append(weekly_category_counts[weekly_category_count][weekly_day])

    weekly_website_frame["days"] = weekly_days
    weekly_category_frame["days"] = weekly_days

    st.text("Weekly Website Access")
    st.line_chart(pd.DataFrame(weekly_website_frame, columns=list(weekly_website_frame.keys())), x="days")

    st.text("Weekly Category Access")
    st.line_chart(pd.DataFrame(weekly_category_frame, columns=list(weekly_category_frame.keys())), x="days")

    # top10 metric
    website_top10_df = pd.DataFrame(Trend.find_weekly_website_top10())
    favorite_top10_df = pd.DataFrame(Favorite.find_favorite_top10())
    user_top10_df = pd.DataFrame(Trend.find_user_top10())

    top_cols = st.columns(3)
    with (top_cols[0]):
        st.text("TOP 10 Websites")
        chart = alt.Chart(website_top10_df).mark_bar().encode(
            x='counts:Q',
            y=alt.Y('websits:N', sort='-x')
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with (top_cols[1]):
        st.text("TOP 10 Favorites")
        chart = alt.Chart(favorite_top10_df).mark_bar().encode(
            x='counts:Q',
            y=alt.Y('websits:N', sort='-x')
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with (top_cols[2]):
        st.text("TOP 10 Users")
        chart = alt.Chart(user_top10_df).mark_bar().encode(
            x='counts:Q',
            y=alt.Y('emails:N', sort='-x')
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        # st.altair_chart(alt.Chart(pd.melt(pd.DataFrame(
        #     np.random.rand(9, 4),
        #     index=["air", "coffee", "orange", "whitebread", "potato", "wine", "beer", "wheatbread", "carrot"],
        # ).reset_index(), id_vars=["index"])).mark_bar().encode(
        #     x=alt.X("value", type="quantitative", title=""),
        #     y=alt.Y("index", type="nominal", title=""),
        #     color=alt.Color("variable", type="nominal", title=""),
        #     order=alt.Order("variable", sort="descending"),
        # ), use_container_width=True)
