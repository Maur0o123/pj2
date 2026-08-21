import os
import argparse

import requests
import time
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GenerateCsv:
    def __init__(self,type_dashboard):

        load_dotenv()

        self.credentials_file = os.environ["PATH_CREDENTIALS"]
        self.spreadsheet_id = os.environ[f"{type_dashboard.upper()}_SPREADSHEET_ID"]
        self.range_name = f"{type_dashboard.capitalize()}"  # Rango de la hoja
        
        self.api_url = os.environ[f"DASHBOARD_{type_dashboard.upper()}_URL"]

        # Autenticación y creación de servicio
        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)

        # # # Configuración del logger
        # # logging.basicConfig(
        # #     filename='dashboard_vehiculos.log', 
        # #     level=logging.INFO,
        # #     format='%(asctime)s - %(levelname)s - %(message)s'
        # # )

    # Función para borrar un rango de celdas
    def clear_range(self):
        sheet = self.service.spreadsheets()
        request = sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=self.range_name)
        request.execute()

    # Función para escribir datos en un rango
    def write_to_spreadsheet(self, values):
        body = {'values': values}
        sheet = self.service.spreadsheets()
        request = sheet.values().update(
            spreadsheetId=self.spreadsheet_id, range=self.range_name, 
            valueInputOption="RAW", body=body
        )
        response = request.execute()

    def fetch_api_and_write_to_sheet(self, api_url):
        while True:
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()

                    # Headers: agrega los encabezados que deseas escribir en el archivo
                    headers = [
                        'id', 'placaPatente', 'kilometraje', 'fechacreacion', 'cantidad_reportes',
                        'cantidad_origen', 'cantidad_formulario', 'cantidad_mantencion', 'faena',
                        'status_faena', 'tipo', 'marca', 'modelo', 'ano', 'status', 'tenencia', 'completado'
                    ]
                    
                    # Incluir encabezados y luego los datos
                    values = [headers]
                    for item in data:
                        values.append([
                            item.get('id', None), item.get('placaPatente', None), item.get('kilometraje', None),
                            item.get('fechacreacion', None), item.get('cantidad_reportes', None), item.get('cantidad_origen', None),
                            item.get('cantidad_formulario', None), item.get('cantidad_mantencion', None), item.get('faena', None),
                            item.get('status_faena', None), item.get('tipo', None), item.get('marca', None), item.get('modelo', None),
                            item.get('ano', None), item.get('status', None), item.get('tenencia', None), item.get('completado', None)
                        ])
                    
                    # Llamar a la función de escritura con los datos obtenidos
                    self.write_to_spreadsheet(values)
                    break  # Si todo sale bien, salimos del bucle
                else:
                    print(f"Error al obtener datos de la API. Código de respuesta: {response.status_code}")
                    time.sleep(30)  # Espera 30 segundos antes de intentar nuevamente
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                time.sleep(30)  # Espera 30 segundos antes de intentar nuevamente


    # Función run que ejecuta todo
    def run(self):

        print("Iniciando ejecución del script.")
        # Llamar a la función para borrar el rango
        print("Borrando datos del archivo:")
        self.clear_range()
        # Llamar a la función para obtener datos de una API y escribir en el archivo
        print("Obteniendo datos de la API y escribiendo en el archivo:")
        self.fetch_api_and_write_to_sheet(self.api_url)
        print("Proceso terminado satisfactoriamente")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-type",
        "--typeDashboard",
        choices=["vehiculos","sondajes","prevencion","inventario"],
        required=True,
    )
    args = parser.parse_args()

    type_dashboard = args.typeDashboard
    GenerateCsv(
        type_dashboard
    ).run()