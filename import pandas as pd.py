import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load the Excel file
file_path = "list.xlsx"
excel_file = pd.ExcelFile(file_path)
df = excel_file.parse('Sheet1')

# Set aesthetic style
sns.set(style="whitegrid")

# Convert age to numeric for plotting
df['What is your age?'] = pd.to_numeric(df['What is your age?'], errors='coerce')

# 1. Demographic Overview

# Gender distribution
plt.figure(figsize=(6, 4))
sns.countplot(y='What is your gender?', data=df)
plt.title('Gender Distribution')
plt.xlabel('Count')
plt.ylabel('Gender')
plt.tight_layout()
plt.show()

# Age distribution
plt.figure(figsize=(6, 4))
sns.histplot(df['What is your age?'].dropna(), bins=10, kde=True)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Languages spoken
plt.figure(figsize=(10, 6))
language_series = df['What language(s) do you primarily speak at home? (Select all that apply)'].dropna()
language_counts = language_series.str.split(', ').explode().value_counts()
sns.barplot(y=language_counts.index, x=language_counts.values)
plt.title('Primary Languages Spoken at Home')
plt.xlabel('Count')
plt.ylabel('Language')
plt.tight_layout()
plt.show()

# 2. Sentiment or Readiness Analysis
readiness_cols = [
    'How would you rate your confidence in adapting to a new environment?',
    'How anxious are you about making new friends in the residence?',
    'Do you find it easy to initiate conversations with new people?',
    'How important is it for you to feel close to friends while living in the residence?',
    'How confident are you in building long-term relationships with peers in residence?',
    'Do you feel prepared to live independently in a new environment?',
    'How confident are you in resolving interpersonal conflicts?',
]

for col in readiness_cols:
    if col in df.columns:
        plt.figure(figsize=(8, 4))
        sns.countplot(y=col, data=df, order=df[col].value_counts().index)
        plt.title(f'Response Distribution: {col}')
        plt.xlabel('Count')
        plt.tight_layout()
        plt.show()

# 3. Response Correlation
correlation_df = df[[
    'Do you feel prepared to live independently in a new environment?',
    'How familiar are you with the role of the residence warden in supporting students during their transition to university?',
    'How aware are you of the different student support services (such as counseling, student health, or academic support) available to assist you during your transition?',
    'How well do you know the resources available in student affairs that help students adjust to university life?',
    'How aware are you of how student affairs offices (such as counselling or student health) and the residence warden work together to support new students?'
]].dropna()

plt.figure(figsize=(10, 6))
sns.heatmap(pd.crosstab(correlation_df.iloc[:, 0], correlation_df.iloc[:, 1]), annot=True, cmap="YlGnBu")
plt.title('Preparedness vs. Awareness of Residence Warden Role')
plt.xlabel('Awareness Level')
plt.ylabel('Preparedness')
plt.tight_layout()
plt.show()

# 4. Top Challenges or Excitements (Word Clouds)
challenge_col = 'What do you think will be your biggest challenge in transitioning to residence life?'
excite_col = ' What are you most excited about when thinking of living in the residence?'  # Note the leading space

def generate_wordcloud(text_series, title):
    text = ' '.join(text_series.dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=14)
    plt.tight_layout()
    plt.show()

generate_wordcloud(df[challenge_col], "Top Challenges in Transitioning to Residence Life")
generate_wordcloud(df[excite_col], "Top Excitements About Living in Residence")

# 5. Missing Data Analysis (without missingno)
missing_data = df.isnull().mean().sort_values(ascending=False) * 100
missing_data = missing_data[missing_data > 0]

plt.figure(figsize=(10, 6))
sns.barplot(x=missing_data.values, y=missing_data.index)
plt.title('Missing Data Percentage by Column')
plt.xlabel('Percentage Missing (%)')
plt.ylabel('Survey Questions')
plt.tight_layout()
plt.show()
