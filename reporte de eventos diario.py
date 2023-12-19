import datetime
import os.path
import csv
import pandas as pd
import isoweek
import numpy as np

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

calendarios_id = [( [], "clinicamedicadeporte2@gmail.com"), #Dr. Covarrubias Mata
                    ([], "hdp8a0duqcvg6bvq4414jof4cs@group.calendar.google.com"), #Terapias 
                    ([], "o0h3hnmsm3c1f4ogrnbarq9h7g@group.calendar.google.com")] #Dr. Covarrubias Arroyo
def get_events_for_day(service, year, month, day, calendar_id):
    # Obtener el primer día del mes
    start_date = f"{year}-{month:02d}-01T00:00:00Z"

    # Obtener el primer día del mes siguiente para determinar el final del rango
    next_month = month % 12 + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year
    end_date = f"{next_year}-{next_month:02d}-01T00:00:00Z"

    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy="startTime",
            maxResults=300,  # Ajusta según tus necesidades
        ).execute()
        events = events_result.get("items", [])
        return events
    except HttpError as e:
        print(f"Error fetching events: {e}")
        return []



def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        all_events = []  # Lista para almacenar todos los eventos

        month = 12; 
        for citas, calendar in calendarios_id:
            events = get_events_for_day(service, 2024, month, calendar)
            citas.append(len(events))

        directorio_de_salida = "/home/yuki/Documents/Clinica/Descargas/Citas_" + month + ".csv" 
        # Abre un archivo CSV en modo escritura ('w', newline='') y crea un objeto writer
        with open(directorio_de_salida, 'w', newline='') as csvfile:
            # Define el objeto writer usando la coma como delimitador
            csv_writer = csv.writer(csvfile, delimiter=',')

            # Itera sobre las tuplas en calendarios_id
            for citas, _ in calendarios_id:
                csv_writer.writerow(citas)



    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Error details: {error.content}")

if __name__ == "__main__":
    main()