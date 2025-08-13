# covid19_global_data_tracker.ipynb

# 1️⃣ Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure plots display well
plt.style.use('seaborn-v0_8')
sns.set_palette("muted")

# 2️⃣ Load COVID-19 Dataset
# We'll use the 'Our World in Data' COVID-19 dataset
url = "covid_data_with_population.csv"
print("Loading data... This may take a few seconds.")
df = pd.read_csv(url)

# 3️⃣ Data Exploration
print("\nFirst 5 rows:")
print(df.head())


print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum().head(20))  # Show first 20 columns with missing values

# Select key columns for analysis
data = df[['location', 'date', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'population']]
data['date'] = pd.to_datetime(data['date'])

# 4️⃣ Filter for top 5 countries with highest cases (latest date available)
latest_date = data['date'].max()
latest_data = data[data['date'] == latest_date]
top5_countries = latest_data.nlargest(5, 'total_cases')['location']
print("\nTop 5 Countries by Total Cases:", top5_countries.tolist())

# 5️⃣ Visualization 1: Total cases over time for top 5 countries
plt.figure(figsize=(12,6))
for country in top5_countries:
    country_data = data[data['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title("Total COVID-19 Cases Over Time - Top 5 Countries")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.tight_layout()
plt.show()

# 6️⃣ Visualization 2: New cases over time for top 5 countries
plt.figure(figsize=(12,6))
for country in top5_countries:
    country_data = data[data['location'] == country]
    plt.plot(country_data['date'], country_data['new_cases'], label=country)

plt.title("Daily New COVID-19 Cases - Top 5 Countries")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.legend()
plt.tight_layout()
plt.show()

# 7️⃣ Visualization 3: Death rate comparison (latest date)
latest_data['death_rate'] = (latest_data['total_deaths'] / latest_data['total_cases']) * 100
death_rate_top5 = latest_data[latest_data['location'].isin(top5_countries)]

plt.figure(figsize=(8,5))
sns.barplot(x='location', y='death_rate', data=death_rate_top5)
plt.title("COVID-19 Death Rate (%) - Top 5 Countries")
plt.ylabel("Death Rate (%)")
plt.xlabel("Country")
plt.tight_layout()
plt.show()

# 8️⃣ Insights
print("\n📊 Key Insights:")
print("- Countries with the highest cases are", ", ".join(top5_countries))
print("- Death rate varies between countries despite similar case counts.")
print("- New cases trends reveal peaks and declines that may match lockdown or vaccination periods.")
