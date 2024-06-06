from email.policy import HTTP
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

class GoogleCalendar:
    def __init__(self, credentials, idcalendar):
        self.credentials = credentials
        self.idcalendar = idcalendar
        self.service = build("calendar", "v3", credentials=service_account.Credentials.from_service_account_info(self.credentials, scopes= ["https://www.googleapis.com/auth/calendar"]))


    def create_event(self, name_event, start_time, end_time, timezone, attendes = None):
        event = {
            'summary': name_event,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone' : timezone
            }
        }

        if attendes:
            event['attendes'] = [{"email": email} for email in attendes]

        try:
            create_event = self.service.events().insert(calendarId = self.idcalendar, body=event).execute()
        except HttpError as error:
            raise Exception(f"An error as ocurried:{error}")

        return create_event


# Prueba de creacion de evento en calendario
#credentials = st.secrets["google"]["credential_google"]
#id_calendar = "martinez.olivares.006@gmail.com"
#google_calendar = GoogleCalendar(credentials, id_calendar)
#start_time = '2024-06-05T09:00:00-07:00'
#end_time = '2024-06-05T17:00:00-07:00'
#time_zone = 'America/Los_Angeles'
#attendes = ''
#google_calendar.create_event("partido padel", start_time, end_time, time_zone, attendes)
