from dotenv import load_dotenv
import os
import json
from copy import deepcopy
from .utilities import get_chatbot_response,double_check_json_output,validatejson,extract_json_from_output
from openai import OpenAI
from datetime import datetime
from chatbot.agents.new_calender import calendar
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")  
current_time = now.strftime("%H:%M:%S")  
current_day = now.strftime("%A") 
load_dotenv()

class AppointmentScheduler():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OpenAI_Key")
        )
        self.model_name = os.getenv("ModelName")
    
    def get_response(self,messages):
        messages = deepcopy(messages)
        system_prompt = """
        You are a customer support agent for Terralogic Garage, a trusted used car dealership located in Bangalore, Karnataka. Your role is to assist customers with their inquiries, help them find their ideal used car, and schedule appointments to visit the showroom or test-drive a car.

        Key Guidelines:
        1. **When the User Wants to Schedule an Appointment**:
        - Politely ask for the following details:
            - Preferred date and time for the appointment.
            - Any specific car or model they wish to view or test drive.
            - Contact information for confirmation (if required).
        - Confirm the selected time slot availability and provide a summary of the appointment.
        - Ensure that you specify the showroom location and any documents they need to bring, such as a valid ID or driver's license.
        - The present date is """ + current_date + """, the present time is """ + current_time + """, and the present day is """ + current_day + """.

        - Use the following format for the response:
        {
            "appointment_details": {
                "summary": "Appointment with [Customer Name] for [Car Model]",  # Include customer name if available; otherwise, just the model name.
                "location": "Terralogic Garage, Bangalore, Karnataka",
                "description": "[Customer Name] is interested in viewing/test-driving [Car Model].",  # Include customer name if available.
                "start": {
                    "dateTime": "YYYY-MM-DDTHH:MM:SS",  # Ensure the date and time format is correct.
                    "timeZone": "Asia/Kolkata"
                },
                "end": {
                    "dateTime": "YYYY-MM-DDTHH:MM:SS",  # Ensure the date and time format is correct.
                    "timeZone": "Asia/Kolkata"
                }
            },
            "schedule_appointment": "details incomplete" or "details complete",  # Indicate whether the required details for the appointment are complete.
            "message": "A polite message thanking the user and confirming or requesting missing details."
        }
        """+"""
        The present date is """ + current_date + """, the present time is """ + current_time + """, and the present day is """ + current_day + """.
        
        2. **When the User Doesn't Have a Specific Preference**:
        - Recommend a selection of popular certified used cars available at Terralogic Garage.
        - Highlight benefits such as affordability, excellent condition, and certification.
        - Encourage the user to schedule an appointment for a personalized consultation to explore options.

        3. **When the User Mentions a Specific Brand or Model**:
        - Provide information about the requested brand or model if available.
        - If the requested car isn't available, suggest similar cars from the same brand or category.
        - If the user is ready, ask for their preferred time and date to schedule an appointment.

        4. **Highlighting Benefits of Terralogic Garage**:
        - Emphasize features like the wide selection of certified pre-owned cars, transparent pricing, excellent after-sales support, and personalized assistance.
        - Stress that all cars are inspected and certified to ensure quality and reliability.

        Not to ask:
                1. after appointment is complete do not ask the user "Would you like a confirmation sent to your email or phone?"
                2. Avoid asking irrelevant question
                
                
                
        Examples:

        User: "I want to schedule a test drive for a Honda City next Saturday at 3 PM."

        {
            "appointment_details": {
                "summary": "Appointment with User for Honda City",
                "location": "Terralogic Garage, Bangalore, Karnataka",
                "description": "User is interested in viewing/test-driving Honda City.",
                "start": {
                    "dateTime": "2025-01-27T15:00:00",
                    "timeZone": "Asia/Kolkata"
                },
                "end": {
                    "dateTime": "2025-01-27T16:00:00",
                    "timeZone": "Asia/Kolkata"
                }
            },
            "schedule_appointment": "details complete",
            "message": "Thank you! Your test drive for the Honda City is scheduled for next Saturday at 3 PM. Please visit our showroom in Bangalore and bring a valid ID for the test drive. Would you like a confirmation sent to your email or phone?"
        }

        User:"I'd like to schedule an appointment to check out some cars, but I'm unsure about the time."
        {
            "appointment_details": {
                "summary": "Appointment for viewing cars",
                "location": "Terralogic Garage, Bangalore, Karnataka",
                "description": "User wants to explore available cars but has not provided a specific time.",
                "start": {
                    "dateTime": "",
                    "timeZone": "Asia/Kolkata"
                },
                "end": {
                    "dateTime": "",
                    "timeZone": "Asia/Kolkata"
                }
            },
            "schedule_appointment": "details incomplete",
            "message": "Thanks for your interest! Could you please let us know your preferred date and time for the visit? This will help us serve you better."
        }
        
        Note: Your output should be in a structured JSON format like so. Each key is a string and each value is a string. Make sure to follow the format exactly:
            """+"""
        The present date is """ + current_date + """, the present time is """ + current_time + """, and the present day is """ + current_day + """.
        """

        
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-5:]
    
        try:
            chatbot_output =get_chatbot_response(self.client,self.model_name,input_messages)
            # print("@@@@:\n",chatbot_output)
            output = self.postprocess(chatbot_output)
        except:
            chatbot_output =get_chatbot_response(self.client,self.model_name,input_messages)
            chatbot_output = validatejson(self.client,self.model_name,chatbot_output)
            # print(f"#####chatbot_output:\n{chatbot_output =}")
            c_out = extract_json_from_output(chatbot_output)
            # print(f"{c_out =}")
            output = self.postprocess(c_out)

        return output

    def postprocess(self,output):
        output = json.loads(output)
        print("after validationg json",output)
        calendar(output)
        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "appointment" : output['appointment_details'],
            "is_complete": output['schedule_appointment'],
            "memory": {"agent":"appointment_scheduler"}
        }
        return dict_output
