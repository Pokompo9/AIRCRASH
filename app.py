import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    file = "./aircrashes.csv"
    df = pd.read_csv(file)
        
    df = df.dropna(axis = 0)
    df.rename(columns={'Country/Region':'Region'},
           inplace =True)
    df.loc[:, 'Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1), errors='coerce')
    df['Survivor Rate (%)'] = df['Fatalities (air)'] / df['Aboard'] * 100

    return df

df = load_data()

st.title("Air Crashes app from 1952 to Date")

st.write(df)


 # Sidebar filters
st.sidebar.header("Filter Options")

# Years filter
years = df['Year'].unique()
selected_years = st.sidebar.multiselect("Select Years", years, default=years)


# Filter Dataframe based on selection
filtered_df = df[df['Year'].isin(selected_years)]


# display metrics

ground_fatalities = df['Ground'].sum()
air_fatalities = df['Fatalities (air)'].sum()
total_fatalities = air_fatalities + ground_fatalities

st.subheader("Number of Fatalities")
col1, col2, col3, = st.columns(3)

col1.metric("Fatalities on Ground", ground_fatalities)
col2.metric("Total Fatalities", total_fatalities)
col3.metric("Fatalities in Air", air_fatalities)





#1 Crashes per years

st.header('Crashes per Year')

# Group by 'Year' and count the number of crashes per year
crashes_per_year = df.groupby('Year').size().reset_index(name='Crashes by Year')


# Plot as a continuous line graph
plt.figure(figsize=(12, 6))
plt.plot(crashes_per_year['Year'], crashes_per_year['Crashes by Year'],  marker='o')

# Title and labels
plt.xlabel('Year')
plt.ylabel('Number of Crashes')


# Display the graph
plt.tight_layout()
plt.grid(True)
st.pyplot(plt)


#2 Crashes per Aircraft Type

st.header('Crashes per Aircraft Type')

crashes_per_aircraft = df.groupby('Aircraft').size().reset_index(name='Number of Crashes')
crashes_per_aircraft_sorted = crashes_per_aircraft.sort_values(by='Number of Crashes', ascending=False)
top_10_crashes = crashes_per_aircraft_sorted.head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x='Aircraft', y='Number of Crashes', data=top_10_crashes, color='red')
plt.xlabel('Aircraft Type')
plt.ylabel('Number of Crashes')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.tight_layout()
st.pyplot(plt)





#3 Crashes per Country

st.header('Crashes per Country')

crashes_per_region = df.groupby('Region').size().reset_index(name='Crashes by Region')
crashes_per_region_sorted = crashes_per_region.sort_values(by='Crashes by Region', ascending=False)
top_10_region = crashes_per_region_sorted.head(10)

plt.figure(figsize=(12, 6))
plt.barh(top_10_region['Region'], top_10_region['Crashes by Region'], color='blue')
plt.xlabel('Region')
plt.ylabel('Number of Crashes')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.tight_layout()
st.pyplot(plt)



#4 Fatalitites by Month

st.header(' Fatalitites by Month')
monthly_fatalities = df.groupby('Month')['Fatalities (air)'].sum().reset_index(name='Fatalities by air')

plt.figure(figsize=(14, 7))
plt.plot(monthly_fatalities['Month'], monthly_fatalities['Fatalities by air'], marker='o', linestyle='-')
plt.title('Total Fatalities Grouped by Month')
plt.xlabel('Month')
plt.ylabel('Total Fatalities')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)


# Survivor Rate by Year

st.header('Survivor Rate by Year')
yearly_survivor_rate = df.groupby('Year')['Survivor Rate (%)'].mean().reset_index(name = 'Survivor Rate')

plt.figure(figsize=(14, 7))
plt.plot(yearly_survivor_rate['Year'], yearly_survivor_rate['Survivor Rate'], marker='o', linestyle='-')
plt.xlabel('Year')
plt.ylabel('Survivor Rate')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
st.pyplot(plt)
