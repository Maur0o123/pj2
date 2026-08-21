import os
import requests
import time
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GenerateCsvPrevencionReportes:
    def __init__(self):
        load_dotenv()
        self.credentials_file = os.environ.get("PATH_CREDENTIALS", "credentials.json")
        
        # We need these two defined in .env
        self.spreadsheet_id = os.environ.get("PREVENCION_REPORTES_SPREADSHEET_ID")
        self.api_url = os.environ.get("DASHBOARD_PREVENCION_REPORTES_URL", "http://127.0.0.1:8000/api/dashboard_prevencion_reportes/")
        
        self.range_name = "Reportes" # Name of the target sheet tab

        if not self.spreadsheet_id:
            print("ERROR: Faltan PREVENCION_REPORTES_SPREADSHEET_ID en .env")
            return

        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)

    def clear_range(self):
        sheet = self.service.spreadsheets()
        request = sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=self.range_name)
        request.execute()

    def write_to_spreadsheet(self, values):
        body = {'values': values}
        sheet = self.service.spreadsheets()
        request = sheet.values().update(
            spreadsheetId=self.spreadsheet_id, range=self.range_name, 
            valueInputOption="RAW", body=body
        )
        request.execute()

    def fetch_api_and_write(self):
        if not self.spreadsheet_id:
            return
            
        try:
            print(f"Obteniendo datos de {self.api_url}...")
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()

                headers = [
                    'id', 'tipo', 'faena', 'porcentaje', 'plantilla_base', 'creador', 'fecha'
                ]
                
                values = [headers]
                
                if not data:
                    values.append([
                        "Sin Datos", "Sin Tipo", "Sin Faena", 0, "Sin Plantilla", "Sin Creador", "Sin Fecha"
                    ])
                else:
                    for item in data:
                        values.append([
                            item.get('id', ''), 
                            item.get('tipo', ''), 
                            item.get('faena', ''),
                            item.get('porcentaje', 0), 
                            item.get('plantilla_base', ''), 
                            item.get('creador', ''), 
                            item.get('fecha', '')
                        ])
                
                self.clear_range()
                print("Escribiendo datos en Google Sheets...")
                self.write_to_spreadsheet(values)
                print("Proceso terminado satisfactoriamente ok.")
            else:
                print(f"Error HTTP {response.status_code} al llamar a la API.")
        except Exception as e:
            print(f"Error procesando los datos: {e}")

    def run(self):
        print("Iniciando volcado de API de Reportes de Prevención a Google Sheets...")
        self.fetch_api_and_write()

if __name__ == '__main__':
    GenerateCsvPrevencionReportes().run()
