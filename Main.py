import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Fetch data from Remotive
url = "https://remotive.com/api/remote-jobs"
res = requests.get(url)
data = res.json()["jobs"]

# Convert to DataFrame
df = pd.DataFrame(data)

# Preview structure
print(df.shape)
print(df.columns.tolist())
df.head()

# Cleaned DataFrame
df_clean = df[[
    'title', 'company_name', 'category', 'tags',
    'job_type', 'publication_date',
    'candidate_required_location', 'salary'
]]

# Convert date to datetime
df_clean['publication_date'] = pd.to_datetime(df_clean['publication_date'])

# Set style
sns.set(style="whitegrid")

# 1. Top 10 job categories
plt.figure(figsize=(10, 5))
df_clean['category'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Tech Job Categories")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Job types distribution
plt.figure(figsize=(6, 4))
df_clean['job_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title("Job Type Distribution")
plt.ylabel('')
plt.tight_layout()
plt.show()

# 3. Jobs over time
plt.figure(figsize=(12, 4))
df_clean['publication_date'].dt.date.value_counts().sort_index().plot()
plt.title("Jobs Posted Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.show()

# 4. Top 10 hiring locations
plt.figure(figsize=(10, 5))
df_clean['candidate_required_location'].value_counts().head(10).plot(kind='bar', color='lightgreen')
plt.title("Top 10 Hiring Locations")
plt.ylabel("Number of Jobs")
plt.xlabel("Location")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Flatten the list of all tags into a single list
all_tags = df_clean['tags'].explode()
tag_counts = Counter(all_tags)

# Convert to DataFrame
tag_df = pd.DataFrame(tag_counts.most_common(15), columns=['Skill', 'Count'])

# Plot
plt.figure(figsize=(10, 5))
sns.barplot(data=tag_df, x='Skill', y='Count', palette='mako')
plt.title("Top 15 In-Demand Tech Skills")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Count how many jobs have salary info
has_salary = df_clean['salary'].notnull().sum()
print(f"Jobs with salary info: {has_salary} / {len(df_clean)}")

# Show common salary patterns
df_clean['salary'].dropna().value_counts().head(10)

# Clean ranges into categories
df_clean['salary_range'] = df_clean['salary'].str.extract(r'(\$\d{2,3},?\d*\s?-\s?\$\d{2,3},?\d*)')
df_clean['salary_range'].value_counts().head(10).plot(kind='barh', figsize=(10, 5), color='coral')
plt.title("Top Salary Ranges Mentioned")
plt.xlabel("Number of Jobs")
plt.tight_layout()
plt.show()