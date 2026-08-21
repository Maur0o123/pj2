import os
import re
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GenerateCsvVigilanciaMedica:
    def __init__(self):
        # Cargar variables de entorno desde .env
        load_dotenv()
        self.credentials_file = os.environ.get("PATH_CREDENTIALS", "credentials.json")

        # ID o URL de la hoja de cálculo y URL de la API
        raw_spreadsheet_value = (
            os.environ.get("VIGILANCIA_MEDICA_SPREADSHEET_ID")
            or os.environ.get("VIGILANCIA_MEDICA_SPREADSHEET_URL")
        )
        self.spreadsheet_id = self.extract_spreadsheet_id(raw_spreadsheet_value)
        self.api_url = os.environ.get("DASHBOARD_VIGILANCIA_MEDICA_URL", "http://127.0.0.1:8000/api/dashboard_vigilancia_medica/")
        self.range_name = os.environ.get("VIGILANCIA_MEDICA_RANGE_NAME", "VigilanciaMedica")

        if not self.spreadsheet_id:
            print("ERROR: Falta VIGILANCIA_MEDICA_SPREADSHEET_ID o VIGILANCIA_MEDICA_SPREADSHEET_URL en .env")
            return

        # Autenticación con Google Sheets usando la cuenta de servicio
        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)

    @staticmethod
    def extract_spreadsheet_id(value):
        if not value:
            return None

        value = value.strip()
        match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", value)
        if match:
            return match.group(1)

        return value

    def clear_range(self):
        """Limpia la hoja antes de escribir los nuevos datos para evitar duplicados o datos viejos"""
        sheet = self.service.spreadsheets()
        request = sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=self.range_name)
        request.execute()

    def write_to_spreadsheet(self, values):
        """Escribe los valores en la hoja de cálculo"""
        body = {'values': values}
        sheet = self.service.spreadsheets()
        request = sheet.values().update(
            spreadsheetId=self.spreadsheet_id, range=self.range_name, 
            valueInputOption="RAW", body=body
        )
        request.execute()

    def fetch_api_and_write(self):
        """Obtiene los datos de la API de Django y los procesa para Google Sheets"""
        if not self.spreadsheet_id:
            return
            
        try:
            print(f"Obteniendo datos de {self.api_url}...")
            response = requests.get(self.api_url, timeout=30)
            if response.status_code == 200:
                data = response.json()

                # Definir los encabezados basados en los datos que envía la API
                headers = [
                    'id', 'rut_trabajador', 'nombre_completo', 'faena', 'cargo',
                    'fecha_ingreso', 'antiguedad_anos', 'ges', 
                    'silice_eval_riesgo', 'silice_nivel_riesgo', 'silice_fecha_vence', 'silice_vigencia',
                    'ruido_eval_riesgo', 'ruido_nivel_seguimiento', 'ruido_fecha_vence', 'ruido_vigencia',
                    'hipo_exposicion', 'hipo_fecha_vence', 'hipo_vigencia'
                ]
                
                values = [headers]
                
                if not data:
                    print("La API no devolvió datos. Se escribirá solo el encabezado.")
                else:
                    for item in data:
                        values.append([
                            item.get('id', ''), 
                            item.get('rut_trabajador', ''), 
                            item.get('nombre_completo', ''),
                            item.get('faena', ''), 
                            item.get('cargo', ''), 
                            item.get('fecha_ingreso', ''), 
                            item.get('antiguedad_anos', 0),
                            item.get('ges', ''),
                            item.get('silice_eval_riesgo', ''),
                            item.get('silice_nivel_riesgo', ''),
                            item.get('silice_fecha_vence', ''),
                            item.get('silice_vigencia', ''),
                            item.get('ruido_eval_riesgo', ''),
                            item.get('ruido_nivel_seguimiento', ''),
                            item.get('ruido_fecha_vence', ''),
                            item.get('ruido_vigencia', ''),
                            item.get('hipo_exposicion', ''),
                            item.get('hipo_fecha_vence', ''),
                            item.get('hipo_vigencia', '')
                        ])
                
                self.clear_range()
                print("Escribiendo datos en Google Sheets...")
                self.write_to_spreadsheet(values)
                print("Proceso terminado satisfactoriamente ok.")
            else:
                print(f"Error HTTP {response.status_code} al llamar a la API.")
        except HttpError as e:
            error_text = str(e)
            if "Unable to parse range" in error_text:
                print(
                    f"Error en Google Sheets: la pestaña '{self.range_name}' no existe en el spreadsheet {self.spreadsheet_id}."
                )
            elif "The caller does not have permission" in error_text:
                print(
                    "Error de permisos en Google Sheets: comparte el archivo con el client_email de credentials.json como Editor."
                )
            else:
                print(f"Error de Google Sheets: {error_text}")
        except Exception as e:
            print(f"Error procesando los datos: {e}")

    def run(self):
        print("Iniciando volcado de API de Vigilancia Médica a Google Sheets...")
        self.fetch_api_and_write()

if __name__ == '__main__':
    GenerateCsvVigilanciaMedica().run()
