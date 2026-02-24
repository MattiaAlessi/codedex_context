import pandas as pd

# Load the dataset (make sure the CSV file is in the working directory)
df = pd.read_csv('breached_services_info.csv')

# Convert 'BreachDate' and 'AddedDate' to datetime
df['BreachDate'] = pd.to_datetime(df['BreachDate'], errors='coerce')
df['AddedDate'] = pd.to_datetime(df['AddedDate'], errors='coerce')

# Check for any missing values
df.isnull().sum()

# Fill missing values or drop them (depending on the column)
# In this case, we can drop rows where 'PwnCount' is missing
df = df.dropna(subset=['PwnCount'])

# Preview the data
df.head()



import matplotlib.pyplot as plt

# Extract year from BreachDate
df['BreachYear'] = df['BreachDate'].dt.year

# Count breaches per year
breach_counts = df['BreachYear'].value_counts().sort_index()

# Plot the data
plt.figure(figsize=(10,6))
breach_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Breaches per Year')
plt.xlabel('Year')
plt.ylabel('Number of Breaches')
plt.xticks(rotation=45)
plt.show()



import ast

# Convert the 'DataClasses' column from string to list (it was stored as a string representation of a list)
df['DataClasses'] = df['DataClasses'].apply(ast.literal_eval)

# Flatten the list of data classes and count the occurrences
data_classes = [item for sublist in df['DataClasses'] for item in sublist]
data_classes_count = pd.Series(data_classes).value_counts()

# Plot the most common data classes exposed
plt.figure(figsize=(10,6))
data_classes_count.head(10).plot(kind='barh', color='coral')
plt.title('Top 10 Exposed Data Classes')
plt.xlabel('Frequency')
plt.ylabel('Data Class')
plt.show()



# Boxplot for PwnCount based on verification status
import seaborn as sns

plt.figure(figsize=(10,6))
sns.boxplot(x='IsVerified', y='PwnCount', data=df)
plt.title('PwnCount vs Verification Status')
plt.xlabel('Is Verified')
plt.ylabel('Pwn Count')
plt.show()



# Sort the data by 'PwnCount' and plot the top services
top_services = df[['Name', 'PwnCount']].sort_values(by='PwnCount', ascending=False).head(10)

plt.figure(figsize=(12,6))
plt.barh(top_services['Name'], top_services['PwnCount'], color='lightgreen')
plt.title('Top 10 Services with the Most Breached Records')
plt.xlabel('Pwn Count')
plt.ylabel('Service Name')
plt.gca().invert_yaxis()  # To display the top service at the top
plt.show()