import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def load_data():
    # Load the CSV file
    data = pd.read_csv('Hotel_Reviews.csv')
    return data

def display_wordcloud(data, column, background_color='white'):
    # Concatenate all reviews in the column
    text = ' '.join(review for review in data[column] if review not in ['No Negative', 'No Positive', ''])
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color=background_color).generate(text)
    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt.gcf())  # Show the matplotlib figure in Streamlit
    plt.close()  # Close the figure to prevent it from displaying again in the notebook output

# Main function to run the app
def main():
    # Apply styles for the background color and other elements
    st.markdown("""
        <style>
        .stApp {
            background-color: #E6E6FA;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #6A0DAD;
            margin-bottom: 25px !important;
        }
        h1, .stTextInput > div > div > input, .stSelectbox > div > div {
            color: #4B0082;
        }
        .st-bb {
            background-color: transparent;
        }
        .st-at {
            background-color: #E6E6FA;
        }
        .st-cx {
            background-color: #E6E6FA;
        }
        .reportview-container .main .block-container {
            padding-top: 5rem;
            padding-bottom: 5rem;
        }
        .bold-label {
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    # Display 'PRANAVHOTELS.com' in the top left corner
    st.markdown('<div class="logo-text">PRANAVHOTELS.com</div>', unsafe_allow_html=True)

    st.title('Travel Vista - Your Hotel Search Ends Here')

    # Load data
    data = load_data()

    # Bolded Search for Hotel Name
    st.markdown('**Enter hotel name to search**')
    hotel_name = st.text_input('', key='hotel_name')
    filtered_data = data
    if hotel_name:
        filtered_data = filtered_data[filtered_data['Hotel_Name'].str.contains(hotel_name, case=False, na=False)]

    # Bolded Using 'Reviewer_Nationality' column for filtering
    if 'Reviewer_Nationality' in filtered_data.columns and filtered_data.shape[0] > 0:
        st.markdown('**Choose a nationality**')
        nationality = st.selectbox('', options=['All'] + list(filtered_data['Reviewer_Nationality'].unique()), key='nationality')
        if nationality != 'All':
            filtered_data = filtered_data[filtered_data['Reviewer_Nationality'] == nationality]

    # Button to display the data
    if st.button('Show Data'):
        st.dataframe(filtered_data)

    # Word cloud generation
    if st.button('Generate Word Clouds for Positive Reviews') and hotel_name:
        display_wordcloud(filtered_data, 'Positive_Review')

    if st.button('Generate Word Clouds for Negative Reviews') and hotel_name:
        display_wordcloud(filtered_data, 'Negative_Review', background_color='black')

# Ensures the main function is called only when the script is run directly
if __name__ == "__main__":
    main()