# Import necessary libraries
import joblib
import mysql.connector
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS for handling cross-origin requests
import string

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model and vectorizer from files
model = joblib.load('fake_news_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Function to preprocess the text (convert to lowercase, remove punctuation, etc.)
def preprocess_text(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    return text

# Function to check if news is fake or real and save the result to MySQL
def check_news_and_save(news_text):
    processed_text = preprocess_text(news_text)
    features = vectorizer.transform([processed_text])
    prediction = model.predict(features)
    
    result = 'Real' if prediction == 1 else 'Fake'
    
    # Save the article and its classification to the database
    save_to_db(news_text, result)
    
    return result

# Function to save news article to MySQL database
def save_to_db(news_text, classification):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='186707',  # Replace with your MySQL password
            database='fake_news_db'  # Replace with your database name
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (content, classification) VALUES (%s, %s)", (news_text, classification))
        conn.commit()
        cursor.close()
        conn.close()
        print("News article saved to database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Route to handle news checking
@app.route('/check-news', methods=['POST'])
def check_news():
    data = request.get_json()  # Get JSON data from the request
    news_text = data.get('news_text')  # Extract the news text
    result = check_news_and_save(news_text)  # Process the news text
    return jsonify({'result': result})  # Return the result as JSON

# Route for rendering the main page
@app.route('/')
def index():
    return render_template('index.html')  # Assuming index.html is in the templates folder

# Command-line interface for user input (optional)
def main():
    while True:
        news_to_check = input("Enter a news article (or type 'exit' to quit): ")
        if news_to_check.lower() == 'exit':
            break
        result = check_news_and_save(news_to_check)
        print(f"The news article is classified as: {result}")

if __name__ == '__main__':
    app.run(debug=True)  # Run Flask app in debug mode for easier troubleshooting
