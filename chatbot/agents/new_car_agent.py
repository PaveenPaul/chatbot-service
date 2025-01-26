from dotenv import load_dotenv
import os
from .utilities import get_chatbot_response,get_embedding
from openai import OpenAI
from copy import deepcopy
from pinecone import Pinecone
load_dotenv()

class NewCar_details():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OpenAI_Key"),
        )
        self.embedding_client = OpenAI(
            api_key=os.getenv("OpenAI_Key"), 
        )
        self.model_name = os.getenv("ModelName")
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_NEW_INDEX_NAME")
    
    def get_closest_results(self,index_name,input_embeddings,top_k=3):
        index = self.pc.Index(index_name)
        
        results = index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )

        return results

    def get_response(self,messages):
        messages = deepcopy(messages)

        user_message = messages[-1]['content']
        embedding = get_embedding(self.embedding_client,self.embedding_model_name,user_message)[0]
        result = self.get_closest_results(self.index_name,embedding)
        source_knowledge = "\n".join([x['metadata']['text'].strip()+'\n' for x in result['matches'] ])

        prompt = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """
        system_prompt = """
        You are a customer support agent for Terralogic Garage, a trusted used car dealership located in Bangalore, Karnataka. Your role is to engage with potential customers, answer their queries about pre-owned cars, and assist them in finding the perfect vehicle based on their needs. 

        Key Guidelines:
        1. **When the User Doesn't Have a Specific Preference**:
        - Recommend a selection of popular certified used cars available at Terralogic Garage.
        - Highlight the benefits of these cars, such as affordability, excellent condition, and certification.
        - Encourage the user to visit the showroom or schedule an appointment for a personalized consultation.

        2. **When the User Mentions a Specific Brand or Model**:
        - Provide information about the requested brand or model if available.
        - If the requested car isn't available, suggest similar cars from the same brand or alternatives within the same price range or category.
        - Convince the user to explore these options at Terralogic Garage.

        3. **When the User is Interested in a Specific Car and Wants to Schedule an Appointment**:
        - Focus on scheduling the appointment.
        - Avoid recommending additional cars unless explicitly asked.
        - Provide details about the available time slots, the showroom location, and any required documents for the appointment.

        4. **Highlighting Benefits of Terralogic Garage**:
        - Emphasize features like the wide selection of certified pre-owned cars, transparent pricing, excellent after-sales support, and personalized assistance.
        - Stress that all cars are inspected and certified to ensure quality and reliability.

        You are free to decide the Price of the Model if Price is asked but make sure the you use 'Price for the Base Model' and You can also provide additional information about the Model if asked.
        Ensure that every interaction feels welcoming, professional, and customer-focused. Encourage the user to take the next step, whether it’s exploring available options, scheduling an appointment, or visiting the showroom in person. Always adapt your responses based on the user’s needs and preferences.
        
        """
        
        messages[-1]['content'] = prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output =get_chatbot_response(self.client,self.model_name,input_messages)
        output = self.postprocess(chatbot_output)
        # print(f"New Car:\n{output =}")
        return output

    def postprocess(self,output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {"agent":"new_car_agent"
                      }
        }
        return output
