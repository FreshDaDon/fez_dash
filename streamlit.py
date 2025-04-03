import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Page configuration
st.set_page_config(
    page_title="Student Readiness Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        h1, h2, h3, h4 {
            color: #003366;
        }
        .stButton>button {
            background-color: #003366;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("First-Year Student Transition Insights")
st.markdown("Gain meaningful insights into how students are transitioning into residence life through this interactive analytics dashboard.")

# Upload
uploaded_file = st.sidebar.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')

    # Sidebar Navigation
    st.sidebar.header("Navigation")
    option = st.sidebar.radio("Select Section", [
        "Demographic Overview",
        "Sentiment & Readiness",
        "Preparedness vs Support Awareness",
        "Word Cloud Insights",
        "Missing Data Report"
    ])

    if option == "Demographic Overview":
        st.header("Demographic Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Gender Distribution")
            fig, ax = plt.subplots()
            sns.countplot(y='What is your gender?', data=df, ax=ax, palette="Set2")
            st.pyplot(fig)

        with col2:
            st.subheader("Age Group Distribution")
            age_order = ['Under 18', '18-20', '21-24', '25-29', '30 and above']
            df['What is your age?'] = df['What is your age?'].astype(str)
            fig, ax = plt.subplots()
            sns.countplot(y='What is your age?', data=df, order=[age for age in age_order if age in df['What is your age?'].unique()], palette="Blues_d", ax=ax)
            st.pyplot(fig)

        st.subheader("Languages Spoken at Home")
        language_series = df['What language(s) do you primarily speak at home? (Select all that apply)'].dropna()
        language_counts = language_series.str.split(', ').explode().value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(y=language_counts.index, x=language_counts.values, ax=ax, palette="coolwarm")
        st.pyplot(fig)

    elif option == "Sentiment & Readiness":
        st.header("Sentiment and Readiness")
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
                st.subheader(col)
                fig, ax = plt.subplots()
                sns.countplot(y=col, data=df, order=df[col].value_counts().index, palette="pastel", ax=ax)
                st.pyplot(fig)

    elif option == "Preparedness vs Support Awareness":
        st.header("Correlation Between Preparedness and Institutional Awareness")
        cols_of_interest = [
            'Do you feel prepared to live independently in a new environment?',
            'How familiar are you with the role of the residence warden in supporting students during their transition to university?',
        ]
        corr_df = df[cols_of_interest].dropna()

        if not corr_df.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(pd.crosstab(corr_df.iloc[:, 0], corr_df.iloc[:, 1]), annot=True, cmap="YlOrBr", ax=ax)
            st.pyplot(fig)
        else:
            st.info("Not enough data to generate correlation heatmap.")

    elif option == "Word Cloud Insights":
        st.header("Word Cloud Insights")

        def plot_wordcloud(column, label):
            if column in df.columns:
                text = " ".join(df[column].dropna().astype(str))
                if text:
                    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
                    fig, ax = plt.subplots()
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis('off')
                    st.subheader(label)
                    st.pyplot(fig)

        plot_wordcloud('What do you think will be your biggest challenge in transitioning to residence life?', "Biggest Challenges")
        plot_wordcloud('\u00a0What are you most excited about when thinking of living in the residence?', "Most Exciting Aspects")

    elif option == "Missing Data Report":
        st.header("Missing Data Overview")
        missing_data = df.isnull().mean().sort_values(ascending=False) * 100
        missing_data = missing_data[missing_data > 0]

        if not missing_data.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=missing_data.values, y=missing_data.index, palette="mako", ax=ax)
            ax.set_xlabel("Missing %")
            ax.set_ylabel("Survey Fields")
            st.pyplot(fig)
        else:
            st.success("No missing data detected in the dataset.")
else:
    st.info("Please upload your Excel survey file to begin analysis.")
