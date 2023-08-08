import openai
import pyAudioAnalysis as paa
import pickle
from keys import OPENAI_API_KEY
from prompts import create_prompt, INITIAL_RESPONSE
import time

openai.api_key = "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"

# Loading the Trained GMM Model
with open('/Users/supreme/your_gmm.pkl', 'rb') as file:
    your_gmm = pickle.load(file)

print("GMM model loaded successfully")

def recognize_speaker(transcript_audio):
    transcript_features = paa.audioFeatureExtraction(transcript_audio, 0.050, 0.025, 0.010, 0.005)
    score = paa.speakerRecognition(transcript_features, your_gmm)
    
    if score > 0.85:
        print("Your voice detected.")
        return True
    else:
        print("Different voice detected.")
        return False

def generate_response_from_transcript(transcript):
    try:
        # Assuming transcript is the path to the audio file
        with open(transcript, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
    except Exception as e:
        print(e)
        return ''
    
    # Additional logic to generate response using the GPT model, if required
    full_response = response['choices'][0]['message']['content'] # Modify as needed
    try:
        return full_response.split('[')[1].split(']')[0]
    except:
        return response

class GPTResponder:
    def __init__(self):
        self.response = INITIAL_RESPONSE
        self.response_interval = 2

    def update_response_interval(self, update_interval):
        # You can implement the logic to update the response interval here
        # For now, I'll just assign the value directly
        self.response_interval = update_interval

    def respond_to_transcriber(self, transcriber):
        while True:
            if transcriber.transcript_changed_event.is_set():
                start_time = time.time()
                transcript_audio = transcriber.get_audio() # Replace with the correct method to access audio
                is_recognized = recognize_speaker(transcript_audio)
                
                if is_recognized:
                    # Assuming you have a method to get the transcript from transcriber
                    transcript = transcriber.get_transcript()
                    response = generate_response_from_transcript(transcript)
                    self.response = response
                else:
                    # Handle different voice logic, if needed
                    pass
