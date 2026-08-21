from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill, NamedStyle
from openpyxl.utils import get_column_letter, column_index_from_string
from datetime import datetime, timedelta
import locale
import pytz
import requests 
from pathlib import Path
from openpyxl.worksheet.table import Table, TableStyleInfo, TableColumn
from collections import defaultdict
from openpyxl.drawing.image import Image
from openpyxl.formatting.rule import CellIsRule
from pprint import pprint
from openpyxl import load_workbook
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
import copy
import re
from ..reportes import helpers

dict_meses = {
        "1": "ene",
        "2": "feb",
        "3": "mar",
        "4": "abr",
        "5": "may",
        "6": "jun",
        "7": "jul",
        "8": "ago",
        "9": "sep",
        "10": "oct",
        "11": "nov",
        "12": "dic",
    }


def normalizar_texto(value):
    return str(value or "").strip().upper()


def agregar_datos_a_celdas(hoja, inicio_celda, datos, primer_color, segundo_color):

    fila_inicio = inicio_celda

    # Definir los colores alternados para las filas
    color_fondo_1 = PatternFill(start_color=primer_color, end_color=primer_color, fill_type="solid")
    color_fondo_2 = PatternFill(start_color=segundo_color, end_color=segundo_color, fill_type="solid")

    ultima_fila = fila_inicio  # Variable para almacenar la última fila usada

    for idx,diccionario in enumerate(datos):
        # Determinar la fila donde se agregará este diccionario
        fila_actual = fila_inicio + idx
        ultima_fila = fila_actual  # Actualizar la última fila usada
        if idx % 2 == 0:
            color_fondo = color_fondo_1  # Verde para filas pares
        else:
            color_fondo = color_fondo_2  # Rojo para filas impares

        for  j, (key, value)in enumerate(diccionario.items()):


            celda = hoja[f"{key}{fila_actual}"]
            celda.value = value
            # Aplicar formato a la celda
            celda.font = Font(name="Arial", size=8, bold=False)
            celda.alignment = Alignment(horizontal="center", vertical="center")
            # Aplicar el color de fondo a la celda
            celda.fill = color_fondo

    return hoja, ultima_fila

def ordenar_data(data, orden_claves):

    data_ordenada = []
    for item in data:
        nuevo_item = {"mes": item["mes"]}  # Mantiene la clave "mes"
        for clave in orden_claves:
            if clave in item:
                nuevo_item[clave] = item[clave]
        data_ordenada.append(nuevo_item)

    return data_ordenada

def obtener_celdas_intermedias(rango):
    inicio, fin = rango.split(":")  # Separar inicio y fin
    m_inicio = re.match(r"^([A-Z]+)(\d+)$", inicio.upper())
    m_fin = re.match(r"^([A-Z]+)(\d+)$", fin.upper())
    if not m_inicio or not m_fin:
        raise ValueError(f"Rango de celdas inválido: {rango}")

    col_inicio, fila_inicio = m_inicio.group(1), int(m_inicio.group(2))
    col_fin, fila_fin = m_fin.group(1), int(m_fin.group(2))
    
    cols = range(column_index_from_string(col_inicio), column_index_from_string(col_fin) + 1)
    return [f"{get_column_letter(c)}" for c in cols]

def asignar_columnas(diccionario, celdas_intermedias,graficos_actuales,total_data):
    fila_resultado = {}  # Diccionario para almacenar los resultados

    # La columna 'A' siempre debe contener el valor de 'mes'
    if 'mes' in diccionario:
        fila_resultado['A'] = diccionario['mes']
    
    columnas_disponibles = celdas_intermedias[1:]  # Excluimos 'A' porque es para 'mes'
    indice_columna = 0  # Índice para recorrer la lista de columnas disponibles

    # Iterar sobre cada categoría en el diccionario
    for categoria, subdiccionario in diccionario.items():
        if categoria == 'mes':  # Saltar 'mes' porque ya fue asignado a 'A'
            continue
        if categoria not in graficos_actuales:
            graficos_actuales[categoria] = {"plan":{}, "acumulado_plan":{}}
        
        # Agregar los valores al gráfico
        graficos_actuales[categoria]["plan"]["columna_inicial"]=indice_columna+2
        graficos_actuales[categoria]["plan"]["inicio_filas"]=5
        graficos_actuales[categoria]["plan"]["termino_filas"]=5 + total_data
        graficos_actuales[categoria]["acumulado_plan"]["columna_inicial"]=indice_columna+2
        graficos_actuales[categoria]["acumulado_plan"]["inicio_filas"]=5
        graficos_actuales[categoria]["acumulado_plan"]["termino_filas"]=5 + total_data

        if isinstance(subdiccionario, dict):  # Verificar si es un diccionario anidado
            for subkey, subvalue in subdiccionario.items():
                if indice_columna < len(columnas_disponibles):  # Asegurar que no excedamos las columnas

                    columna = columnas_disponibles[indice_columna]
                    fila_resultado[columna] = subvalue
                    indice_columna += 1  # Avanzar a la siguiente columna

    return fila_resultado, graficos_actuales

def obtener_maqueta_programas(programas, campanas):
    campana_por_id = {
        str(c.get("id")): (c.get("campana") or "SIN CAMPAÑA")
        for c in campanas
    }

    programas_ordenados = sorted(
        programas,
        key=lambda p: (
            normalizar_texto(campana_por_id.get(str(p.get("campana")), "SIN CAMPAÑA")),
            normalizar_texto(p.get("programa")),
            int(p.get("id") or 0),
        ),
    )

    maqueta_programas = OrderedDict()
    nombres_programas = {}
    etiquetas_programas = OrderedDict()
    mapa_programa_campana = {}
    mapa_programa_solo = defaultdict(list)

    for programa in programas_ordenados:
        programa_id = str(programa.get("id"))
        nombre_programa = normalizar_texto(programa.get("programa")) or "SIN PROGRAMA"
        nombre_campana = campana_por_id.get(str(programa.get("campana")), "SIN CAMPAÑA")
        nombre_campana = str(nombre_campana).strip()

        # Clave única visible en tabla y útil para gráficos
        clave_programa = f"{nombre_programa} ({nombre_campana})"

        if clave_programa not in maqueta_programas:
            maqueta_programas[clave_programa] = {
                "Plan": float(0.00),
                "Real mensual": float(0.00),
                "Acumulado plan": float(0.00),
                "Acumulado real": float(0.00),
            }
            etiquetas_programas[clave_programa] = {
                "programa": nombre_programa,
                "campana": nombre_campana,
            }

        nombres_programas[programa_id] = clave_programa
        mapa_programa_campana[(nombre_programa, normalizar_texto(nombre_campana))] = clave_programa
        mapa_programa_solo[nombre_programa].append(clave_programa)

    return maqueta_programas, nombres_programas, etiquetas_programas, mapa_programa_campana, mapa_programa_solo

def obtener_maqueta_tabla(maqueta_programas, mes_inicio,anio_inicio,mes_termino,anio_termino):
    abreviaciones_es = ["ene", "feb", "mar", "abr", "may", "jun", 
                        "jul", "ago", "sep", "oct", "nov", "dic"]

    fecha_inicio = datetime(anio_inicio, mes_inicio, 1)
    fecha_termino = datetime(anio_termino, mes_termino, 1)

    resultado = []

    while fecha_inicio <= fecha_termino:
        mes_str = abreviaciones_es[fecha_inicio.month - 1]
        anio_str = str(fecha_inicio.year)[-2:]

        current_dict = OrderedDict()
        current_dict["mes"] = f"{mes_str}-{anio_str}"
        for k, v in maqueta_programas.items():
            current_dict[k] = copy.deepcopy(v)  

        resultado.append(current_dict)
        fecha_inicio += relativedelta(months=1)

    return resultado

def agregamos_planificacion_maqueta(fecha_programa,nombre_programa,maqueta,plan):

    if plan == None:
        plan = float(0.00)
    
    for m in maqueta:
        if m['mes'] == fecha_programa:
            m[nombre_programa]["Plan"] = float(plan)
            return maqueta
    return maqueta

def obtener_planificacion_programas(planificacion_programas,nombres_programas,maqueta):
    abreviaciones = ["ene", "feb", "mar", "abr", "may", "jun", 
                        "jul", "ago", "sep", "oct", "nov", "dic"]
    

    for programa in planificacion_programas:

        mes_programa = abreviaciones[int(programa["mes"])-1]
        anio_programa = str(programa["ano"])[-2:]

        fecha_programa = f"{mes_programa}-{anio_programa}"
        nombre_programa = nombres_programas.get(f'{programa["programa"]}')
        if not nombre_programa:
            continue
        
        maqueta = agregamos_planificacion_maqueta(fecha_programa,nombre_programa,maqueta,programa["plan"])

    return maqueta

def obtener_programa_key(sonda_actual, sondajes_recomendaciones, mapa_programa_campana, mapa_programa_solo):
    for pozo, detalles in sondajes_recomendaciones.items():
        for detalle in detalles:
            if detalle['nombre_sonda'] != sonda_actual:
                continue

            recomendacion = detalle.get('recomendacion') or {}
            programa_nombre = normalizar_texto(recomendacion.get('programa'))
            campana_nombre = normalizar_texto(recomendacion.get('campana'))

            key = mapa_programa_campana.get((programa_nombre, campana_nombre))
            if key:
                return key

            # Fallback: si el nombre de programa existe en una sola campaña, usarlo.
            candidatos = mapa_programa_solo.get(programa_nombre, [])
            if len(candidatos) == 1:
                return candidatos[0]

    return None
                
def agregamos_avence_real_maqueta(fecha_programa,nombre_programa,maqueta,real):

    if real == None:
        real = float(0.00)
    
    for m in maqueta:

        if m['mes'] == fecha_programa['mes']:

            m[nombre_programa]["Real mensual"] += float(real)

            return maqueta
    return maqueta

def obtener_avance_real_programas(datos_mensuales,maqueta,sondajes_recomendaciones,mapa_programa_campana,mapa_programa_solo):
    abreviaciones = ["ene", "feb", "mar", "abr", "may", "jun", 
                        "jul", "ago", "sep", "oct", "nov", "dic"]
    

    for fecha, dias in datos_mensuales.items():
        nombre_mes = fecha[:3].lower()    
        ultimos_digitos_anio = fecha[-2:] 
        fecha_actual = {
            "mes": f"{nombre_mes}-{ultimos_digitos_anio}",
        }

        for d in dias:

            for key , value in d.items():

                if "-" in key and "(" not in key:

                    programa = obtener_programa_key(
                        key,
                        sondajes_recomendaciones,
                        mapa_programa_campana,
                        mapa_programa_solo,
                    )

                    if programa:
                        
                        maqueta = agregamos_avence_real_maqueta(fecha_actual,programa,maqueta,value)

    return maqueta

def obtener_acumulados(maqueta):
    acumulados = {}

    for mes in maqueta:

        for key, values in mes.items():
            if key == "mes":
                continue

            if key not in acumulados:
                acumulados[key] = {
                    "Acumulado plan": values["Plan"],
                    "Acumulado real": values["Real mensual"]
                }
            else:
                acumulados[key]["Acumulado plan"] += values["Plan"]
                acumulados[key]["Acumulado real"] += values["Real mensual"]

            # Asignar los acumulados al programa en ese mes
            values["Acumulado plan"] = acumulados[key]["Acumulado plan"]
            values["Acumulado real"] = acumulados[key]["Acumulado real"]

    return maqueta

def construir_data(
    mes_inicio,
    anio_inicio,
    mes_termino,
    anio_termino,
    programas,
    planificacion_programas,
    datos_mensuales,
    sondajes_recomendaciones,
    campanas,
):

    (
        maqueta_programas,
        nombres_programas,
        etiquetas_programas,
        mapa_programa_campana,
        mapa_programa_solo,
    ) = obtener_maqueta_programas(programas, campanas)

    maqueta = obtener_maqueta_tabla(maqueta_programas, mes_inicio,anio_inicio,mes_termino,anio_termino)

    maqueta = obtener_planificacion_programas(planificacion_programas,nombres_programas,maqueta)


    maqueta = obtener_avance_real_programas(
        datos_mensuales,
        maqueta,
        sondajes_recomendaciones,
        mapa_programa_campana,
        mapa_programa_solo,
    )

    maqueta = obtener_acumulados(maqueta)

    return maqueta, nombres_programas, etiquetas_programas


def agregar_encabezado_avance_programa(hoja, etiquetas_programas, fila_campana=2, fila_programa=3, fila_subtitulos=4):
    estilo_encabezado = Font(color="FFFFFF", size=8, bold=True)
    estilo_subtitulo = Font(color="000000", size=8, bold=True)
    centrado = Alignment(horizontal="center", vertical="center", wrap_text=True)
    fondo_encabezado = PatternFill(start_color="f2900e", end_color="f2900e", fill_type="solid")
    fondo_subtitulo = PatternFill(start_color="fcc000", end_color="fcc000", fill_type="solid")
    subtitulos = ["Plan", "Real mensual", "Acumulado plan", "Acumulado real"]

    # Columna A (mes/programa)
    for fila, valor in ((fila_campana, "Campaña"), (fila_programa, "Programa"), (fila_subtitulos, "")):
        celda = hoja[f"A{fila}"]
        celda.value = valor
        celda.font = estilo_encabezado if fila != fila_subtitulos else estilo_subtitulo
        celda.alignment = centrado
        celda.fill = fondo_encabezado if fila != fila_subtitulos else fondo_subtitulo
    hoja.column_dimensions["A"].width = 8

    col_actual = 2  # B
    for clave_programa, meta in etiquetas_programas.items():
        col_inicio = get_column_letter(col_actual)
        col_fin = get_column_letter(col_actual + 3)

        # Fila campaña
        hoja.merge_cells(f"{col_inicio}{fila_campana}:{col_fin}{fila_campana}")
        celda_campana = hoja[f"{col_inicio}{fila_campana}"]
        celda_campana.value = meta["campana"]
        celda_campana.font = estilo_encabezado
        celda_campana.alignment = centrado
        celda_campana.fill = fondo_encabezado

        # Fila programa
        hoja.merge_cells(f"{col_inicio}{fila_programa}:{col_fin}{fila_programa}")
        celda_programa = hoja[f"{col_inicio}{fila_programa}"]
        celda_programa.value = meta["programa"]
        celda_programa.font = estilo_encabezado
        celda_programa.alignment = centrado
        celda_programa.fill = fondo_encabezado

        # Fila subtítulos
        helpers.agregar_subtitulos(
            hoja,
            col_inicio,
            fila_subtitulos,
            subtitulos,
            color_fondo="fcc000",
            alto_fila_factor=2,
            ancho_columna=8,
        )

        col_actual += 4

    inicio_tabla = f"A{fila_programa}"
    termino_tabla = f"{get_column_letter(col_actual - 1)}{fila_programa}"
    return hoja, inicio_tabla, termino_tabla


def run(libro,campanas,programas,planificacion_programas,datos_mensuales,sondajes_recomendaciones):
    
    mes_inicio = 1
    anio_inicio = 2025
    mes_termino = 12
    anio_termino = 2025


    # se busca encontrar el año mas bajo de las campañas para poder obtener los años de inicio y final
    for c in campanas:
        if int(c['anoInicial']) < anio_inicio:
            anio_inicio = int(c['anoInicial'])

        if int(c['anoFinal']) > anio_termino:
            anio_termino = int(c['anoFinal'])


    data, nombres_programas, etiquetas_programas = construir_data(
        mes_inicio,
        anio_inicio,
        mes_termino,
        anio_termino,
        programas,
        planificacion_programas,
        datos_mensuales,
        sondajes_recomendaciones,
        campanas,
    )
    #data = consumir_datos_api()

    # if not data:
    #     print("No hay datos disponibles en REPORTE AVANCE PROGRAMAS.")
    #     data = [
    #     {
    #         "mes": "sep-23",
    #         "GEOLOGÍA": {
    #             "Plan": 10.00,
    #             "Real mensual": 10.00,
    #             "Acumulado plan": 10.00,
    #             "Acumulado real": 10.00
    #         },
    #         "GEOTÉCNICO": {
    #             "Plan": 20.00,
    #             "Real mensual": 20.00,
    #             "Acumulado plan": 20.00,
    #             "Acumulado real": 20.00
    #         },
    #         "HIDROGEOLÓGICO - EVU": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         }
    #     },
    #     {
    #         "mes": "oct-23",
    #         "GEOLOGÍA": {
    #             "Plan": 20.00,
    #             "Real mensual": 20.00,
    #             "Acumulado plan": 20.00,
    #             "Acumulado real": 20.00
    #         },
    #         "GEOTÉCNICO": {
    #             "Plan": 30.00,
    #             "Real mensual": 30.00,
    #             "Acumulado plan": 30.00,
    #             "Acumulado real": 30.00
    #         },
    #         "HIDROGEOLÓGICO - EVU": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         }
    #     },
    #     {
    #         "mes": "nov-23",
    #         "GEOLOGÍA": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         },
    #         "GEOTÉCNICO": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         },
    #         "HIDROGEOLÓGICO - EVU": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         }
    #     },
    #     {
    #         "mes": "dic-23",
    #         "GEOLOGÍA": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         },
    #         "GEOTÉCNICO": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         },
    #         "HIDROGEOLÓGICO - EVU": {
    #             "Plan": 0.00,
    #             "Real mensual": 0.00,
    #             "Acumulado plan": 0.00,
    #             "Acumulado real": 0.00
    #         }
    #     }
    # ]
    
    #     # Obtener todas las claves distintas de "mes" en la data 
    
    # Agregar una nueva hoja 
    hoja = libro.create_sheet(title="AVANCE PROGRAMA")

    hoja = helpers.obtener_fecha_documento(hoja, "A1","A1:F1")


    orden_programas = list(etiquetas_programas.keys())
    hoja, inicio_tabla, termino_tabla = agregar_encabezado_avance_programa(
        hoja,
        etiquetas_programas,
        fila_campana=2,
        fila_programa=3,
        fila_subtitulos=4,
    )
    # Mover la nueva hoja a la primera posición

    data_ordenada = ordenar_data(data, orden_programas)

    celdas_intermedias = obtener_celdas_intermedias(f'{inicio_tabla}:{termino_tabla}')
    

    filas_para_tabla = []
    graficos_actuales = {} 


    total_data = len(data_ordenada) -1 # se le resta 1 para poder calzar el incremento de filas

    for data in data_ordenada:
        fila_resultado,graficos_actuales = asignar_columnas(data, celdas_intermedias,graficos_actuales,total_data)
        filas_para_tabla.append(fila_resultado,)
    
    hoja, ultima_fila= agregar_datos_a_celdas(hoja,5, filas_para_tabla, "ffffff", "ffe598")

    ultima_fila = ultima_fila + 2
    # Iterar por las categorías
    for categoria, valores in graficos_actuales.items():
        titulo_plan = f'{categoria.upper()} PLAN vs REAL'
        titulo_acumulado = f'{categoria.upper()} ACUMULADO'
        # Iterar por cada subdiccionario dentro de la categoría
        for key, value in valores.items():

            if key == "plan":
                celda_inicio_grafico = f"A{ultima_fila}"
                titulo = titulo_plan
                columna_inicial = value["columna_inicial"]
            if key == "acumulado_plan":
                celda_inicio_grafico = f"L{ultima_fila}"
                titulo = titulo_acumulado
                columna_inicial = value["columna_inicial"]+2

            hoja = helpers.generar_tabla_avance_programa(
                hoja,
                titulo = titulo,
                celda_inicio_grafico =celda_inicio_grafico,
                columna_inicial = columna_inicial,
                inicio_filas = value["inicio_filas"],
                termino_filas = value["termino_filas"]
                )

            
        ultima_fila = ultima_fila + 17


    libro._sheets.insert(0, libro._sheets.pop(-1))

    return libro,nombres_programas
