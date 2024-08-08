# app.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sqlite3
import json

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Connect to SQLite database
conn = sqlite3.connect('university_database.db')
cursor = conn.cursor()

# Define chatbot functions
def process_input(user_input):
	# Tokenize user input
	tokens = word_tokenize(user_input)
	
	# Remove stopwords
	stop_words = set(stopwords.words('english'))
	tokens = [token for token in tokens if token not in stop_words]
	
	# Lemmatize tokens
	lemmatizer = WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(token) for token in tokens]
	
	# Determine intent behind user input
	intent = determine_intent(tokens)
	
	# Retrieve information from database
	if intent == 'course_info':
		course_info = retrieve_course_info(tokens)
		return course_info
	elif intent == 'faculty_info':
		faculty_info = retrieve_faculty_info(tokens)
		return faculty_info
	elif intent == 'campus_events':
		campus_events = retrieve_campus_events(tokens)
		return campus_events
	elif intent == 'student_services':
		student_services = retrieve_student_services(tokens)
		return student_services
	else:
		return "I didn't understand that. Please try again!"

def determine_intent(tokens):
	# Use machine learning algorithm to determine intent
	# For simplicity, we'll use a basic keyword-based approach
	if 'course' in tokens or 'courses' in tokens:
		return 'course_info'
	elif 'faculty' in tokens or 'professor' in tokens:
		return 'faculty_info'
	elif 'event' in tokens or 'events' in tokens:
		return 'campus_events'
	elif 'library' in tokens or 'cafeteria' in tokens:
		return 'student_services'
	else:
		return 'unknown'

def retrieve_course_info(tokens):
	# Retrieve course information from database
	cursor.execute("SELECT * FROM courses WHERE course_name LIKE ?", ('%' + tokens[0] + '%',))
	course_info = cursor.fetchall()
	return course_info

def retrieve_faculty_info(tokens):
	# Retrieve faculty information from database
	cursor.execute("SELECT * FROM faculty WHERE faculty_name LIKE ?", ('%' + tokens[0] + '%',))
	faculty_info = cursor.fetchall()
	return faculty_info

def retrieve_campus_events(tokens):
	# Retrieve campus events from database
	cursor.execute("SELECT * FROM events WHERE event_name LIKE ?", ('%' + tokens[0] + '%',))
	campus_events = cursor.fetchall()
	return campus_events

def retrieve_student_services(tokens):
	# Retrieve student services from database
	cursor.execute("SELECT * FROM services WHERE service_name LIKE ?", ('%' + tokens[0] + '%',))
	student_services = cursor.fetchall()
	return student_services

# Create a Flask API to interact with the chatbot
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot_api():
	user_input = request.get_json()['user_input']
	response = process_input(user_input)
	return jsonify({'response': response})

if __name__ == '__main__':
	app.run(debug=True)