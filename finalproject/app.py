from flask import Flask, render_template, Response, request, send_file, jsonify
import cv2
import numpy as np
from keras.models import load_model
from gtts import gTTS
import os
import pickle
import requests
from openai import AzureOpenAI
import time
from collections import Counter
from datetime import datetime


app = Flask(__name__)

# Paths and models
emotion_model_path = 'models/fer2013_mini_XCEPTION.102-0.66.hdf5'
known_faces_file = 'known_faces.pkl'  # File to save known faces data

# Load the emotion detection model
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize Haar cascade for face detection
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_detector = cv2.CascadeClassifier(haar_file)
emotion_history = []

# Initialize text-to-speech engine
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('afplay output.mp3')  # Replace 'afplay' with suitable command for your OS


# Load known faces
def load_known_faces():
    if os.path.exists(known_faces_file):
        with open(known_faces_file, 'rb') as file:
            known_face_encodings, known_face_names = pickle.load(file)
    else:
        known_face_encodings, known_face_names = [], []
    return known_face_encodings, known_face_names


# Save known faces
def save_known_faces(known_face_encodings, known_face_names):
    with open(known_faces_file, 'wb') as file:
        pickle.dump((known_face_encodings, known_face_names), file)

# Save new face
def save_new_face(face_encoding, name, known_face_encodings, known_face_names):
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)
    save_known_faces(known_face_encodings, known_face_names)

# Function to capture new user's name
def get_user_name():
    name = input("Please type your name: ")
    speak(f"Nice to meet you, {name}!")
    return name

# Function to detect emotion
def detect_emotion(face):
    face = cv2.resize(face, (64, 64))
    face = face.astype('float32') / 255.0
    face = np.expand_dims(face, axis=-1)  # Add a single channel dimension
    face = np.expand_dims(face, axis=0)  # Add batch dimension
    emotion_prediction = emotion_classifier.predict(face)[0]
    max_index = np.argmax(emotion_prediction)
    return emotion_labels[max_index]
    
def send_to_openai(message):
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        api_key="a284de3e1b2348b0b0151b2e67a63a5c",
        api_version="2024-02-01",
        azure_endpoint="https://thesisproject.openai.azure.com/"
    )

    # Empathetic system message
    system_message = {
        "role": "system",
        "content": "Your name is Karla,You are a sensitive and empathetic assistant. Respond with care and understanding to the user's feelings."
    }
    
    # Send the message to the OpenAI API with the context
    response = client.chat.completions.create(
        model="thesis",  # Specify the model you want to use
        messages=[system_message, {"role": "user", "content": message}]
    )
    return response.choices[0].message.content.strip()



def generate_frames(name):
    global emotion_history
    known_face_encodings, known_face_names = load_known_faces()
    webcam = cv2.VideoCapture(0)
    initial_greeting = True
    
    # Initialize variables
    start_time = time.time()
    emotion_list = []
    capture_duration = 20  # Capture duration in seconds

    while True:
        ret, frame = webcam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_gray = gray[y:y+h, x:x+w]

            # Encode face for recognition (you need to implement this part)
            face_encoding = None  # Replace with actual face encoding logic

            # Detect emotion
            emotion = detect_emotion(face_gray)
            # Track the detected emotion with date and time

            # Speak initial greeting and ask for name
            if initial_greeting:
                speak("Hello, I'm your AI assistant Karla. What's your name?")
                initial_greeting = False

            # If name is provided, save and greet with emotion
            if name and face_encoding is not None and face_encoding not in known_face_encodings:
                save_new_face(face_encoding, name, known_face_encodings, known_face_names)
                start_time = time.time()

            # Capture emotions for the specified duration
            if start_time and (time.time() - start_time <= capture_duration):
                emotion_list.append(emotion)
            
            # Draw rectangle around the face and emotion text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            
            # Display name if provided
            if name:
                cv2.putText(frame, f"Name: {name}", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Check if the capture duration has passed
        if start_time and (time.time() - start_time > capture_duration):
            most_common_emotion = Counter(emotion_list).most_common(1)[0][0]
            print(f"The general felt emotion over the last {capture_duration} seconds is: {most_common_emotion}")
           
            # Create the final message based on emotion
            if most_common_emotion == "Sad":
                final_message = f"Hello {name}, you seem sad. I'm here to help. Is there anything specific you'd like to talk about or do you need some support?"
            elif most_common_emotion == "Happy":
                final_message = f"Hello {name}, it looks like you're feeling great! How can I assist you in this cheerful mood?"
            else:
                final_message = f"Hello {name}, it looks like you seem to be feeling {most_common_emotion}. How can I assist you today?"
            
            # Send the final message to the chat interface
            send_chat_message(final_message)
            emotion_history.append({'emotion': most_common_emotion, 'timestamp': datetime.now()})
         


    webcam.release()


@app.route('/emotion_history_page')
def emotion_history_page():
    return render_template('emotion_history.html')

@app.route('/emotion_history', methods=['GET'])
def get_emotion_history():
    global emotion_history
    return jsonify({'emotion_history': emotion_history})

def send_chat_message(message):
    # Send the message to the chat interface
    response = requests.post('http://localhost:5000/chat', json={'message': message})
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")

def get_most_common_emotion(name):
    # Call your generate_frames function to get the most common emotion
    most_common_emotion = generate_frames(name)
    return most_common_emotion



@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if message:
        # Process the user message with OpenAI API
        response = send_to_openai(message)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'No message provided'}), 400

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    name = request.args.get('name', '')
    return Response(generate_frames(name), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/output.mp3')
def output():
    return send_file('output.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
