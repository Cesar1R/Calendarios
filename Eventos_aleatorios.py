import random
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Credenciales de la cuenta de servicio


if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
# Save the credentials for the next run
with open("token.json", "w") as token:
  token.write(creds.to_json())


# Crear un cliente de la API de Google Calendar
service = build("calendar", "v3", credentials=creds)

# Obtener lista de calendarios del usuario
calendar_list = service.calendarList().list().execute()

# IDs de los calendarios disponibles
calendar_ids = [calendar['id'] for calendar in calendar_list.get('items')]

# Colores para los eventos (puedes modificar o agregar más colores según sea necesario)
colors = [
    {'colorId': '1', 'background': '#a4bdfc', 'foreground': '#1d1d1d'},  # Azul
    {'colorId': '2', 'background': '#7ae7bf', 'foreground': '#1d1d1d'},  # Verde
    {'colorId': '3', 'background': '#dbadff', 'foreground': '#1d1d1d'},  # Morado
    # ... Puedes agregar más colores aquí
]

# Función para generar eventos aleatorios
def generate_random_events():
    for _ in range(10000):
        start_time = datetime.datetime.now() + datetime.timedelta(days=random.randint(90, 300))  # Cuarto a décimo mes
        end_time = start_time + datetime.timedelta(minutes=random.randint(30, 240))  # Duración aleatoria
        
        event = {
            'summary': 'Evento aleatorio',
            'description': 'Nota aleatoria',
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'America/Mexico_City',  # Reemplaza con tu zona horaria
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'America/Mexico_City',  # Reemplaza con tu zona horaria
            },
            'colorId': str(random.randint(1, len(colors))),  # Color aleatorio
        }
        
        # Seleccionar un calendario aleatorio para agregar el evento
        calendar_id = random.choice(calendar_ids)
        
        # Crear el evento en el calendario seleccionado
        service.events().insert(calendarId=calendar_id, body=event).execute()

# Generar eventos aleatorios
generate_random_events()
