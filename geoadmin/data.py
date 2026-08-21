import requests
import json

#url = "https://sicgeoadmin.cl/api/save_reporte_operacional/"
url = "http://127.0.0.1:8000/api/save_reporte_operacional/"
#url = "http://127.0.0.1:8000/api/save_reporte_materiales_sonda/"
#url = "https://2641-2800-150-13b-1123-eda5-31a2-66e6-f952.ngrok-free.app/api/save_reporte_operacional/"


# Función para refrescar el token
def refresh_token():
    refresh_url = "http://127.0.0.1:8000/api/token/refresh/"
    refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjUxNTE2MSwiaWF0IjoxNzM1NjUxMTYxLCJqdGkiOiIwM2JkNTMxNjM5MDA0YjBmOGU0OTk0ZmZkMTMxODI4ZiIsInVzZXJfaWQiOjJ9.iDXv2AML2GhuM1jha3Tt6VQ5-iDLvpI8gjwlsS7trVM"

    response = requests.post(refresh_url, data={"refresh": refresh_token})
    if response.status_code == 200:
        new_access_token = response.json().get("access")
        return new_access_token
    else:
        print("Error al refrescar el token:", response.json())
        return None

def post_data():
    # Cargar el token de acceso inicial
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1NjUxNDYxLCJpYXQiOjE3MzU2NTExNjEsImp0aSI6IjVlZGEzYjNiYjE0MzRiZWQ5Y2RlMWQ4NmM5MDU3YTk3IiwidXNlcl9pZCI6Mn0.ZXLPOSvjOHqxmvap3dFrEmeyQuo-0reWHXgYWaiIABU"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data =  [
    {
        "origen": "movil",
        "tipo": "reporte",
        "id": 257,
        "turno": "1",
        "fechacreacion": "2024-12-31T10:01:28.843",
        "fechaedicion": "2024-12-31T10:01:28.843",
        "sondajeSerie": "4555",
        "sondajeEstado": "",
        "metroInicial": "3.00",
        "metroFinal": "6.00",
        "totalPerforado": "3.00",
        "progreso": "Por Revisar",
        "correlativo": 1,
        "status": True,
        "controlador": "Claudio Conelli",
        "perforista": 2,
        "sonda": 2,
        "sondajeCodigo": 2,
        "id_checklist": "7627064083340"
    },
    {
        "origen": "movil",
        "tipo": "reporte",
        "id": 258,
        "turno": "1",
        "fechacreacion": "2024-12-31T10:01:49.392",
        "fechaedicion": "2024-12-31T10:01:49.392",
        "sondajeSerie": "4555",
        "sondajeEstado": "",
        "metroInicial": "3.00",
        "metroFinal": "6.00",
        "totalPerforado": "3.00",
        "progreso": "Por Revisar",
        "correlativo": 1,
        "status": True,
        "controlador": "Claudio Conelli",
        "perforista": 2,
        "sonda": 2,
        "sondajeCodigo": 2,
        "id_checklist": "7627064083340"
    },
    {
        "origen": "movil",
        "tipo": "reporte",
        "id": 259,
        "turno": "1",
        "fechacreacion": "2024-12-31T10:06:15.295",
        "fechaedicion": "2024-12-31T10:06:15.295",
        "sondajeSerie": "4555",
        "sondajeEstado": "",
        "metroInicial": "3.00",
        "metroFinal": "8.00",
        "totalPerforado": "5.00",
        "progreso": "Por Revisar",
        "correlativo": 1,
        "status": True,
        "controlador": "Claudio Conelli",
        "perforista": 2,
        "sonda": 2,
        "sondajeCodigo": 2,
        "id_checklist": "2036492121569"
    },
    {
        "origen": "movil",
        "tipo": "reporte",
        "id": 260,
        "turno": "1",
        "fechacreacion": "2024-12-31T10:06:20.040",
        "fechaedicion": "2024-12-31T10:06:20.040",
        "sondajeSerie": "4555",
        "sondajeEstado": "",
        "metroInicial": "3.00",
        "metroFinal": "8.00",
        "totalPerforado": "5.00",
        "progreso": "Por Revisar",
        "correlativo": 1,
        "status": True,
        "controlador": "Claudio Conelli",
        "perforista": 2,
        "sonda": 2,
        "sondajeCodigo": 2,
        "id_checklist": "2036492121569"
    },
    {
        "origen": "movil",
        "tipo": "reporte",
        "id": 261,
        "turno": "1",
        "fechacreacion": "2024-12-31T10:09:46.912",
        "fechaedicion": "2024-12-31T10:09:46.912",
        "sondajeSerie": "4555",
        "sondajeEstado": "",
        "metroInicial": "3.00",
        "metroFinal": "6.00",
        "totalPerforado": "3.00",
        "progreso": "Creado",
        "correlativo": 1,
        "status": True,
        "controlador": "Claudio Conelli",
        "perforista": 2,
        "sonda": 2,
        "sondajeCodigo": 2,
        "id_checklist": "4255798041484"
    },
    {
        "origen": "movil",
        "tipo": "reporte",
        "id": 262,
        "turno": "1",
        "fechacreacion": "2024-12-31T10:09:48.177",
        "fechaedicion": "2024-12-31T10:09:48.177",
        "sondajeSerie": "4555",
        "sondajeEstado": "",
        "metroInicial": "3.00",
        "metroFinal": "6.00",
        "totalPerforado": "3.00",
        "progreso": "Creado",
        "correlativo": 1,
        "status": True,
        "controlador": "Claudio Conelli",
        "perforista": 2,
        "sonda": 2,
        "sondajeCodigo": 2,
        "id_checklist": "4255798041484"
    },
    {
        "origen": "movil",
        "tipo": "perforacion",
        "id": 1,
        "perforacion": "3",
        "desde": "3.00",
        "hasta": "6.00",
        "recuperado": "3",
        "porcentaje": "100.00%",
        "barra": "1",
        "largoBarra": "3",
        "totalHta": "4.80",
        "contra": "1.80",
        "fechacreacion": "2024-12-31T13:00:30.465Z",
        "status": True,
        "reporte": 257,
        "selectedDiametro": 2,
        "selectedTipo_Terreno": 2,
        "selectedOrientacion": 2
    },
    {
        "origen": "movil",
        "tipo": "perforacion",
        "id": 1,
        "perforacion": "3",
        "desde": "3.00",
        "hasta": "6.00",
        "recuperado": "3",
        "porcentaje": "100.00%",
        "barra": "1",
        "largoBarra": "3",
        "totalHta": "4.80",
        "contra": "1.80",
        "fechacreacion": "2024-12-31T13:00:30.465Z",
        "status": True,
        "reporte": 258,
        "selectedDiametro": 2,
        "selectedTipo_Terreno": 2,
        "selectedOrientacion": 2
    },
    {
        "origen": "movil",
        "tipo": "perforacion",
        "id": 1,
        "perforacion": "5",
        "desde": "3.00",
        "hasta": "8.00",
        "recuperado": "5",
        "porcentaje": "100.00%",
        "barra": "2",
        "largoBarra": "6",
        "totalHta": "13.80",
        "contra": "10.80",
        "fechacreacion": "2024-12-31T13:05:19.003Z",
        "status": True,
        "reporte": 259,
        "selectedDiametro": 2,
        "selectedTipo_Terreno": 2,
        "selectedOrientacion": 1
    },
    {
        "origen": "movil",
        "tipo": "perforacion",
        "id": 1,
        "perforacion": "5",
        "desde": "3.00",
        "hasta": "8.00",
        "recuperado": "5",
        "porcentaje": "100.00%",
        "barra": "2",
        "largoBarra": "6",
        "totalHta": "13.80",
        "contra": "10.80",
        "fechacreacion": "2024-12-31T13:05:19.003Z",
        "status": True,
        "reporte": 260,
        "selectedDiametro": 2,
        "selectedTipo_Terreno": 2,
        "selectedOrientacion": 1
    },
    {
        "origen": "movil",
        "tipo": "perforacion",
        "id": 1,
        "perforacion": "3",
        "desde": "3.00",
        "hasta": "6.00",
        "recuperado": "3",
        "porcentaje": "100.00%",
        "barra": "1",
        "largoBarra": "3",
        "totalHta": "4.80",
        "contra": "1.80",
        "fechacreacion": "2024-12-31T13:08:54.745Z",
        "status": True,
        "reporte": 261,
        "selectedDiametro": 3,
        "selectedTipo_Terreno": 2,
        "selectedOrientacion": 1
    },
    {
        "origen": "movil",
        "tipo": "perforacion",
        "id": 1,
        "perforacion": "3",
        "desde": "3.00",
        "hasta": "6.00",
        "recuperado": "3",
        "porcentaje": "100.00%",
        "barra": "1",
        "largoBarra": "3",
        "totalHta": "4.80",
        "contra": "1.80",
        "fechacreacion": "2024-12-31T13:08:54.745Z",
        "status": True,
        "reporte": 262,
        "selectedDiametro": 3,
        "selectedTipo_Terreno": 2,
        "selectedOrientacion": 1
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "13:00",
        "horaFinal": "01:00",
        "totalHoras": "12:00",
        "detalle": 7,
        "editableInicio": True,
        "reporte": 259
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "01:00",
        "horaFinal": None,
        "totalHoras": "",
        "detalle": "",
        "editableInicio": False,
        "reporte": 259
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "13:00",
        "horaFinal": "01:00",
        "totalHoras": "12:00",
        "detalle": 7,
        "editableInicio": True,
        "reporte": 260
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "01:00",
        "horaFinal": None,
        "totalHoras": "",
        "detalle": "",
        "editableInicio": False,
        "reporte": 260
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "13:15",
        "horaFinal": "01:15",
        "totalHoras": "12:00",
        "detalle": 7,
        "editableInicio": True,
        "reporte": 261
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "01:15",
        "horaFinal": None,
        "totalHoras": "",
        "detalle": "",
        "editableInicio": False,
        "reporte": 261
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "13:15",
        "horaFinal": "01:15",
        "totalHoras": "12:00",
        "detalle": 7,
        "editableInicio": True,
        "reporte": 262
    },
    {
        "origen": "movil",
        "tipo": "controlHorario",
        "horaInicio": "01:15",
        "horaFinal": None,
        "totalHoras": "",
        "detalle": "",
        "editableInicio": False,
        "reporte": 262
    },
    {
        "origen": "movil",
        "tipo": "insumos",
        "id": 54,
        "corona": "P",
        "escareador": "P",
        "casing": "3.3",
        "zapata": "P",
        "status": True,
        "reporte": 257,
        "cantidadAgua": ""
    },
    {
        "origen": "movil",
        "tipo": "insumos",
        "id": 55,
        "corona": "P",
        "escareador": "P",
        "casing": "3.3",
        "zapata": "P",
        "status": True,
        "reporte": 258,
        "cantidadAgua": ""
    },
    {
        "origen": "movil",
        "tipo": "insumos",
        "id": 56,
        "corona": "P",
        "escareador": "P",
        "casing": "3.3",
        "zapata": "P",
        "status": True,
        "reporte": 259,
        "cantidadAgua": ""
    },
    {
        "origen": "movil",
        "tipo": "insumos",
        "id": 57,
        "corona": "P",
        "escareador": "P",
        "casing": "3.3",
        "zapata": "P",
        "status": True,
        "reporte": 260,
        "cantidadAgua": ""
    },
    {
        "origen": "movil",
        "tipo": "insumos",
        "id": 58,
        "corona": "P",
        "escareador": "P",
        "casing": "3.3",
        "zapata": "P",
        "status": True,
        "reporte": 261,
        "cantidadAgua": ""
    },
    {
        "origen": "movil",
        "tipo": "insumos",
        "id": 59,
        "corona": "P",
        "escareador": "P",
        "casing": "3.3",
        "zapata": "P",
        "status": True,
        "reporte": 262,
        "cantidadAgua": ""
    },
    {
        "origen": "movil",
        "tipo": "longitud",
        "id": 48,
        "largoBarril": "4.15",
        "largoBarra": "1",
        "puntoMuerto": "2.35",
        "restoBarra": "1.80",
        "longitudPozo": "3.00",
        "numeroBarra": "1",
        "htaEnPozo": "No",
        "mtsDeHta": "0.00",
        "profundidadHta": "0.00",
        "status": True,
        "reporte": 257
    },
    {
        "origen": "movil",
        "tipo": "longitud",
        "id": 49,
        "largoBarril": "4.15",
        "largoBarra": "1",
        "puntoMuerto": "2.35",
        "restoBarra": "1.80",
        "longitudPozo": "3.00",
        "numeroBarra": "1",
        "htaEnPozo": "No",
        "mtsDeHta": "0.00",
        "profundidadHta": "0.00",
        "status": True,
        "reporte": 258
    },
    {
        "origen": "movil",
        "tipo": "longitud",
        "id": 50,
        "largoBarril": "4.15",
        "largoBarra": "2",
        "puntoMuerto": "2.35",
        "restoBarra": "10.80",
        "longitudPozo": "5.00",
        "numeroBarra": "2",
        "htaEnPozo": "No",
        "mtsDeHta": "0.00",
        "profundidadHta": "0.00",
        "status": True,
        "reporte": 259
    },
    {
        "origen": "movil",
        "tipo": "longitud",
        "id": 51,
        "largoBarril": "4.15",
        "largoBarra": "2",
        "puntoMuerto": "2.35",
        "restoBarra": "10.80",
        "longitudPozo": "5.00",
        "numeroBarra": "2",
        "htaEnPozo": "No",
        "mtsDeHta": "0.00",
        "profundidadHta": "0.00",
        "status": True,
        "reporte": 260
    },
    {
        "origen": "movil",
        "tipo": "longitud",
        "id": 52,
        "largoBarril": "4.15",
        "largoBarra": "1",
        "puntoMuerto": "2.35",
        "restoBarra": "1.80",
        "longitudPozo": "3.00",
        "numeroBarra": "1",
        "htaEnPozo": "No",
        "mtsDeHta": "0.00",
        "profundidadHta": "0.00",
        "status": True,
        "reporte": 261
    },
    {
        "origen": "movil",
        "tipo": "longitud",
        "id": 53,
        "largoBarril": "4.15",
        "largoBarra": "1",
        "puntoMuerto": "2.35",
        "restoBarra": "1.80",
        "longitudPozo": "3.00",
        "numeroBarra": "1",
        "htaEnPozo": "No",
        "mtsDeHta": "0.00",
        "profundidadHta": "0.00",
        "status": True,
        "reporte": 262
    },
    {
        "origen": "movil",
        "id": 48,
        "observaciones": "",
        "observaciones": "",
        "status": True,
        "reporte": 257
    },
    {
        "origen": "movil",
        "tipo": "observacion",
        "id": 49,
        "observaciones": "",
        "status": True,
        "reporte": 258
    },
    {
        "origen": "movil",
        "tipo": "observacion",
        "id": 50,
        "observaciones": "010101",
        "status": True,
        "reporte": 259
    },
    {
        "origen": "movil",
        "tipo": "observacion",
        "id": 51,
        "observaciones": "010101",
        "status": True,
        "reporte": 260
    },
    {
        "origen": "movil",
        "tipo": "observacion",
        "id": 52,
        "observaciones": "",
        "status": True,
        "reporte": 261
    },
    {
        "origen": "movil",
        "tipo": "observacion",
        "id": 53,
        "observaciones": "",
        "status": True,
        "reporte": 262
    }
    ]
    

    response = requests.post(url, json=data, headers=headers)
    
    # Si la solicitud falla con un error de autenticación, intenta refrescar el token
    if response.status_code == 401:
        print("Token expirado. Intentando refrescar el token...")
        new_access_token = refresh_token()
        if new_access_token:
            # Actualiza el encabezado con el nuevo token de acceso
            headers["Authorization"] = f"Bearer {new_access_token}"
            response = requests.post(url, json=data, headers=headers)
        else:
            print("No se pudo refrescar el token.")
            return

    # Verifica si la solicitud tuvo éxito
    if response.status_code == 200:
        print("Datos enviados exitosamente.")
        print("Response JSON:", response.json())
    else:
        print("Error al enviar los datos:", response.status_code)
        print("Response JSON:", response.json())

post_data()