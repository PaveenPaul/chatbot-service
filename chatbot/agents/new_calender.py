import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
load_dotenv()


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def calendar(json_data):
    if json_data.get('schedule_appointment') == 'details complete':
    
        appointment_details = json_data.get('appointment_details', {})
        summary = appointment_details.get('summary', 'No summary provided')
        location = appointment_details.get('location', 'No location provided')
        description = appointment_details.get('description', 'No description provided')
        start = appointment_details.get('start', {})
        end = appointment_details.get('end', {})

        creds = None
        token_path=os.getenv("token_json")
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file("token.json")
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credss=os.getenv("cred_path")
                flow = InstalledAppFlow.from_client_secrets_file(
                   credss, SCOPES
                )
                creds = flow.run_local_server(port=0)
                
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        
        try:
            service = build("calendar", "v3", credentials=creds)
            event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start.get("dateTime"),
                "timeZone": start.get("timeZone"),
            },
            "end": {
                "dateTime": end.get("dateTime"),
                "timeZone": end.get("timeZone"),
            },
            }
            event = service.events().insert(calendarId="primary", body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
                
        except HttpError as exp:
            print(f"HttpError occurred: {exp}")
            print(f"Details: {exp.content.decode('utf-8')}")
    else:
        print(str("details incomplete").upper())
        
if __name__ == "__main__":
    calendar()
