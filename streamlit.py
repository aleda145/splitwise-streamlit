import streamlit as st
import pandas as pd
import altair as alt


def clean_df():
    df = pd.read_csv("finance-2022-04-08.csv")
    df = df[:-1]  # Remove last row, summary from splitwise

    # Set types
    df["Cost"] = df["Cost"].astype(float)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def check_categories(df):
    cat_df = df[["Date", "Cost", "Category"]]
    cat_list = sorted(list(cat_df["Category"].unique()))
    categories = st.multiselect("Choose Categories", cat_list, [])
    if categories:
        cat_df = cat_df[cat_df["Category"].isin(categories)]
        # Remove the categories that have been filtered out, otherwise they are still
        # set as the categories for the Category column
        # just pandas stuff
        cat_df["Category"] = cat_df["Category"].cat.remove_unused_categories()

    show_top = st.slider("Coalesce", 0, len(cat_list), value=5)

    if show_top:
        top_5 = (
            cat_df.groupby("Category")
            .sum()
            .sort_values(by="Cost", ascending=False)[0:show_top]
        )
        top_5_cat = list(top_5.index)
        cat_df.loc[~cat_df["Category"].isin(top_5_cat), "Category"] = "Other"

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


def check_who(df):
    cat_list = sorted(list(df["Category"].unique()))
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
    who_sum_df = who_df.groupby(
        [pd.Grouper(key="Date", freq="M"), "Category", "User"]
    ).sum()
    who_sum_df = who_sum_df.reset_index()

    chart = (
        alt.Chart(who_sum_df)
        .mark_area(opacity=0.5)
        .encode(x="Date:T", y=alt.Y("Cost:Q"), color="User")
    )
    st.altair_chart(chart, use_container_width=True)

    chart = (
        alt.Chart(who_sum_df)
        .mark_area(opacity=0.5)
        .encode(x="Date:T", y=alt.Y("Cost:Q", stack="normalize"), color="User")
    )
    st.altair_chart(chart, use_container_width=True)

    who_count_df = who_df.groupby(
        [pd.Grouper(key="Date", freq="M"), "Category", "User"]
    ).count()
    who_count_df = who_count_df.reset_index()
    chart = (
        alt.Chart(who_count_df)
        .mark_area(opacity=0.5)
        .encode(x="Date:T", y=alt.Y("Cost:Q"), color="User")
    )
    st.altair_chart(chart, use_container_width=True)

    chart = (
        alt.Chart(who_count_df)
        .mark_area(opacity=0.5)
        .encode(x="Date:T", y=alt.Y("Cost:Q", stack="normalize"), color="User")
    )
    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    df = clean_df()
    # Remove payment, it's not that interesting
    if st.checkbox("Exlude payments", value=True):
        df = df[df["Category"] != "Payment"]
    check_categories(df)
    df["Category"] = df["Category"].astype("category")

    check_who(df)
