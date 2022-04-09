import streamlit as st
import pandas as pd
import altair as alt


df = pd.read_csv("finance-2022-04-08.csv")
df = df[:-1]  # Remove last row, summary from splitwise

# Set types
df["Cost"] = df["Cost"].astype(float)
df["Category"] = df["Category"].astype("category")
df["Date"] = pd.to_datetime(df["Date"])

# Remove payment, it's not that interesting
if st.checkbox("Exlude payments", value=True):
    df = df[df["Category"] != "Payment"]

cat_df = df
cat_list = sorted(list(cat_df["Category"].unique()))
categories = st.multiselect("Choose Categories", cat_list, [])
if categories:
    cat_df = cat_df[cat_df["Category"].isin(categories)]
    # Remove the categories that have been filtered out, otherwise they are still
    # set as the categories for the Category column
    # just pandas stuff
    cat_df["Category"] = cat_df["Category"].cat.remove_unused_categories()

chart = (
    alt.Chart(cat_df)
    .mark_bar()
    .encode(
        alt.X("sum(Cost)", axis=alt.Axis(labelExpr='datum.value + "kr"')),
        alt.Y("Category", sort="-x"),
    )
)
st.altair_chart(chart, use_container_width=True)

chart_pie = (
    alt.Chart(cat_df)
    .mark_arc()
    .encode(
        theta=alt.Theta("sum(Cost)", type="quantitative"),
        color=alt.Color(field="Category", type="nominal"),
    )
)
st.altair_chart(chart_pie, use_container_width=True)

date_df = cat_df.groupby([pd.Grouper(key="Date", freq="M"), "Category"]).sum()
date_df = date_df.reset_index()
chart = (
    alt.Chart(date_df)
    .mark_area(opacity=0.5)
    .encode(x="Date:T", y="Cost:Q", color="Category")
)
st.altair_chart(chart, use_container_width=True)
chart = (
    alt.Chart(date_df)
    .mark_area(opacity=0.5)
    .encode(x="Date:T", y=alt.Y("Cost:Q", stack="normalize"), color="Category")
)
st.altair_chart(chart, use_container_width=True)

compare_cat = st.selectbox("Which Category to check?", cat_list)
who_df = df[df["Category"].isin([compare_cat])]
who_df["Category"] = who_df["Category"].cat.remove_unused_categories()
who_df = who_df.melt(
    id_vars=["Date", "Description", "Category", "Cost", "Currency"],
    var_name="User",
    value_name="Balance",
)
payer = who_df["Balance"] > 0
who_df.loc[payer, ["Paid"]] = who_df.loc[payer, ["Cost"]].values
who_df = who_df.dropna()
who_df = who_df.groupby([pd.Grouper(key="Date", freq="M"), "Category", "User"]).sum()
who_df = who_df.reset_index()

chart = (
    alt.Chart(who_df)
    .mark_area(opacity=0.5)
    .encode(x="Date:T", y=alt.Y("Cost:Q"), color="User")
)
st.altair_chart(chart, use_container_width=True)

chart = (
    alt.Chart(who_df)
    .mark_area(opacity=0.5)
    .encode(x="Date:T", y=alt.Y("Cost:Q", stack="normalize"), color="User")
)
st.altair_chart(chart, use_container_width=True)
