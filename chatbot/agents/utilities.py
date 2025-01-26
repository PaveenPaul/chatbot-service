from datetime import datetime

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")  
current_time = now.strftime("%H:%M:%S")  
current_day = now.strftime("%A") 

def get_chatbot_response(client,model_name,messages,temperature=0):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000,
    ).choices[0].message.content
    
    return response

def get_embedding(embedding_client,model_name,text_input):
    output = embedding_client.embeddings.create(input = text_input,model=model_name)
    
    embedings = []
    for embedding_object in output.data:
        embedings.append(embedding_object.embedding)

    return embedings

def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(client,model_name,messages)

    return response

def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(client,model_name,messages)

    return response

def validatejson(client, model_name, json_string):
    
    
    if isinstance(json_string, list):
        json_string = "\n".join(json_string) 
    system_prompt = f"""
        You are a JSON validation agent. Your role is to validate the JSON input provided by the chatbot to ensure it adheres to the required structure.
        Only return the validated JSON if it matches the specified format. If the JSON is invalid or incomplete, return an error message explaining the issue.
        The present JSON structure to validate is:
        timeZone should always be "Asia/Kolkata", set the date time based on the todays date {current_date} , the time now is {current_time} and todays Day is {current_day}
        {json_string}

        ### Expected JSON Structure:
        
        {{
            "appointment_details": {{
                "summary": "string",  
                "location": "string",  
                "description": "string",  
                "start": {{
                    "dateTime": "string",  
                    "timeZone": "string"  
                }},
                "end": {{
                    "dateTime": "string", 
                    "timeZone": "string" 
                }}
            }},
            "schedule_appointment": "details complete" or "details incomplete",  # Indicates if all details are provided
            "message": "string"  # Response message to the user (must not be empty)
        }}

        
        Do NOT return a single letter, explanation, or any text outside of the JSON response.

    """
    
   
    messages = [{"role": "user", "content": system_prompt}]
    
    
    response = get_chatbot_response(client, model_name, messages)
 
    return response


def extract_json_from_output(chatbot_output):
    import re
    import json
 
    json_match = re.search(r'```(?:json|write)\n(.*?)\n```', chatbot_output, re.DOTALL)

    if json_match:
        json_string = json_match.group(1)  
        try:
            json_data = json.loads(json_string)  
            return json_string
        except json.JSONDecodeError as e:
            return {"error": f"Failed to decode JSON: {e}"}
    else:
        return {"error": "No JSON found in the input."}