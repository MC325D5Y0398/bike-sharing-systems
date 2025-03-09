import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Membaca data yang telah dibersihkan
file_path = os.path.join(os.path.dirname(__file__), "day_data.csv", "hour_data.csv")
day_data = pd.read_csv("dashboard/day_data.csv")
hour_data = pd.read_csv("dashboard/hour_data.csv")

# Mengubah tipe data "dteday" menjadi datetime
day_data["dteday"] = pd.to_datetime(day_data["dteday"])
hour_data["dteday"] = pd.to_datetime(hour_data["dteday"])

# Mengubah nama kolom agar mudah dibaca
day_data = day_data.rename(columns={
    "dteday": "Date",
    "cnt": "Total Rentals",
    "casual": "Casual Users",
    "registered": "Registered Users",
    "temp": "Temperature (°C)",
    "atemp": "Feels-Like Temperature (°C)",
    "hum": "Humidity (%)",
    "windspeed": "Wind Speed (km/h)",
    "season": "Season",
    "mnth": "Month",
    "weekday": "Weekday",
    "workingday": "Working Day"
})

# Mengubah nama musim, bulan, dan hari dari integer menjadi string nama aslinya
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
month_map = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}
weekday_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

day_data["Season_Num"] = day_data["Season"]
day_data["Season"] = day_data["Season"].map(season_map)
day_data["Month_Num"] = day_data["Month"]
day_data["Month"] = day_data["Month"].map(month_map)
day_data["Weekday"] = day_data["Weekday"].map(weekday_map)

st.set_page_config(layout="wide", page_title="Bike Sharing Systems Dashboard")
st.title("🚴‍♂️ Bike Sharing Systems Dashboard")

st.text("")
st.text("")
st.text("")

# Membuat fitur filter di sidebar
st.sidebar.header("🔎 Filters")
st.sidebar.text("")
date_range = st.sidebar.date_input("Select Date Range", [day_data["Date"].min(), day_data["Date"].max()])

date_range = [pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])]

user_type = st.sidebar.selectbox("Select User Type", ["All", "Casual", "Registered"])

filtered_data = day_data[(day_data["Date"] >= date_range[0]) & (day_data["Date"] <= date_range[1])]
if user_type == "Casual":
    filtered_data["Total Rentals"] = filtered_data["Casual Users"]
elif user_type == "Registered":
    filtered_data["Total Rentals"] = filtered_data["Registered Users"]

# Menunjukkan total registered users dan total casual users
col1, col2 = st.columns(2)
with col1:
    total_registered = filtered_data["Registered Users"].sum()
    st.metric(label="Total Registered Users", value=f"{total_registered:,}")
with col2:
    total_casual = filtered_data["Casual Users"].sum()
    st.metric(label="Total Casual Users", value=f"{total_casual:,}")

# Grafik Bike Usage Based on Seasons
st.subheader("📊 Bike Usage Based on Seasons")
season_data = filtered_data.groupby("Season")["Total Rentals"].sum()
st.bar_chart(season_data)

# Grafik Bike Usage Based on Days
st.subheader("📅 Bike Usage Based on Days")
weekday_data = filtered_data.groupby("Weekday")["Total Rentals"].sum()
st.bar_chart(weekday_data)

# Grafik Bike Usage Based on Months
st.subheader("📆 Bike Usage Based on Months")
month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
month_data = filtered_data.groupby("Month")["Total Rentals"].sum().reindex(month_order)
st.bar_chart(month_data)

# Menunjukkan total penggunaan sepeda di tahun 2011 dan 2012
yearly_trend = filtered_data.groupby(filtered_data["Date"].dt.year)["Total Rentals"].sum()
col1, col2 = st.columns(2)
with col1:
    total_2011 = yearly_trend.get(2011, 0)
    st.metric(label="Total Rentals in 2011", value=f"{total_2011:,}")
with col2:
    total_2012 = yearly_trend.get(2012, 0)
    st.metric(label="Total Rentals in 2012", value=f"{total_2012:,}")

# Grafik Bike Rental Trends (2011 vs 2012)
st.subheader("📈 Bike Rental Trends (2011 vs 2012)")
st.line_chart(yearly_trend)

# Grafik Daily Bike Rentals Trend (2011 vs 2012)
st.subheader("📅 Daily Bike Rentals Trend (2011 vs 2012)")
st.line_chart(filtered_data.set_index("Date")["Total Rentals"])

# Grafik Bike Rentals Trend with Moving Average (2011 vs 2012)
st.subheader("📈 Bike Rentals Trend with Moving Average (2011 vs 2012)")
filtered_data["Moving Average"] = filtered_data["Total Rentals"].rolling(window=7).mean()
st.line_chart(filtered_data.set_index("Date")["Moving Average"])

# Penutup
st.sidebar.text("")
st.sidebar.text("Copyright © MC325D5Y0398 Given Putra")

st.text("")
st.text("")
st.text("")

st.caption('Copyright © MC325D5Y0398 Given Putra')
