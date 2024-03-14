import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency  # Module for formatting currency

sns.set(style='dark')


def top_hourly_rentals_hr(df):
    grouped_data = df.groupby(
        'hr')['cnt'].sum().sort_values(ascending=False)[:5]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values)

    plt.title('Top 5 Hourly Bike Rentals')
    st.pyplot(plt.gcf())


def linechart_hourly_bike_rentals_hr(df):
    grouped_data = df.groupby('hr')['cnt'].sum()

    plt.figure(figsize=(14, 6))
    sns.lineplot(x=grouped_data.index, y=grouped_data.values,
                 marker='o', color='orange', sort=False)

    plt.title('Hourly Bike Rentals', fontsize=16)
    plt.xlabel('Hour of the Day', fontsize=14)
    plt.ylabel('Total Bike Rentals', fontsize=14)
    st.pyplot(plt.gcf())


def hourly_weekday_orders_hr(df):
    grouped_data = df.groupby(
        'weekday')['casual'].sum().sort_values(ascending=False)[:5]

    # Bar Plot for Top 5 Weekdays vs Casual
    plt.figure(figsize=(10, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values, color='skyblue')

    plt.title('Top 5 Weekdays vs Casual')
    plt.xlabel('Weekday')
    plt.ylabel('Total Casual')
    st.pyplot(plt.gcf())

    # Line Chart for Casual Orders per Weekday
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=grouped_data.index, y=grouped_data.values,
                 marker='o', color='green', label='Casual Orders')
    plt.title('Casual Orders per Weekday')
    plt.xlabel('Weekday')
    plt.ylabel('Total Casual Orders')
    plt.legend()
    st.pyplot(plt.gcf())


def monthly_orders_hr():
    global all_df
    all_df['month'] = pd.to_datetime(all_df['dteday']).dt.to_period('M')
    grouped_data = all_df.groupby('month')['cnt'].sum().sort_values()

    # Create a figure and axis for the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))

    # Bar Chart for Monthly Orders
    sns.barplot(x=grouped_data.index.astype(str), y=grouped_data.values,
                ax=ax, color='skyblue', label='Monthly Orders')

    # Set labels and title for the bar chart
    ax.set_xlabel('Month and Year')
    ax.set_ylabel('Total Orders')
    ax.set_title('Total Orders per Month and Year')
    ax.tick_params(axis='x', rotation=45, ha='right')

    # Show legend for the bar chart
    ax.legend(loc='upper right')

    # Show the plot
    st.pyplot(fig)


all_df = pd.read_csv("all_data.csv")
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()


with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date))
                 & (all_df["dteday"] <= str(end_date))]

# Ganti daily_orders_df dengan all_df pada bagian ini
col1, col2 = st.columns(2)
with col1:
    total_orders = all_df['cnt'].sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_months = all_df['dteday'].dt.to_period('M').nunique()
    st.metric("Total Months", value=total_months)

# Mengelompokkan data per 3 bulan dan menghitung total orderan per 3 bulan
resampled_df_3months = all_df.resample('3M', on='dteday').sum()

# Visualisasi data per 3 bulan
st.subheader("Peformance order rent bicycle every 3 months ")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(resampled_df_3months.index, resampled_df_3months["cnt"],
        marker='o', linewidth=2, color="#90CAF9")
plt.title("Peformance Rent Bicycle hoursb")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Best & Worst Performing Weekdays (Casual)")
hourly_weekday_orders_hr(all_df)

st.subheader("Top hourly rental")
linechart_hourly_bike_rentals_hr(all_df)
