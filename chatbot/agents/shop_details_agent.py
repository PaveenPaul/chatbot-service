from dotenv import load_dotenv
import os
import json
from copy import deepcopy
from .utilities import get_chatbot_response
from openai import OpenAI
load_dotenv()

class Shop_DetailsAgent():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OpenAI_Key")
        )
        self.model_name = os.getenv("ModelName")
    
    def get_response(self,messages):
        messages = deepcopy(messages)
        system_prompt = """
            Welcome to Terralogic Garage, your trusted partner in finding the perfect car that suits your lifestyle and needs. Located in the heart of Bangalore, Karnataka, we specialize in providing top-notch services for both new and used cars. Whether you’re upgrading to a new model or exploring options for a pre-owned vehicle, Terralogic Garage is here to make your journey seamless and rewarding.

            What We Offer
            Wide Selection of Cars: Our showroom boasts an extensive collection of both new and certified pre-owned cars, ensuring you’ll find the ideal match for your preferences and budget.
            Personalized Assistance: Our team of experienced professionals is dedicated to guiding you through every step, from exploring features to comparing models, ensuring a stress-free decision-making process.
            Appointment Scheduling: For new car purchases, we offer appointment scheduling with our knowledgeable sales representatives, making it easier for you to plan and explore options at your convenience.
            After-Sales Support: At Terralogic Garage, our relationship doesn’t end with the purchase. We provide exceptional after-sales services to keep your car in prime condition.
            Our Location
            We are conveniently located in Bangalore, Karnataka, India, making us easily accessible to customers across the city and surrounding areas. Visit us to explore our showroom and experience our exceptional service firsthand.

            Working Hours
            Monday to Friday: 10:00 AM to 6:00 PM
            Saturday: 10:00 AM to 2:00 PM
            Sundays : 10:00 AM to 2:00 PM
            Why Choose Us?
            Customer-Centric Approach: Your satisfaction is our top priority, and we strive to exceed your expectations at every step.
            Transparent Transactions: With us, you can be assured of complete transparency in pricing and quality, whether you’re buying a new car or a pre-owned vehicle.
            Expert Advice: Our team is equipped with extensive knowledge of the latest car models, features, and industry trends to help you make an informed decision.
            At Terralogic Garage, we are committed to delivering an exceptional car-buying experience that’s tailored to your unique needs. We invite you to visit our showroom and embark on the journey to find your dream car today!

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the points above and see if the message lies under this point or not. Then you write some your thoughts about what point is this input relevant to.
            "decision": "complete" 
            "message": "Reply to the Customer"
            }
            """
        
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output = get_chatbot_response(self.client,self.model_name,input_messages)
        output = self.postprocess(chatbot_output)
        # print(f"shop details:\n{output =}")
        return output

    def postprocess(self,output):
        output = json.loads(output)
        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {"agent":"shop_details_agent",
                       "guard_decision": output['decision']
                      }
        }
        return dict_output
