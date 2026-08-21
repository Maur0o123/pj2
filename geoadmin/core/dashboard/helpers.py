
from django.http import JsonResponse

def data_dashboard_inventario_operaciones():
    data = [
        {
        "faena": "Sierra Gorda",
        "seccion": "Operaciones",
        "familia": "Bolsas",
        "item": "Bolsa 123",
        "cantidad": 100,
        "inventario_minimo": 50,
        "inventario_maximo": 200,
        "fecha": "2025-03-03",
        "marca": "ccc",
        "duracion": 2,
        "valor_neto": 1200
        },
        {
        "faena": "Escondida",
        "seccion": "Operaciones",
        "familia": "Cajas",
        "item": "Caja 123",
        "cantidad": 75,
        "inventario_minimo": 30,
        "inventario_maximo": 150,
        "fecha": "2025-03-03",
        "marca": "aaa",
        "duracion": 3,
        "valor_neto": 1400
        },
        {
        "faena": "Antucoya",
        "seccion": "Operaciones",
        "familia": "Alambres",
        "item": "Alambre 123",
        "cantidad": 50,
        "inventario_minimo": 20,
        "inventario_maximo": 100,
        "fecha": "2025-03-03",
        "marca": "bbb",
        "duracion": 4,
        "valor_neto": 1500
        },
        {
        "faena": "Sierra Gorda",
        "seccion": "Operaciones",
        "familia": "Bolsas",
        "item": "Bolsa 456",
        "cantidad": 100,
        "inventario_minimo": 50,
        "inventario_maximo": 200,
        "fecha": "2025-04-03",
        "marca": "ccc",
        "duracion": 2,
        "valor_neto": 1200
        },
        {
        "faena": "Escondida",
        "seccion": "Operaciones",
        "familia": "Cajas",
        "item": "Caja 456",
        "cantidad": 75,
        "inventario_minimo": 30,
        "inventario_maximo": 150,
        "fecha": "2025-04-03",
        "marca": "aaa",
        "duracion": 3,
        "valor_neto": 1400
        },
        {
        "faena": "Antucoya",
        "seccion": "Operaciones",
        "familia": "Alambres",
        "item": "Alambre 456",
        "cantidad": 50,
        "inventario_minimo": 20,
        "inventario_maximo": 100,
        "fecha": "2025-04-03",
        "marca": "bbb",
        "duracion": 4,
        "valor_neto": 1500
        },
    ]

    return {"status": 200, "data": data}

def data_dashboard_inventario_vehiculos():
    data = [
        {
        "faena": "Sierra Gorda",
        "seccion": "Vehículos",
        "familia": "Basureros",
        "item": "Basurero 123",
        "cantidad": 20,
        "inventario_minimo": 10,
        "inventario_maximo": 50,
        "fecha": "2025-03-03",
        "marca": "A",
        "duracion": 2,
        "valor_neto": 1200
        },
        {
        "faena": "Escondida",
        "seccion": "Vehículos",
        "familia": "Pizarras",
        "item": "Pizarra 123",
        "cantidad": 15,
        "inventario_minimo": 5,
        "inventario_maximo": 30,
        "fecha": "2025-03-03",
        "marca": "A",
        "duracion": 2,
        "valor_neto": 1200
        },
        {
        "faena": "Antucoya",
        "seccion": "Vehículos",
        "familia": "Barras",
        "item": "Barra Cooper",
        "cantidad": 10,
        "inventario_minimo": 3,
        "inventario_maximo": 20,
        "fecha": "2025-03-03",
        "marca": "A",
        "duracion": 2,
        "valor_neto": 1200
        }
    ]

    return  {"status": 200, "data": data}

def data_dashboard_inventario_prevencion():
    data = [
        { 
        "faena": "Sierra Gorda",
        "seccion": "Prevención",
        "familia": "Cascos",
        "item": "Casco 123",
        "cantidad": 30,
        "inventario_minimo": 10,
        "inventario_maximo": 50,
        "fecha": "2025-03-03",
        "marca": "A",
        "duracion": 2,
        "valor_neto": 1200
        },
        { 
        "faena": "Escondida",
        "seccion": "Prevención",
        "familia": "Máscaras",
        "item": "Máscara 123",
        "cantidad": 25,
        "inventario_minimo": 10,
        "inventario_maximo": 40,
        "fecha": "2025-03-03",
        "marca": "A",
        "duracion": 2,
        "valor_neto": 1200
        },
        { 
        "faena": "Antucoya",
        "seccion": "Prevención",
        "familia": "Camisas",
        "item": "Camisa 123",
        "cantidad": 40,
        "inventario_minimo": 15,
        "inventario_maximo": 60,
        "fecha": "2025-03-03",
        "marca": "A",
        "duracion": 2,
        "valor_neto": 1200
        }
    ]

    return  {"status": 200, "data": data}

def data_dashboard_sondas_diario():
    data = [
        { 
        "faena": "Sierra Gorda",
        "campaña": "campaña 1",
        "programa": "programa 1",
        "recomendación": "recomendacion 1",
        "sonda": "sonda 1",
        "sondaje": "sondaje 1",
        "turno": "dia",
        "fecha": "2025-03-03",
        "desde": 0,
        "hasta": 100,
        "perforado": 100,
        "observacion": "sin observacion",
        },
        { 
        "faena": "Escondida",
        "campaña": "campaña 2",
        "programa": "programa 2",
        "recomendación": "recomendacion 2",
        "sonda": "sonda 2",
        "sondaje": "sondaje 2",
        "turno": "noche",
        "fecha": "2025-03-03",
        "desde": 0,
        "hasta": 200,
        "perforado": 1200,
        "observacion": "sin observacion",
        }
    ]

    return  {"status": 200, "data": data}
def data_dashboard_sondas_total():
    data = [
        { 
        "faena": "Sierra Gorda",
        "campaña": "campaña 1",
        "programa": "programa 1",
        "año": 2025,
        "mes programa": "marzo",
        "total mes programa": 100,
        "perforacion avance (m)": 10,
        "por perforar": 90,
        "% avance": 10,
        },
        { 
        "faena": "Escondida",
        "campaña": "campaña 2",
        "programa": "programa 2",
        "año": 2025,
        "mes programa": "marzo",
        "total mes programa": 100,
        "perforacion avance (m)": 10,
        "por perforar": 90,
        "% avance": 10,
        }
    ]

    return  {"status": 200, "data": data}