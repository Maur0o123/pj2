from datetime import datetime
from datetime import timedelta
from pdf2image import convert_from_path
import os
import platform
from .models import FechasImportantes
from django.db.models.functions import Cast
from django.db.models import F, IntegerField
from decimal import Decimal, InvalidOperation
from django.utils import timezone
import pytz


#Helper para sumar el total de horas
def sumar_totales_control_horario(post_data):
    control_horario_count = 0
    for key in post_data.keys():
        if key.startswith('inicio_'):
            control_horario_count += 1
    total_horas = timedelta()
    for i in range(1, control_horario_count + 1):
        total_str = post_data.get(f'total_{i}', '')
        if not total_str: # Lo saltamos por si viene vacio
            continue
        try:
            horas_str, minutos_str = total_str.split(':') 
            horas = int(horas_str)
            minutos = int(minutos_str)
        except ValueError:
            continue # Si viene mal formado, la ignoramos para que no se rompa
        total_horas += timedelta(hours=horas, minutes=minutos)
    return total_horas

#normalziar campos enteros limpiando la entrada para asegurarse de que sea un numero entero
def normalizar_entero(valor):
    if valor is None:
        raise ValueError("Valor requerido")
    valor = str(valor).strip()
    if not valor: #verificamos que no este vacio
        raise ValueError("Valor requerido")
    # Solo dígitos, nada de signos ni puntos ni comas
    if not valor.isdigit(): 
        raise ValueError("Debe ser un numero entero positivo") 
    #preguntar si es que se puede agregar el numero0
    valor_int = int(valor)
    if valor_int == 0:
        raise ValueError("El valor no puede ser 0")
    return int(valor)

#normaliza el formato decimal (coma a punto) y limpia espacios para permitir conversiones seguras a float/Decimal.
def normalizar_decimal(valor):
    if valor is None:
        return None
    #si viene como numero lo pasamos a string.
    if isinstance(valor, (int, float, Decimal)):
        valor_str = str(valor)
    #si viene como string, lo limpiamos
    elif isinstance(valor, str):
        valor_str = valor.strip().replace(",", ".")
        if valor_str == "":
            return None
    else:
        raise TypeError(f"Tipo no soportado: {type(valor)}")
    # Convertir a Decimal
    try:
        decimal = Decimal(valor_str)
    except InvalidOperation:
        raise ValueError(f"Valor decimal inválido: {valor!r}")
    #SIEMPRE devuelve dos decimales exactos
    return decimal.quantize(Decimal("0.01"))

#elimna la fotografia actual y la reemplaza por la fotografia base
def procesar_fotografia(documentacionUsuario, toggle, fotografia_tipo, archivo_base, request):
    if toggle == "si":
            #documentacionUsuario.fotografiaLicenciaInterna = "documentacion_usuario/no-imagen.png"
            setattr(documentacionUsuario, fotografia_tipo, archivo_base)
    else:     
        try:
            #documentacionUsuario.fotografiaLicenciaInterna = request.FILES[fotografia_tipo]
            setattr(documentacionUsuario, fotografia_tipo, request.FILES[fotografia_tipo])
        except:
            #documentacionUsuario.fotografiaLicenciaInterna = documentacionUsuario.fotografiaLicenciaInterna
            setattr(documentacionUsuario, fotografia_tipo, getattr(documentacionUsuario, fotografia_tipo))
            
#elimna la fotografia actual y la reemplaza por la fotografia base si esta vacia le agrega una base
def procesar_fotografia_dos(toggle, fotografia_tipo, archivo_base, request):
    if toggle == "si":
            #documentacionUsuario.fotografiaLicenciaInterna = "documentacion_usuario/no-imagen.png"
            archivo = archivo_base
            return archivo
    else:     
        try:
            #documentacionUsuario.fotografiaLicenciaInterna = request.FILES[fotografia_tipo]
            archivo = request.FILES[fotografia_tipo]
            return archivo
        except:
            #documentacionUsuario.fotografiaLicenciaInterna = documentacionUsuario.fotografiaLicenciaInterna
            archivo = archivo_base
            return archivo

#verifica si el campo esta vacio, sino devuelve el valor original
def validar_campo_vacio(campo_tipo, request):
    if request.POST[campo_tipo] == "":
        return None
    else:
        return request.POST[campo_tipo]
    
#verifica si el campo de tipo archivo esta vacio, sino devuelve el valor original   
def validar_archivo_vacio(campo_tipo, request):
    if request.FILES[campo_tipo] == "":
        return None
    else:
        return request.FILES[campo_tipo]
    
#genera un listado de todos los objetos, si "" muestra solo habilitados, si es distinto muestra todos. (para mostrarlos por select    )
def get_filtered_queryset(model, objeto_actual,orden):
    objetos_con_estado = model.objects.filter(status=True)
    if objeto_actual != "":
        for objeto in objeto_actual:
            if not objeto.status:
                objetos_incluyendo_nuevo = objetos_con_estado | model.objects.filter(pk=objeto.pk)
            else:
                objetos_incluyendo_nuevo = objetos_con_estado
        return objetos_incluyendo_nuevo.order_by(*orden)
    else:
        return objetos_con_estado.order_by(*orden)
    
#formatea la fecha que ingresa por template
def formatear_fecha(fecha):
    if not fecha:
        final =""
        return final
    else:
        original = str(datetime.strftime(fecha, "%Y-%m-%d"))
        formateada = datetime.strptime(original, "%Y-%m-%d")
        final = formateada.strftime('%Y-%m-%d')
        return final
    
#reconoce el tipo de extension que tiene el archivo
def extension_archivo(archivo):
    if archivo.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg")):
        extension = "imagen"
        return extension
    elif archivo.url.lower().endswith((".pdf")):
        extension = "pdf"
        return extension
    else:
        extension = "otro"
        return extension

#convertir PDF a imagenes
def extension_archivo_pdfs(file_path):
    return os.path.splitext(file_path)[1][1:].lower()

def convert_pdf_to_images(pdf_path, poppler_path, quality):
    output_dir = 'media/pdfs_temp_images'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'image_{os.path.basename(pdf_path)}_{i}.jpeg')
        image.save(image_path, 'JPEG', quality=quality)
        image_paths.append(image_path)
    return image_paths

def check_and_convert_pdf(file_path):
    poppler_path = None
    system = platform.system()
    if system == "Windows":
        poppler_path = r'C:\poppler\Library\bin'
    elif system == "Linux":
        poppler_path = '/usr/bin'
    else:
        raise OSError("Sistema operativo no soportado")

    if extension_archivo_pdfs(file_path) == 'pdf':
        return convert_pdf_to_images(file_path, poppler_path,10)
    else:
        return [file_path]
    
def ordenar_por_mes_inicial(mes_inicial):
    mes_inicial = int(mes_inicial)
    return FechasImportantes.objects.annotate(
        mes_as_int=Cast('fechaVencimiento', IntegerField())
    ).annotate(
        mes_ordenado=((F('mes_as_int') - mes_inicial + 12) % 12)
    ).order_by('mes_ordenado')

CL_TZ = pytz.timezone("America/Santiago")
def to_utc(dt):
    if isinstance(dt, str):
        # ISO con Z
        if dt.endswith("Z"):
            return datetime.fromisoformat(dt.replace("Z", "+00:00"))
        dt = datetime.fromisoformat(dt)

    if timezone.is_naive(dt):
        dt = CL_TZ.localize(dt)

    return dt.astimezone(pytz.UTC)
