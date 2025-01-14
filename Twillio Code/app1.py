# Import necessary libraries
import os
import requests
from twilio.rest import Client
from flask import Flask, request, Response
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Gather

# Load environment variables from .env file
load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "ACbf9eddd99608f8b9247e4fde8e00ed1f")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "966c9120bae93079da3583c52b0d233a")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+12183925356")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Rasa webhook URL
RASA_WEBHOOK_URL = "http://localhost:5005/webhooks/rest/webhook"

# Flask app to act as the TwiML webhook
app = Flask(__name__)

# Function to get a response from Rasa
def get_rasa_response(user_message):
    try:
        payload = {"sender": "user", "message": user_message}
        print(f"Sending to Rasa: {payload}")  # Log the message being sent to Rasa
        response = requests.post(RASA_WEBHOOK_URL, json=payload)
        response_data = response.json()
        print(f"Response from Rasa: {response_data}")  # Log Rasa's response

        # Check if there are multiple responses from Rasa
        responses = []
        for item in response_data:
            if "text" in item:
                responses.append(item["text"])

        # Return multiple responses or a fallback message
        return responses if responses else ["I'm sorry, I didn't understand that."]
    except Exception as e:
        print(f"Error communicating with Rasa: {e}")
        return ["There was an issue connecting to the conversation system."]

# TwiML webhook route to handle call interactions
@app.route("/voice", methods=["POST"])
def voice():
    # Get the caller's input from the Twilio POST request
    user_input = request.form.get("SpeechResult", "")

    # If no speech input, ask for it
    if not user_input:
        response = VoiceResponse()
        gather = Gather(input="speech", timeout=2, speech_model="frustration-aware", hints="hello, goodbye")
        response.append(gather)
        response.redirect("/voice")  # Redirect to /voice if no input received
        return Response(str(response), mimetype="application/xml")

    # If user input is received, call Rasa and get the response
    rasa_responses = get_rasa_response(user_input)

    # Print to debug what Rasa sends back
    print(f"Rasa responses: {rasa_responses}")

    # Build the Twilio response object
    response = VoiceResponse()

    # Loop through all responses from Rasa and speak them one by one
    for rasa_response in rasa_responses:
        gather = Gather(input="speech", timeout=1, speech_model="frustration-aware", hints="hello, goodbye")
        gather.say(rasa_response, voice="en-IN-Standard-D")
        response.append(gather)
        # Add a pause between responses

    # Redirect again to /voice if no "Goodbye" is in the responses
    if not any("goodbye" in r.lower() for r in rasa_responses):
        response.redirect("https://7a29-2401-4900-3dc5-7d5-a84e-bd94-28c6-d32a.ngrok-free.app/voice")

    return Response(str(response), mimetype="application/xml")
# Function to make the initial call
def make_call(to_number):
    try:
        # The Flask server should already be running for this to work
        ngrok_url = "https://7a29-2401-4900-3dc5-7d5-a84e-bd94-28c6-d32a.ngrok-free.app/voice"  # Replace with your actual ngrok URL
        call = client.calls.create(
            url=ngrok_url,
            to=to_number,
            from_=TWILIO_PHONE_NUMBER
        )
        print(f"Call initiated. Call SID: {call.sid}")
    except Exception as e:
        print(f"Error making call: {e}")

# Main function
if __name__ == "__main__":
    # Start the Flask server in a separate thread
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(port=5000, debug=False))
    flask_thread.start()

    # Target phone number (replace with the recipient's verified number)
    recipient_number = "+919354763594"

    # Initiate the call
    make_call(recipient_number)