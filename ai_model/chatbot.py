import openai
import os
from flask import Flask, request, jsonify
import traceback

openai.api_key = "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"

app = Flask(__name__)

@app.errorhandler(500)
def handle_internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "details": str(error), "trace": traceback.format_exc()}), 500

@app.route("/")
def engine():
    # Detect if firebase collection has been updated
    
    # Fetch entire firebase data collection and initiate messages with it
    
    # Generate response
    
    # Add to response collection in firebase

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# messages=[{"role": "system", "content": "You are Valara, a personal health coach and emotional support figure. You place an emphasis on providng the user with an in-depth feedback on the health data you receive"}]

# def generate_response(prompt):
#     messages.append({"role": "user", "content": prompt})
    
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         temperature = 0.7,
#         messages=messages
#     )
    
#     messages.append(response.choices[0].message)
    
#     return response.choices[0].message.content

# while True:
#     input_prompt = input("Chat: ")
#     output_response = generate_response(input_prompt)
#     print(output_response + "\n\n")

prompt = "Based on the user's heart rate of {heart_rate}, sleep quality of {sleep_quality}, activity level of {activity_level}, and mood scores of {mood_scores} over the past week, provide a summary and health advice. Use second person pronouns and have an understanding tone"

prompt2 = "Given my average steps of {avg_steps}, hours of sleep of {sleep_hours}, and emotional state of {emotional_state}, point the data out first, then suggest ways to improve my health and wellbeing."

prompt3 = "Analyze the correlation between the user's mood {mood_list}, their sleep quality {sleep_quality_list}, and their activity levels {activity_levels_list} over the past month.. Use second person pronouns, and provide output in a way that demonstrates compassion towards the user"

prompt4 = "Based on the user's sleep patterns {sleep_patterns} and their daily activity schedule {activity_schedule}, suggest the most optimal sleep cycle for them, pointing out the recommended sleep and wake up times. Provide response from the perspective of a caring health professional who just recieved data from a patient, using second person pronouns."
# EOD, get data from health api



# Make suggestions


'''Example data that we can fetch using apple health api (// means verfication in progress)
step-count : 10000
body-mass: 50kg
body-fat percentage: 25%
heart-rate: 99bpm
sleep related
//bedtime: 3am
//wake-up time: 9am
//sleep-amount: 6 hours
blood glucose levels: 130mg/dl
blood pressure levels: 116mmHg/ 72mmHg 
respiratory rate: 12 breaths/min'''