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
                    [], "hdp8a0duqcvg6bvq4414jof4cs@group.calendar.google.com", #Terapias 
                    [],"o0h3hnmsm3c1f4ogrnbarq9h7g@group.calendar.google.com"] #Dr. Covarrubias Arroyo


def get_events_for_week(service, week_number, year, calendar_id):
    # Obtener el primer día de la semana
    start_date = isoweek.Week(year, week_number).monday().isoformat() + 'Z'

    # Obtener el último día de la semana
    end_date = (isoweek.Week(year, week_number).sunday() + datetime.timedelta(days=1)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId="calendar_id",
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])
    return events

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
        
        #Recorrer todos los calendarios 
        for citas, calendar in calendarios_id: 
            # Recorrer todo el año 2023 por semanas
            for week_number in range(1, 54):  # Ajusta según necesidades específicas

                events = get_events_for_week(service, week_number, 2023, calendar)

                citas.append(len(events)) 

                # for event in events:
                #     start = event["start"].get("dateTime", event["start"].get("date"))
                #     comments = event.get("description", "")
                #     calendar_name = "primary"
                    
                #     # Obtener el año y el mes
                #     start_date = pd.to_datetime(start)
                #     year_month = start_date.to_period("M").strftime("%Y-%m")
                    
                #     event_title = event.get("summary", "Sin título")
                    
                #     # Crear un diccionario para cada evento y agregarlo a la lista
                #     all_events.append({
                #         "Mes": pd.to_datetime(start).to_period("M").strftime("%Y-%m"),
                #         "Calendario del que proviene": calendar_name,
                #         "Titulo del evento": event_title,
                #         "Comentarios del evento": comments,
                #     })

        # Crear un DataFrame a partir de la lista de eventos
        #df = pd.DataFrame(all_events)

        df = pd.DataFrame([(i, len(citas)) for i, (citas, _) in enumerate(calendarios_id)],
                  columns=['Posicion', 'Cantidad'])


        # Guardar el DataFrame en un archivo CSV
        df.to_csv("/home/yuki/Documents/Clinica/Descargas/Citas_completas_2023.csv", index=False, encoding="utf-8")

    except HttpError as error:
        print(f"An error occurred: {error}")

if _name_ == "_main_":
    main()