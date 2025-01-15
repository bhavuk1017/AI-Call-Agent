# <ins>AI Sales Calling Agent</ins>

This project is an AI-powered calling agent developed specifically for sales purposes. The agent uses Twilio for telephony services, Rasa for conversational AI, and an LLM (Large Language Model) as a fallback when Rasa cannot respond effectively. MongoDB is integrated as a database to store information about the conversations for future analysis.

### [Tutorial and Presentation](https://drive.google.com/drive/folders/13hPMdORz6eg0soao2s_zqBuIleWQwj9M?usp=sharing)

## Features

1.	Sales-Focused Conversations: The agent is optimized to handle sales-related queries and interactions.
2.	Dynamic Conversation Handling:
    •	  Primary: Uses Rasa CALM for predefined conversational flows.
    •	  Fallback: Integrates with an LLM to provide intelligent responses when Rasa fails to understand user input.
3.	Conversation Logging: Stores all conversation data in MongoDB for analysis and tracking.
4.	Speech Recognition: Processes user speech during calls with Twilio’s speech-to-text capabilities.
5.	Interactive Call Flow: Allows for dynamic interactions with users, including handling multiple responses in a single call.
6.	Ngrok Integration: Exposes the Flask server to the public internet for Twilio webhook integration.
7.	Comprehensive Deployment: Includes a PPT and video demonstrating the system’s functionality.

## Usage
![Alt text](https://github.com/user-attachments/assets/e035f70a-5475-43a6-b4d5-3843d009d317)

Step 1: Update Recipient Number

Modify the recipient_number in the app.py file to the target phone number (must be verified in your Twilio account if you’re using a trial account).

Step 2: Make a Call

The Flask server will automatically initiate a call to the recipient once it starts. During the call, the agent will:

•	Use Rasa for predefined sales conversations.

•	Fall back to an LLM for unrecognized inputs.

•	Store conversation data in MongoDB for future analysis.

**Conversation Logging**

MongoDB is used to store the following details:

•	Timestamp of the conversation

•	User inputs

•	Agent responses

•	Call status (e.g., completed, failed)

This data can be used for:

•	Sales performance analysis

•	Conversation quality improvement

•	Customer insights

**Supporting Materials**

•	PPT Presentation: Link to PPT

•	Demonstration Video: Link to Video



## Future Improvements

•	Enhance sales-specific responses by training the Rasa model further.

•	Add analytics for stored MongoDB conversation data.

•	Deploy the solution to a production environment with high availability and scalability.

•	Optimize fallback logic between Rasa and the LLM.



Requirements

•	Python 3.8+

•	Twilio Account with an active phone number

•	Ngrok for public URL exposure

•	Rasa installed and running locally

•	MongoDB instance for conversation data storage

•	Flask framework



**Installation**

<ins>Step 1</ins>: Clone the Repository

	git clone https://github.com/bhavuk1017/AI-Call-Agent.git
	cd ai-sales-calling-agent

<ins>Step 2</ins>: Install Dependencies

	pip install -r requirements.txt

<ins>Step 3</ins>: Configure Environment Variables

Create a .env file in the root directory and set the following environment variables:

	TWILIO_ACCOUNT_SID=your_twilio_account_sid
	TWILIO_AUTH_TOKEN=your_twilio_auth_token
	TWILIO_PHONE_NUMBER=your_twilio_phone_number
	RASA_WEBHOOK_URL=http://localhost:5005/webhooks/rest/webhook
	MONGO_URI=your_mongodb_connection_uri
	LLM_API_KEY=your_large_language_model_api_key


<ins>Step 4</ins>: Start Rasa Server

Ensure that your Rasa server is running:

```rasa run --enable-api```

<ins>Step 5</ins>: Start Ngrok

Start Ngrok to expose your local Flask server to the public internet:

```ngrok http 5000```

Copy the Ngrok URL and update it in the make_call() function within app.py.

<ins>Step 6</ins>: Run the Flask Server

```python app.py```


Debugging

To debug issues, check the following:

1.	Rasa Logs: Ensure Rasa is running and check its logs for errors.
   
	
 2.	Twilio Console: Verify the call status and logs in your Twilio console.
	
 3.	Flask Terminal Logs: The Flask app logs all interactions, including the messages sent to and received from Rasa and the LLM.
	
 4.	MongoDB Logs: Check if the conversation data is being logged correctly in your database.


<ins>**Acknowledgments**</ins>

	
 •	Twilio for telephony services.
	
 •	Rasa for conversational AI.
	
 •	MongoDB for data storage.
	
 •	Ngrok for secure public exposure of the local server.
	
 •	Large Language Models for intelligent fallback responses.

