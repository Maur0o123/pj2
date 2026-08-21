import os
import argparse

import requests
import time
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GenerateCsv:
    def __init__(self):

        load_dotenv()

        #self.options_process = ["vehiculos","sondajes","prevencion","inventario"]
        self.options_process = ["vehiculos","inventario_sondajes","inventario_prevencion","inventario_vehiculos","sondas"]
        self.credentials_file = os.environ["PATH_CREDENTIALS"]
        # Autenticación y creación de servicio
        self.credentials = service_account.Credentials.from_service_account_file(
        self.credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        self.service = build('sheets', 'v4', credentials=self.credentials)
        # self.credentials_file = os.environ["PATH_CREDENTIALS"]
        # self.spreadsheet_id = os.environ[f"{type_dashboard.upper()}_SPREADSHEET_ID"]
        # self.range_name = f"{type_dashboard.capitalize()}"  # Rango de la hoja
        
        # self.api_url = os.environ[f"DASHBOARD_{type_dashboard.upper()}_URL"]

        # Autenticación y creación de servicio
        # self.credentials = service_account.Credentials.from_service_account_file(
        #     self.credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        # )
        # self.service = build('sheets', 'v4', credentials=self.credentials)


    # Función para borrar un rango de celdas
    def clear_range(self,spreadsheet_id,range_name):
        sheet = self.service.spreadsheets()
        request = sheet.values().clear(spreadsheetId=spreadsheet_id, range=range_name)
        request.execute()

    # Función para escribir datos en un rango
    def write_to_spreadsheet(self, values,spreadsheet_id,range_name):
        body = {'values': values}
        sheet = self.service.spreadsheets()
        request = sheet.values().update(
            spreadsheetId=spreadsheet_id, range=range_name, 
            valueInputOption="RAW", body=body
        )
        response = request.execute()

    def fetch_api_and_write_to_sheet_vehiculos(self, api_url,spreadsheet_id,range_name):
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
                    self.write_to_spreadsheet(values,spreadsheet_id,range_name)
                    break  # Si todo sale bien, salimos del bucle
                else:
                    print(f"Error al obtener datos de la API. Código de respuesta: {response.status_code}")
                    time.sleep(30)  # Espera 30 segundos antes de intentar nuevamente
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                time.sleep(30)  # Espera 30 segundos antes de intentar nuevamente

    def fetch_api_and_write_to_sheet_inventory(self, api_url,spreadsheet_id,range_name):
            while True:
                try:
                    response = requests.get(api_url)

                    # Simulación de una respuesta HTTP con código de estado 200
                    #response = api_url  # Llamamos a la función para obtener los datos directamente
                    
                    if response.status_code == 200: 
                        data = response.json()
                        print("Datos obtenidos correctamente")
                        # Headers: agrega los encabezados que deseas escribir en el archivo
                        headers = [
                            'faena',
                            'seccion', 
                            'categoria', 
                            'item', 
                            'cantidad', 
                            'inventario_minimo', 
                            'inventario_maximo', 
                            'fecha', 
                            'marca', 
                            'duracion', 
                            'valor_neto',
                            'total',
                            'status'
                        ]
                                
                        # Incluir encabezados y luego los datos
                        values = [headers]

                        if not data:
                            values.append([
                                "Sin Faena", "Sin Seccion", "Sin Categoria",
                                "Sin Item", 0, 0, 0,"2011-11-11", "Sin Marca", 0, 0,0,True
                            ])
                        else:
                            for item in data:
                                #print(item)
                                total = int(item.get('cantidad', 0)) * int(item.get('valor_neto', 0))
                                values.append([
                                    item.get('faena', None), item.get('seccion', None), item.get('categoria', None),
                                    item.get('item', None),  item.get('cantidad', None), item.get('stock_minimo', None), item.get('stock_maximo', None),
                                    item.get('fechacreacion', None), item.get('marca', None), item.get('duracion', None), item.get('valor_neto', None),
                                    total,item.get('status', None)
                                ])
                        
                        # Llamar a la función de escritura con los datos obtenidos
                        self.write_to_spreadsheet(values,spreadsheet_id,range_name)
                        break  # Si todo sale bien, salimos del bucle
                    else:
                        print(f"Error al obtener datos de la API. Código de respuesta: {response.status_code}")
                        time.sleep(30)  # Espera 30 segundos antes de intentar nuevamente
                except Exception as e:
                    print(f"Ocurrió un error: {e}")
                    time.sleep(30)  # Espera 30 segundos antes de intentar nuevamente

    def fetch_api_and_write_to_sheet_sondas_diario(self, api_url, spreadsheet_id, range_name):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json().get("data", [])
                headers = ['faena', 'campaña', 'programa', 'recomendación', 'sonda',
                           'sondaje', 'turno', 'fecha', 'desde', 'hasta', 'perforado', 'observacion']
                values = [headers]
                for item in data:
                    values.append([
                        item.get('faena'), item.get('campaña'), item.get('programa'),
                        item.get('recomendación'), item.get('sonda'), item.get('sondaje'),
                        item.get('turno'), item.get('fecha'), item.get('desde'),
                        item.get('hasta'), item.get('perforado'), item.get('observacion')
                    ])
                self.write_to_spreadsheet(values, spreadsheet_id, range_name)
                print("Sondas Diario OK.")
        except Exception as e:
            print(f"Error Sondas Diario: {e}")

    def fetch_api_and_write_to_sheet_sondas_total(self, api_url, spreadsheet_id, range_name):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json().get("data", [])
                headers = ['faena', 'campaña', 'programa', 'año', 'mes programa',
                           'total mes programa', 'perforacion avance (m)', 'por perforar', '% avance']
                values = [headers]
                for item in data:
                    values.append([
                        item.get('faena'), item.get('campaña'), item.get('programa'),
                        item.get('año'), item.get('mes programa'), item.get('total mes programa'),
                        item.get('perforacion avance (m)'), item.get('por perforar'), item.get('% avance')
                    ])
                self.write_to_spreadsheet(values, spreadsheet_id, range_name)
                print("Sondas General OK.")
        except Exception as e:
            print(f"Error Sondas Total: {e}")

    def actualizar_solo_sondajes(self):
        """
        Ejecuta EXCLUSIVAMENTE la actualización de reportes de Sondaje (Diario y General).
        Ideal para threading desde views.py.
        """
        print("\n>>> INICIANDO ACTUALIZACIÓN TRIGGER: SONDAJES <<<")

        # 1. Sondaje Diario
        if "SONDA_DIARIO_ID" in os.environ and "DASHBOARD_SONDAS_DIARIO_URL" in os.environ:
            try:
                print("Actualizando Hoja Diario...")
                id_diario = os.environ["SONDA_DIARIO_ID"]
                url_diario = os.environ["DASHBOARD_SONDAS_DIARIO_URL"]
                hoja_diario = "diario"
                
                self.clear_range(id_diario, hoja_diario)
                self.fetch_api_and_write_to_sheet_sondas_diario(url_diario, id_diario, hoja_diario)
            except Exception as e:
                print(f"Error crítico en Diario: {e}")
        else:
            print("ALERTA: Faltan variables SONDA_DIARIO en .env")

        # 2. Sondaje Total (General)
        if "SONDA_GENERAL_ID" in os.environ and "DASHBOARD_SONDAS_TOTAL_URL" in os.environ:
            try:
                print("Actualizando Hoja General...")
                id_total = os.environ["SONDA_GENERAL_ID"]
                url_total = os.environ["DASHBOARD_SONDAS_TOTAL_URL"]
                hoja_total = "general"

                self.clear_range(id_total, hoja_total)
                self.fetch_api_and_write_to_sheet_sondas_total(url_total, id_total, hoja_total)
            except Exception as e:
                print(f"Error crítico en General: {e}")
        else:
            print("ALERTA: Faltan variables SONDA_GENERAL en .env")
            
        print(">>> FIN ACTUALIZACIÓN SONDAJES <<<\n")
    def run(self):
        """
        Ejecuta Vehículos e Inventarios. IGNORA Sondajes explícitamente.
        """
        print("\n=== INICIANDO BARRIDO GENERAL (Sin Sondajes) ===\n")

        for type_dashboard in self.options_process:
            
            # Si es 'sondas', lo saltamos (se maneja en la función de arriba)
            if type_dashboard == "sondas":
                continue 

            print(f"Iniciando actualización: [ {type_dashboard} ]")
            
            # --- Lógica para Vehículos ---
            if type_dashboard == "vehiculos":
                if "VEHICULOS_SPREADSHEET_ID" in os.environ and "DASHBOARD_VEHICULOS_URL" in os.environ:
                    sid = os.environ["VEHICULOS_SPREADSHEET_ID"]
                    url = os.environ["DASHBOARD_VEHICULOS_URL"]
                    rname = "Vehiculos"
                    
                    self.clear_range(sid, rname)
                    self.fetch_api_and_write_to_sheet_vehiculos(url, sid, rname)
                else:
                    print("ERROR: Falta VEHICULOS_SPREADSHEET_ID o URL en .env")

            # --- Lógica para Inventarios ---
            elif type_dashboard.startswith("inventario_"):
                env_suffix = type_dashboard.upper()
                
                id_key = f"{env_suffix}_SPREADSHEET_ID"
                url_key = f"DASHBOARD_{env_suffix}_URL"
                
                if id_key in os.environ and url_key in os.environ:
                    sid = os.environ[id_key]
                    url = os.environ[url_key]
                    rname = type_dashboard.capitalize() # Ej: Inventario_sondajes
                    
                    self.clear_range(sid, rname)
                    self.fetch_api_and_write_to_sheet_inventory(url, sid, rname)
                else:
                    print(f"ERROR: Falta {id_key} o {url_key} en .env")

        print("\n=== PROCESO GENERAL TERMINADO ===\n")

if __name__ == '__main__':
    GenerateCsv().run()