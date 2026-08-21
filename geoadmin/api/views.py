from rest_framework import generics
from core.models import (
    Perforistas, Sondas, Sondajes, Diametros, TipoTerreno, Orientacion,
    CantidadAgua, Aditivos, DetalleControlHorario, MaterialesSonda, MaterialesCaseta, Recomendacion,Campana, Programa, RecomendacionAjuste, RecomendacionFinal
)
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User, Usuario,Faena
from .serializers import (
    UsuariosSerializer,PerforistasSerializer, SondasSerializer, SondajesSerializer, DiametrosSerializer, TipoTerrenoSerializer,
    OrientacionSerializer, CantidadAguaSerializer, AditivosSerializer, DetalleControlHorarioSerializer, 
    ReportesOperacionalesActivosSerializer, DetallesPerforacionesActivosSerializer, ControlesHorariosActivosSerializer, 
    InsumosActivosSerializer, DetalleAditivosActivosSerializer, LongitudPozosActivosSerializer, ObservacionesReportesActivosSerializer, 
    VehiculosSerializer, VehiculosKilometrajesSerializer, VehiculosFaenasSerializer, MaterialesSondaActivosSerializer, MaterialesCasetaActivosSerializer,
    MaterialesSondaSerializer, MaterialesCasetaSerializer, RecomendacionSerializer, CustomTokenObtainPairSerializer, ItemsSerializer,
    CampanaSerializer, ProgramaSerializer, PlanificacionProgramaSerializer,FaenaSerializer
)
from .serializers import DataReporteAvanceCampañaSerializer,RecomendacionSerializerAvanceCampana, RecomendacionAjusteSerializer, RecomendacionFinalSerializer
from core.models import Campana, Programa
from planning.models import PlanificacionPrograma, PlanificacionCampanas

from core.choices import turno, gemelo, jornada
from core.utils import to_utc
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from drilling.models import ReportesOperacionales, DetallesPerforaciones, ControlesHorarios, Insumos, DetalleAditivos, LongitudPozos, ObservacionesReportes
from django.utils import timezone
from django.db.models import Q, Max, Count
from django.core.exceptions import ValidationError
from pprint import pprint
from decimal import Decimal
import datetime
from vehicle.models import Vehiculo, InformacionTecnicaVehiculo, NuevoKilometraje
from inventory.models import Items,StockItemsHistorico,StockItems
from mining.models import VehiculoAsignado
from checklist.models import ChecklistMaterialesSonda, ChecklistMaterialesCaseta
from datetime import datetime
from django.utils import timezone
import hashlib
from collections import defaultdict
from drilling.models import ReportesOperacionales, ObservacionesReportes
from core.models import Recomendacion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import locale
import pytz
import mysql.connector
class DataPerforacionesListView(APIView):
    def get(self, request):
        usuarios = User.objects.filter(is_active=True)
        perforistas = Perforistas.objects.filter(status=True)
        sondas = Sondas.objects.filter(status=True)
        sondajes = Sondajes.objects.filter(status=True)
        diametros = Diametros.objects.filter(status=True)
        tipo_terreno = TipoTerreno.objects.filter(status=True)
        orientacion = Orientacion.objects.filter(status=True)
        cantidad_agua = CantidadAgua.objects.filter(status=True).order_by('cantidadAgua')
        aditivos = Aditivos.objects.filter(status=True)
        detalle_control_horario = DetalleControlHorario.objects.filter(status=True)
        materiales_sonda = MaterialesSonda.objects.filter(status=True)
        materiales_caseta = MaterialesCaseta.objects.filter(status=True)

        recomendaciones = Recomendacion.objects.filter(status=True).order_by('recomendacion')

        reportesOperacionales = ReportesOperacionales.objects.filter(status=True)
        detallesPerforaciones = DetallesPerforaciones.objects.filter(status=True)
        controlesHorarios = ControlesHorarios.objects.filter(status=True)
        insumos = Insumos.objects.filter(status=True)
        detalleAditivos = DetalleAditivos.objects.filter(status=True)
        longitudPozos = LongitudPozos.objects.filter(status=True)
        observacionesReportes = ObservacionesReportes.objects.filter(status=True)
        materiales_sonda_reporte = ChecklistMaterialesSonda.objects.filter(status=True)
        materiales_caseta_reporte = ChecklistMaterialesCaseta.objects.filter(status=True)

        serializerUsuarios = UsuariosSerializer(usuarios, many=True)
        serializerPerforistas = PerforistasSerializer(perforistas, many=True)
        serializerSondas = SondasSerializer(sondas, many=True)
        serializerSondajes = SondajesSerializer(sondajes, many=True)
        serializerDiametros = DiametrosSerializer(diametros, many=True)
        serializerTipoTerreno = TipoTerrenoSerializer(tipo_terreno, many=True)
        serializerOrientacion = OrientacionSerializer(orientacion, many=True)
        serializerCantidadAgua = CantidadAguaSerializer(cantidad_agua, many=True)
        serializerAditivos = AditivosSerializer(aditivos, many=True)
        serializerDetalleControlHorario = DetalleControlHorarioSerializer(detalle_control_horario, many=True)
        serializerMaterialesSonda = MaterialesSondaSerializer(materiales_sonda, many=True)
        serializerMaterialesCaseta = MaterialesCasetaSerializer(materiales_caseta, many=True)

        serializerRecomendaciones = RecomendacionSerializer(recomendaciones, many=True)
        

        serializerReportesOperacionalesActivos = ReportesOperacionalesActivosSerializer(reportesOperacionales, many=True)
        serializerDetallesPerforacionesActivos = DetallesPerforacionesActivosSerializer(detallesPerforaciones, many=True)
        serializerControlesHorariosActivos = ControlesHorariosActivosSerializer(controlesHorarios, many=True)
        serializerInsumosActivos = InsumosActivosSerializer(insumos, many=True)
        serializerDetalleAditivosActivos = DetalleAditivosActivosSerializer(detalleAditivos, many=True)
        serializerLongitudPozosActivos = LongitudPozosActivosSerializer(longitudPozos, many=True)
        serializerObservacionesReportesActivos = ObservacionesReportesActivosSerializer(observacionesReportes, many=True)

        serializerMaterialesSondaActivos = MaterialesSondaActivosSerializer(materiales_sonda_reporte, many=True)
        serializerMaterialesCasetaActivos = MaterialesCasetaActivosSerializer(materiales_caseta_reporte, many=True)

        data = {
            "usuarios": serializerUsuarios.data,
            "perforistas": serializerPerforistas.data,
            "sondas": serializerSondas.data,
            "sondajes": serializerSondajes.data,
            "diametros": serializerDiametros.data,
            "tipo_terreno": serializerTipoTerreno.data,
            "orientacion": serializerOrientacion.data,
            "cantidad_agua": serializerCantidadAgua.data,
            "aditivos": serializerAditivos.data,
            "detalle_control_horario": serializerDetalleControlHorario.data,
            "turno": [{"value": choice[0], "display": choice[1]} for choice in turno],
            "gemelo": [{"value": choice[0], "display": choice[1]} for choice in gemelo],
            "jornada": [{"value": choice[0], "display": choice[1]} for choice in jornada],
            "materiales_sonda": serializerMaterialesSonda.data,
            "materiales_caseta": serializerMaterialesCaseta.data,
            "recomendaciones": serializerRecomendaciones.data,
            "reportesOperacionales": serializerReportesOperacionalesActivos.data,
            "reportesDetallesPerforaciones": serializerDetallesPerforacionesActivos.data,
            "reportesControlesHorarios": serializerControlesHorariosActivos.data,
            "reportesInsumos": serializerInsumosActivos.data,
            "reportesDetalleAditivos": serializerDetalleAditivosActivos.data,
            "reportesLongitudPozos": serializerLongitudPozosActivos.data,
            "reportesObservacionesReportes": serializerObservacionesReportesActivos.data,
            "reportesMaterialesSonda": serializerMaterialesSondaActivos.data,
            "reportesMaterialesCaseta": serializerMaterialesCasetaActivos.data
        }

        return Response(data, status=status.HTTP_200_OK)

class VehiculosListView(APIView):
    def get(self, request):
        vehiculos = Vehiculo.objects.all()
        serializer = VehiculosSerializer(vehiculos, many=True)
        return Response(serializer.data)

class VehiculoskilometrajesListView(APIView):
    def get(self, request):
        kilometrajes = NuevoKilometraje.objects.all()
        serializer = VehiculosKilometrajesSerializer(kilometrajes, many=True)
        return Response(serializer.data)
        
class VehiculosFaenasListView(APIView):
    def get(self, request):
        vehiculoFaenas = VehiculoAsignado.objects.all()
        serializer = VehiculosFaenasSerializer(vehiculoFaenas, many=True)
        return Response(serializer.data)
        
class SaveReporteOperacionalAPI(APIView):
    def post(self, request):
        data = request.data  # Lista de objetos enviada por el cliente

        resultados = {"procesados": [], "errores": []}

        for item in data:
            try:
                with transaction.atomic():
                    if item.get("tipo") == "reporte":
                        
                        reporte = ReportesOperacionales.objects.filter(
                                sondajeCodigo=item.get('sondajeCodigo'), 
                                sondajeSerie=item.get('sondajeSerie'), 
                                sondajeEstado=item.get('sondajeEstado'), 
                                status=True
                            ).order_by('-correlativo').first()
                        correlativo = 1 if reporte is None else reporte.correlativo + 1
                            # Crea Reporte Operacional
                        try:
                            ReportesOperacionales.objects.filter(id=reporte.id).update(status=False)
                        except:
                            pass
                        reporte_operacional = ReportesOperacionales.objects.create(
                            turno=item.get('turno'),
                            perforista_id=item.get('perforista'),
                            sonda_id=item.get('sonda'),
                            sondajeCodigo_id=item.get('sondajeCodigo'),
                            sondajeSerie=item.get('sondajeSerie'),
                            sondajeEstado=item.get('sondajeEstado'),
                            metroInicial=item.get('metroInicial'),
                            metroFinal=item.get('metroFinal'),
                            totalPerforado=item.get('totalPerforado'),
                            controlador=request.user,
                            creador=item.get('controlador'),
                            id_checklist=item.get('id_checklist'),
                            correlativo=correlativo,
                            progreso="Por Revisar",
                            status=True,
                        )
                        idReporteOperacional = item.get('id')
                        ultimoReporteOperacional = ReportesOperacionales.objects.filter(
                                sondajeCodigo=item.get('sondajeCodigo'), 
                                sondajeSerie=item.get('sondajeSerie'), 
                                sondajeEstado=item.get('sondajeEstado'), 
                                status=True
                            ).order_by('-fechacreacion').first()
                        
                        for obj in data:
                            
                            if obj.get("tipo") == "perforacion" and obj.get("reporte") == idReporteOperacional:
                                
                                try:
                                    detalle_perforacion = DetallesPerforaciones.objects.create(
                                        reporte=ultimoReporteOperacional,
                                        diametros=Diametros.objects.get(id=obj.get('selectedDiametro')),  # Usando el ID correcto
                                        perforado=obj.get('recuperado'),  # Correspondiente al dato "recuperado"
                                        desde=obj.get('desde'),
                                        hasta=obj.get('hasta'),
                                        recuperacion=obj.get('recuperado'),  # Correspondiente al dato "recuperado"
                                        porcentajeRecuperacion=float(obj.get('porcentaje').replace('%', '')),  # Extracción del porcentaje
                                        barra=int(obj.get('barra')),
                                        largoBarra=float(obj.get('largoBarra')),
                                        totalHtas=float(obj.get('totalHta')),
                                        contra=float(obj.get('contra')),
                                        tipoTerreno=TipoTerreno.objects.get(id=obj.get('selectedTipo_Terreno')),  # Usando el ID correcto
                                        orientacion=Orientacion.objects.get(id=obj.get('selectedOrientacion')),  # Usando el ID correcto
                                        status=obj.get('status', True),  # Asignar True si no está explícito
                                    )
                                except:
                                    pass
                            elif obj.get("tipo") == "controlHorario" and obj.get("reporte") == idReporteOperacional:
                                
                                try:
                                    hora_inicio = datetime.datetime.strptime(obj.get('horaInicio'), "%H:%M").time()
                                    hora_final = datetime.datetime.strptime(obj.get('horaFinal'), "%H:%M").time()
                                    total_horas = datetime.datetime.strptime(obj.get('totalHoras'), "%H:%M").time()
                                    
                                    control_horario = ControlesHorarios.objects.create(
                                        reporte=ultimoReporteOperacional,
                                        posicion=1,
                                        inicio=hora_inicio,
                                        final=hora_final,
                                        total=total_horas,
                                        detalleControlHorario=DetalleControlHorario.objects.get(id=obj.get('detalle')),  # Relación con el modelo relacionado
                                        status=True,  # Si aplica un estado por defecto
                                    )
                                except:
                                    pass
                            elif obj.get("tipo") == "longitud" and obj.get("reporte") == idReporteOperacional:
                                
                                longitud_pozos = LongitudPozos.objects.create(
                                    reporte=ultimoReporteOperacional,
                                    largoBarril=Decimal(obj.get('largoBarril')),
                                    largoBarra=Decimal(obj.get('largoBarra')),
                                    puntoMuerto=Decimal(obj.get('puntoMuerto')),
                                    restoBarra=Decimal(obj.get('restoBarra')),
                                    numeroBarras=int(obj.get('numeroBarra')),  # Convertir a entero
                                    longitudPozo=Decimal(obj.get('longitudPozo')),
                                    htaEnPozo=obj.get('htaEnPozo'),
                                    mtsDeHta=Decimal(obj.get('mtsDeHta')),
                                    profundidadHta=Decimal(obj.get('profundidadHta')),
                                    status=obj.get('status', True)  # Asignar True si no está explícito
                                )
                            elif obj.get("tipo") == "insumos" and obj.get("reporte") == idReporteOperacional:
                                
                                cantidadAgua_id = obj.get("cantidadAgua")
                                insumos_reportes = Insumos.objects.create(
                                    reporte=ultimoReporteOperacional,
                                    corona=obj.get('corona'),
                                    escareador=obj.get('escareador'),
                                    casing=obj.get('casing'),
                                    zapata=obj.get('zapata'),
                                    status=True,
                                    cantidadAgua=(CantidadAgua.objects.filter(id=cantidadAgua_id).first() if cantidadAgua_id else None)
                                )
                            elif obj.get("tipo") == "aditivo" and obj.get("reporte") == idReporteOperacional:
                                
                                detalle_aditivos = DetalleAditivos.objects.create(
                                    reporte=ultimoReporteOperacional,
                                    aditivo=Aditivos.objects.get(id=obj.get('aditivo')),
                                    cantidad=int(obj.get('cantidad')),  # Convertir cantidad a entero
                                    status=obj.get('status', True),  # Asignar status o True por defecto
                                )
                            elif obj.get("tipo") == "observacion" and obj.get("reporte") == idReporteOperacional:
                                
                                observaciones_reportes = ObservacionesReportes.objects.create(
                                    reporte=ultimoReporteOperacional,
                                    observaciones=obj.get('observaciones'),
                                    status=True,
                                )

                    return Response({'message': 'Reporte guardado exitosamente'}, status=status.HTTP_201_CREATED)    
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(resultados, status=status.HTTP_200_OK)

class SaveReporteMaterialesSonda(APIView):
    def post(self, request):
        data = request.data  # Lista de objetos enviada por el cliente

        resultados = {"procesados": [], "errores": []}

        for item in data:
            try:
                with transaction.atomic():
                    if item.get("tipo") == "checklistEntrada":
                        
                        checklistEntrada = ChecklistMaterialesSonda.objects.create(
                            item_id=item.get("item"),
                            cantidad=item.get("cantidad"),
                            creador=f"{request.user.first_name} {request.user.last_name}",
                            status=True,
                            etapa="Entrada",   
                            jornada=1,
                            turno=item.get("turno"),
                            sonda=Sondas.objects.get(id=item.get("sonda")),
                            sondajeCodigo=Sondajes.objects.get(id=item.get("sondajeCodigo")),
                            sondajeSerie=item.get("sondajeSerie"),
                            sondajeEstado=item.get("sondajeEstado"),
                            id_checklist=item.get("id_checklist"),
                            progreso="Por Revisar",
                            fecha_checklist=datetime.datetime.strptime(
                                item.get('fecha_checklist'), '%Y-%m-%dT%H:%M:%S.%f'
                            ),
                            fechacreacion=datetime.datetime.strptime(
                                item.get('fechacreacion'), '%Y-%m-%dT%H:%M:%S.%f'
                            )
                        )
                    if item.get("tipo") == "checklistSalida":
                        
                        checklistSalida = ChecklistMaterialesSonda.objects.create(
                            item_id=item.get("item"),
                            cantidad=item.get("cantidad"),
                            creador=f"{request.user.first_name} {request.user.last_name}",
                            status=True,
                            etapa="Salida",   
                            jornada=2,
                            turno=item.get("turno"),
                            sonda=Sondas.objects.get(id=item.get("sonda")),
                            sondajeCodigo=Sondajes.objects.get(id=item.get("sondajeCodigo")),
                            sondajeSerie=item.get("sondajeSerie"),
                            sondajeEstado=item.get("sondajeEstado"),
                            id_checklist=item.get("id_checklist"),
                            progreso="Por Revisar",
                            fecha_checklist=datetime.datetime.strptime(
                                item.get('fecha_checklist'), '%Y-%m-%dT%H:%M:%S.%f'
                            ),
                            fechacreacion=datetime.datetime.strptime(
                                item.get('fechacreacion'), '%Y-%m-%dT%H:%M:%S.%f'
                            )
                        )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Reporte guardado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(resultados, status=status.HTTP_200_OK)

class VehiculoskilometrajesListViewDemo(APIView):
    def get(self, request):
        # Obtiene la fecha más reciente y cuenta la cantidad de registros por vehículo y por origen
        kilometrajes = NuevoKilometraje.objects.values('vehiculo').annotate(
            latest_date=Max('fechacreacion'),
            cant_reportes=Count('vehiculo'),  # Total de veces que aparece el vehículo
            cant_origen=Count('origen'),  # Total de registros por origen
            cant_formulario=Count('origen', filter=Q(origen="Formulario")),  # Veces que es "Formulario"
            cant_mantencion=Count('origen', filter=Q(origen="Mantención"))  # Veces que es "Mantención"
        )

        # Filtramos los registros más recientes
        latest_kilometrajes = []
        for km in kilometrajes:
            latest_kilometraje = NuevoKilometraje.objects.filter(
                vehiculo=km['vehiculo'], 
                fechacreacion=km['latest_date']
            ).first()  # Tomamos el primer (y único) registro con la fecha más reciente

            # Buscar la información de faenas de este vehículo
            vehiculo_faena = VehiculoAsignado.objects.filter(vehiculo=km['vehiculo']).order_by('-fechacreacion').first()
            vehiculo_faena_data = VehiculosFaenasSerializer(vehiculo_faena).data if vehiculo_faena else None


            # Verifica si se obtiene el vehículo correctamente

            vehiculo = Vehiculo.objects.filter(placaPatente=latest_kilometraje).order_by('-fechacreacion').first()

           # Accedemos al vehículo con la placaPatente
            vehiculo_data = VehiculosSerializer(vehiculo).data if vehiculo else None

            # Agregamos manualmente los campos de conteo
            if latest_kilometraje:
                latest_kilometraje.cant_reportes = km['cant_reportes']
                latest_kilometraje.cant_origen = km['cant_origen']
                latest_kilometraje.cant_formulario = km['cant_formulario']
                latest_kilometraje.cant_mantencion = km['cant_mantencion']
                # datos de Faena
                latest_kilometraje.faena = vehiculo_faena_data['faena'] 
                latest_kilometraje.status = vehiculo_faena_data['status']

                #datos generales de vehiculo
                latest_kilometraje.tipo = vehiculo_data['tipo']
                latest_kilometraje.marca = vehiculo_data['marca']
                latest_kilometraje.modelo = vehiculo_data['modelo']
                latest_kilometraje.ano = vehiculo_data['ano']
                latest_kilometraje.situacion = vehiculo_data['status']
                latest_kilometraje.tenencia = vehiculo_data['tenencia'] 
                latest_kilometraje.completado = vehiculo_data['completado']

                latest_kilometrajes.append(latest_kilometraje)

        # Serializa los datos
        serializer = VehiculosKilometrajesSerializer(latest_kilometrajes, many=True)

        # Convertimos los datos serializados en una lista de diccionarios para agregar los conteos
        response_data = serializer.data
        for i, item in enumerate(response_data):
            item["cant_reportes"] = latest_kilometrajes[i].cant_reportes
            item["cant_origen"] = latest_kilometrajes[i].cant_origen
            item["cant_formulario"] = latest_kilometrajes[i].cant_formulario
            item["cant_mantencion"] = latest_kilometrajes[i].cant_mantencion
            #datos de faena
            item["faena"] = latest_kilometrajes[i].faena 
            item["status"] = latest_kilometrajes[i].status 
            #datos generales de vehiculo
            item["tipo"] = latest_kilometrajes[i].tipo
            item["marca"] = latest_kilometrajes[i].marca
            item["modelo"] = latest_kilometrajes[i].modelo
            item["ano"] = latest_kilometrajes[i].ano
            item["situacion"] = latest_kilometrajes[i].situacion
            item["tenencia"] = latest_kilometrajes[i].tenencia
            item["completado"] = latest_kilometrajes[i].completado

        return Response(response_data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

token_obtain_pair = CustomTokenObtainPairView.as_view()

class DashboardVehiculos(APIView):

    def estado_to_text(self, estado):
        return "Habilitado" if estado else "Deshabilitado"
    def get(self, request):
        # Obtener todos los vehículos
        vehiculos = Vehiculo.objects.all()

        # Serializar los vehículos
        serializer = VehiculosSerializer(vehiculos, many=True)
        vehiculos_data = serializer.data  # Convertimos a lista para modificar

        # Iterar sobre los vehículos y agregar información 
        for vehiculo in vehiculos_data:
            vehiculo_id = vehiculo["id"]  # Obtener el ID del vehículo
            # Filtrar registros de kilometraje para este vehículo
            kilometrajes = NuevoKilometraje.objects.filter(vehiculo=vehiculo_id)
            # Obtener cantidad de registros en kilometraje
            cantidad_reportes = kilometrajes.count()
            # Obtener cantidad de registros por origen
            cantidad_origen = kilometrajes.values("origen").distinct().count()
            # Obtener cantidad de registros donde origen es "Formulario"
            cantidad_formulario = kilometrajes.filter(origen="Formulario").count()
            # Obtener cantidad de registros donde origen es "Mantención"
            cantidad_mantencion = kilometrajes.filter(origen="Mantención").count()
            # Buscar el último registro de kilometraje
            ultimo_kilometraje = kilometrajes.order_by('-fechacreacion').first()
            # Buscar la faena y el estado del vehículo
            vehiculo_faena = VehiculoAsignado.objects.filter(vehiculo=vehiculo_id).order_by('-fechacreacion').first()
            faena = str(vehiculo_faena.faena) if vehiculo_faena and vehiculo_faena.faena else "SIN ASIGNAR"
            status_faena = bool(vehiculo_faena.status) if vehiculo_faena else True
            
            # Agregar datos al JSON de respuesta
            vehiculo["kilometraje"] = ultimo_kilometraje.kilometraje if ultimo_kilometraje else None
            vehiculo["cantidad_reportes"] = cantidad_reportes
            vehiculo["cantidad_origen"] = cantidad_origen
            vehiculo["cantidad_formulario"] = cantidad_formulario
            vehiculo["cantidad_mantencion"] = cantidad_mantencion
            vehiculo["cantidad_formulario"] = cantidad_formulario
            vehiculo["cantidad_mantencion"] = cantidad_mantencion
            vehiculo["faena"] = faena
            vehiculo["status_faena"] = status_faena
            # vehiculo["status_faena"] = self.estado_to_text(status_faena)
            # current_status_vehicle = vehiculo["status"]
            # vehiculo["status"] = self.estado_to_text(current_status_vehicle)
            
        return Response(vehiculos_data)

class ReporteAvanceCampana(APIView):
    def get_sheet_sondas(self,reportes_digitales,recomendaciones_sheet_sondas):
        usuarios = User.objects.filter(is_active=True)
        perforistas = Perforistas.objects.filter(status=True)
        sondas = Sondas.objects.filter(status=True)
        sondajes = Sondajes.objects.filter(status=True)
        diametros = Diametros.objects.filter(status=True)
        tipo_terreno = TipoTerreno.objects.filter(status=True)
        orientacion = Orientacion.objects.filter(status=True)
        cantidad_agua = CantidadAgua.objects.filter(status=True).order_by('cantidadAgua')
        aditivos = Aditivos.objects.filter(status=True)
        detalle_control_horario = DetalleControlHorario.objects.filter(status=True)
        materiales_sonda = MaterialesSonda.objects.filter(status=True)
        materiales_caseta = MaterialesCaseta.objects.filter(status=True)

        detallesPerforaciones = DetallesPerforaciones.objects.filter(status=True)
        controlesHorarios = ControlesHorarios.objects.filter(status=True)
        insumos = Insumos.objects.filter(status=True)
        detalleAditivos = DetalleAditivos.objects.filter(status=True)
        longitudPozos = LongitudPozos.objects.filter(status=True)
        observacionesReportes = ObservacionesReportes.objects.filter(status=True)
        materiales_sonda_reporte = ChecklistMaterialesSonda.objects.filter(status=True)
        materiales_caseta_reporte = ChecklistMaterialesCaseta.objects.filter(status=True)

        serializerUsuarios = UsuariosSerializer(usuarios, many=True)
        serializerPerforistas = PerforistasSerializer(perforistas, many=True)
        serializerSondas = SondasSerializer(sondas, many=True)
        serializerSondajes = SondajesSerializer(sondajes, many=True)
        serializerDiametros = DiametrosSerializer(diametros, many=True)
        serializerTipoTerreno = TipoTerrenoSerializer(tipo_terreno, many=True)
        serializerOrientacion = OrientacionSerializer(orientacion, many=True)
        serializerCantidadAgua = CantidadAguaSerializer(cantidad_agua, many=True)
        serializerAditivos = AditivosSerializer(aditivos, many=True)
        serializerDetalleControlHorario = DetalleControlHorarioSerializer(detalle_control_horario, many=True)
        serializerMaterialesSonda = MaterialesSondaSerializer(materiales_sonda, many=True)
        serializerMaterialesCaseta = MaterialesCasetaSerializer(materiales_caseta, many=True)

        serializerRecomendaciones = RecomendacionSerializerAvanceCampana(recomendaciones_sheet_sondas, many=True)

        serializerReportesOperacionalesActivos = ReportesOperacionalesActivosSerializer(reportes_digitales, many=True)
        serializerDetallesPerforacionesActivos = DetallesPerforacionesActivosSerializer(detallesPerforaciones, many=True)
        serializerControlesHorariosActivos = ControlesHorariosActivosSerializer(controlesHorarios, many=True)
        serializerInsumosActivos = InsumosActivosSerializer(insumos, many=True)
        serializerDetalleAditivosActivos = DetalleAditivosActivosSerializer(detalleAditivos, many=True)
        serializerLongitudPozosActivos = LongitudPozosActivosSerializer(longitudPozos, many=True)
        serializerObservacionesReportesActivos = ObservacionesReportesActivosSerializer(observacionesReportes, many=True)

        serializerMaterialesSondaActivos = MaterialesSondaActivosSerializer(materiales_sonda_reporte, many=True)
        serializerMaterialesCasetaActivos = MaterialesCasetaActivosSerializer(materiales_caseta_reporte, many=True)



        data = {
            "usuarios": serializerUsuarios.data,
            "perforistas": serializerPerforistas.data,
            "sondas": serializerSondas.data,
            "sondajes": serializerSondajes.data,
            "diametros": serializerDiametros.data,
            "tipo_terreno": serializerTipoTerreno.data,
            "orientacion": serializerOrientacion.data,
            "cantidad_agua": serializerCantidadAgua.data,
            "aditivos": serializerAditivos.data,
            "detalle_control_horario": serializerDetalleControlHorario.data,
            "turno": [{"value": choice[0], "display": choice[1]} for choice in turno],
            "gemelo": [{"value": choice[0], "display": choice[1]} for choice in gemelo],
            "jornada": [{"value": choice[0], "display": choice[1]} for choice in jornada],
            "materiales_sonda": serializerMaterialesSonda.data,
            "materiales_caseta": serializerMaterialesCaseta.data,
            "recomendaciones": serializerRecomendaciones.data,
            "reportesOperacionales": serializerReportesOperacionalesActivos.data,
            "reportesDetallesPerforaciones": serializerDetallesPerforacionesActivos.data,
            "reportesControlesHorarios": serializerControlesHorariosActivos.data,
            "reportesInsumos": serializerInsumosActivos.data,
            "reportesDetalleAditivos": serializerDetalleAditivosActivos.data,
            "reportesLongitudPozos": serializerLongitudPozosActivos.data,
            "reportesObservacionesReportes": serializerObservacionesReportesActivos.data,
            "reportesMaterialesSonda": serializerMaterialesSondaActivos.data,
            "reportesMaterialesCaseta": serializerMaterialesCasetaActivos.data
        }
        return data, serializerReportesOperacionalesActivos.data
    
    def get_sheet_gerenciales(self,reportes_operacionales,recomendaciones):
        

        for recomendacion in recomendaciones:
            sonda = Sondas.objects.get(id=recomendacion['sonda'],status=True)

            if not sonda:
                sonda = 'SINDATO'   
            else:
                sonda = sonda.sonda

            campana = Campana.objects.get(id=recomendacion['campana'],status=True)
            if not campana:
                campana = 'SINDATO'
            
            programa = Programa.objects.get(id=recomendacion['programa'],status=True)
            if not programa:
                programa = 'SINDATO'

            data_actual = {
                'CAMPAÑA':campana.campana,
                '% AVANCE': 0.00,
                'AVANCE DÍA (m)': 0.00,
                'OBSERVACIÓN': 'SINDATO',
                'PERFORACIÓN AVANCE (m)': 0.00,
                'POR PERFORAR (m)': float(recomendacion['largo_programado']),
                'PROFUNDIDAD PROGRAMADA (m)': float(recomendacion['largo_programado']),
                'PROGRAMA': programa.programa,
                'REC': recomendacion['recomendacion'],
                'SONDA': sonda,
                'SONDAJE': 'SINDATO',
                'UBICACION': recomendacion['sector']
            }

        campanas = Campana.objects.filter(status=True)

        meses_espanol = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
            7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        resultado = {}
        for campana in campanas:
            resultado_actual = {
                campana.campana: {
                    "Metros Planificados": campana.metros,
                    "Programas":[]
                }}

            programas = Programa.objects.filter(campana_id=campana.id,status=True)
            for programa in programas:
                # Zona horaria de Chile
                tz_chile = pytz.timezone('America/Santiago')
                fecha_actual = datetime.now(tz_chile)
                # Obtener el nombre del mes y el número del mes sin cero adelante
                numero_mes = fecha_actual.month  # Ejemplo: 4
                nombre_mes = meses_espanol[numero_mes]  # Ejemplo: "Abril"
                año_actual = fecha_actual.year  # Ejemplo: 2025
                planificaciones = PlanificacionPrograma.objects.filter(campana_id=1, programa_id=1)

                for planificacion in planificaciones:
                    
                    if planificacion.mes == str(numero_mes) and planificacion.ano == año_actual:
                        plan_mes_actual = planificacion.plan
                        plan_acumulada = planificacion.acumuladoPlan
                        resultado_actual[campana.campana]["Programas"].append({
                            "Nombre": programa.programa,
                            f"Metros programados a {nombre_mes}": plan_acumulada,
                            "Metros de avance por programa": 0.00,
                        })
                        break

                
                #quede agregando datos para el diccionario B de la tabla general


        return campana
 

    def get(self, request):

        fecha_inicio = request.GET.get('fecha_inicio', None)
        fecha_final = request.GET.get('fecha_final', None)
        faena_id = request.GET.get('faena_id', None)

        def parse_date_param(value):
            if not value:
                return None
            value = str(value).strip()
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            return None

        fecha_inicio_date = parse_date_param(fecha_inicio)
        fecha_final_date = parse_date_param(fecha_final)

        if not fecha_inicio_date or not fecha_final_date:
            return Response(
                {"error": "Formato de fecha inválido. Usa YYYY-MM-DD."},
                status=status.HTTP_200_OK
            )

        if fecha_inicio_date > fecha_final_date:
            return Response(
                {"error": "La fecha inicial no puede ser mayor que la fecha final."},
                status=status.HTTP_200_OK
            )

        fecha_inicio_dt = timezone.make_aware(
            datetime.combine(fecha_inicio_date, datetime.min.time())
        )
        fecha_final_dt = timezone.make_aware(
            datetime.combine(fecha_final_date, datetime.max.time())
        )

        faena = Faena.objects.get(status=True,id=faena_id)

        # Snapshot histórico: solo entidades creadas hasta fecha final
        campanas = Campana.objects.filter(
            status=True,
            faena_id=faena_id,
            fechacreacion__lte=fecha_final_dt
        )

        if not campanas:
            return Response({"error":f"No existen Campañas para Faena = {faena.faena}"}, status=status.HTTP_200_OK)

        programas = Programa.objects.none()
        recomendaciones_sheet_sondas = Recomendacion.objects.none()
        recomendaciones = Recomendacion.objects.none()
        ajuste_recomendaciones = RecomendacionAjuste.objects.none()
        final_recomendaciones = RecomendacionFinal.objects.none()
        reportes_digitales = ReportesOperacionales.objects.none()
        filtro_fecha_reporte = (
            Q(fechaedicion__range=(fecha_inicio_dt, fecha_final_dt)) |
            Q(fechacreacion__range=(fecha_inicio_dt, fecha_final_dt))
        )
        
        for campana in campanas:

            programas_qs = Programa.objects.filter(
                status=True,
                campana_id=campana.id,
                fechacreacion__lte=fecha_final_dt
            )

            if not programas_qs:
                continue

            programas = programas | programas_qs

            for programa in programas_qs:

                filtro_fecha_recomendacion = (
                    Q(fechacreacion__lte=fecha_final_dt) |
                    Q(fecha_inicio__lte=fecha_final_dt)
                )

                recomendaciones_sheet_sondas_qs = Recomendacion.objects.filter(
                    status=True,
                    campana_id=campana.id,
                    programa_id=programa.id,
                ).filter(
                    filtro_fecha_recomendacion
                ).order_by('recomendacion').defer('campana', 'recomendacion')
                
                if not recomendaciones_sheet_sondas_qs:
                    continue
                
                recomendaciones_sheet_sondas = recomendaciones_sheet_sondas | recomendaciones_sheet_sondas_qs 

                recomendaciones_qs = Recomendacion.objects.filter(
                    status=True,
                    campana_id=campana.id,
                    programa_id=programa.id,
                ).filter(
                    filtro_fecha_recomendacion
                )
                recomendaciones = recomendaciones | recomendaciones_qs
                
                for recomendacion in recomendaciones_qs:
                    
                    
                    ajuste_recomendaciones_qs = RecomendacionAjuste.objects.filter(statusAjuste=True,recomendacionAjuste_id=int(recomendacion.id))
                    final_recomendaciones_qs = RecomendacionFinal.objects.filter(statusFinal=True,recomendacionFinal_id=int(recomendacion.id))

                    if ajuste_recomendaciones_qs:
                        ajuste_recomendaciones = ajuste_recomendaciones | ajuste_recomendaciones_qs

                    if final_recomendaciones_qs:
                        final_recomendaciones = final_recomendaciones | final_recomendaciones_qs


                    reportes_digitales_qs = ReportesOperacionales.objects.filter(
                        status=True,
                        sonda_id=recomendacion.sonda_id,
                    ).filter(filtro_fecha_reporte)

                    if reportes_digitales_qs:
                        reportes_digitales = reportes_digitales | reportes_digitales_qs

        reportes_faena_qs = ReportesOperacionales.objects.filter(
            status=True,
            sondajeCodigo__faena_id=faena_id,
        ).filter(filtro_fecha_reporte)
        if reportes_faena_qs:
            reportes_digitales = reportes_digitales | reportes_faena_qs

        if not programas:   
            return Response({"error":f"No existen Programas para Faena = {faena.faena}"}, status=status.HTTP_200_OK)

        if not recomendaciones_sheet_sondas:
            return Response({"error":f"No existen Recomendaciones para Faena = {faena.faena}"}, status=status.HTTP_200_OK)    
        
        if not reportes_digitales:
            return Response({"error":f"No existen Reportes Digitales para Faena = {faena.faena}"}, status=status.HTTP_200_OK)
        

        sondas,reportes_operacionales = self.get_sheet_sondas(reportes_digitales,recomendaciones_sheet_sondas)



        campanas_ids = campanas.values_list('id', flat=True)
        programas_ids = programas.values_list('id', flat=True)

        campanas = Campana.objects.filter(
            status=True,
            id__in=campanas_ids,
            fechacreacion__lte=fecha_final_dt
        )
        programas = Programa.objects.filter(
            status=True,
            id__in=programas_ids,
            fechacreacion__lte=fecha_final_dt
        )
        planificacion_programas = PlanificacionPrograma.objects.filter(
            campana_id__in=campanas_ids,
            programa_id__in=programas_ids,
            fechacreacion__lte=fecha_final_dt
        )

        serializerCampana = CampanaSerializer(campanas, many=True)
        serializerPrograma = ProgramaSerializer(programas, many=True)
        serializerRecomendaciones = RecomendacionSerializer(recomendaciones, many=True)
        serializerRecomendacionesAjuste = RecomendacionAjusteSerializer(ajuste_recomendaciones, many=True)
        serializerRecomendacionesFinal = RecomendacionFinalSerializer(final_recomendaciones, many=True)
        serializerPlanificacionPrograma = PlanificacionProgramaSerializer(planificacion_programas, many=True)

        resultado = {
            "data_sondas": sondas,
            "all_recomendaciones": serializerRecomendaciones.data,
            "data_campanas":serializerCampana.data,
            "data_programas": serializerPrograma.data,
            "data_planificacion_programas":serializerPlanificacionPrograma.data,
            "all_ajuste_recomendaciones": serializerRecomendacionesAjuste.data,
            "all_final_recomendaciones": serializerRecomendacionesFinal.data,
            
        }

        return Response(resultado, status=status.HTTP_200_OK)

class SaveReport(APIView):
    def format_total_hours(self, total_hours: str) -> str:
        partes = total_hours.split(".")
        horas = int(partes[0])
        minutos = int(partes[1]) if len(partes) > 1 else 0
        return f"{horas:02}:{minutos:02}:00.000000"

    def hash_checklist_id(self,value):
        hash_obj = hashlib.sha256(value.encode('utf-8')).hexdigest()
        # Convertir el hash hexadecimal a un número entero
        hash_int = int(hash_obj, 16)
        # Reducirlo a 20 dígitos
        hash_numeric = int(str(hash_int)[:15])
        return  hash_numeric
    
    def create_data(self, data):
        for item in data:
            data_time = item['dateTime']
            item = item['value']
            creador = item["digitalReport"]['drillingSupervisor']
            #ultimo_registro = ChecklistMaterialesSonda.objects.order_by('-fechacreacion').first()

            fecha_checkist = data_time
            sonda = Sondas.objects.get(id=item["entry"]["drillingRig"])
            sondaje = Sondajes.objects.get(id=item["entry"]["drillingType"])
            numero_sondaje = item["entry"]["drillingNumber"]
            gemelo = item["entry"].get("twin","")

            hash_checklist_id = self.hash_checklist_id(f'{fecha_checkist}{sonda}{sondaje}{numero_sondaje}{gemelo}')

            new_id_checklist = hash_checklist_id
            if item.get("entry"):
                
                for key, value in item["entry"]['items'].items():    
                    #buscar el ultimo id + 1 que exista en la db
                    key = key.replace("id_", "", 1)
                    now = timezone.now()
                    checklistEntrada = ChecklistMaterialesSonda.objects.create(
                        item_id=key,
                        cantidad=value,
                        creador=creador,
                        status=True,
                        etapa="Entrada",   
                        #jornada=item["entry"]["shift"], 
                        #turno=item["entry"]["workday"],
                        jornada=item["entry"]["workday"], 
                        turno=item["entry"]["shift"],
                        sonda=Sondas.objects.get(id=item["entry"]["drillingRig"]),
                        sondajeCodigo=Sondajes.objects.get(id=item["entry"]["drillingType"]),
                        sondajeSerie=item["entry"]["drillingNumber"],
                        sondajeEstado=item["entry"].get("twin"),
                        id_checklist=new_id_checklist,
                        progreso="Por Revisar",
                        fecha_checklist=to_utc(item["entry"]["checklistDate"]),
                        fechacreacion=to_utc(item["entry"]["checklistDate"]),
                    )
            if item.get("digitalReport"):
                item_entry = item["entry"]
                reporte = ReportesOperacionales.objects.filter(
                        sondajeCodigo=int(item_entry["drillingType"]), 
                        sondajeSerie=int(item_entry["drillingNumber"]), 
                        sondajeEstado=item_entry.get(item["entry"]["twin"],None), 
                        status=True
                    ).order_by('-correlativo').first()
                correlativo = 1 if reporte is None else reporte.correlativo + 1
                try:
                    ReportesOperacionales.objects.filter(id=reporte.id).update(status=False)
                except:
                    pass
                controlador = Usuario.objects.get(id=item["digitalReport"]["idSupervisor"])
                reporte_operacional = ReportesOperacionales.objects.create(
                    turno=item["entry"]["shift"],
                    perforista_id=item["digitalReport"]["driller"],
                    sonda_id=int(item["entry"]["drillingRig"]),
                    sondajeCodigo_id=int(item["entry"]["drillingType"]),
                    sondajeSerie=int(item["entry"]["drillingNumber"]),
                    sondajeEstado=item["entry"]["twin"],
                    metroInicial=Decimal(item["digitalReport"]["initialMeter"]),
                    metroFinal=Decimal(item["digitalReport"]["finalMeter"]),
                    totalPerforado=Decimal(item["digitalReport"]["totalMetersDrilled"]), 
                    controlador=controlador,
                    creador=item["digitalReport"]["drillingSupervisor"],
                    id_checklist=new_id_checklist,
                    correlativo=correlativo,
                    progreso="Por Revisar",
                    fechacreacion=to_utc(item["entry"]["checklistDate"]),
                    status=True,
                )
                item_entry = item["entry"]
                ultimoReporteOperacional = ReportesOperacionales.objects.filter(
                        id_checklist=new_id_checklist,
                        status=True
                    ).order_by('-fechacreacion').first()
                

                # punto muerto y largo barril para longitud de pozo
                punto_muerto_raw = Decimal(item["digitalReport"]["wellLength"]['deadPoint'])
                punto_muerto = Decimal("0.00") if punto_muerto_raw <= Decimal("0.1") else punto_muerto_raw

                largo_barril_raw = Decimal(item["digitalReport"]["wellLength"]['barrelLength'])
                largo_barril = Decimal("0.00") if largo_barril_raw <= Decimal("0.1") else largo_barril_raw

                if punto_muerto == Decimal("0.00") and largo_barril == Decimal("0.00"):
                    resto_barra=Decimal("0.00")
                    total_htas=Decimal("0.00")
                    contra=Decimal("0.00")
                else:
                    resto_barra=Decimal(item["digitalReport"]["wellLength"]['remainingBar'])

                for drilling_details in item["digitalReport"]['drillingDetails']:   
                    if punto_muerto == Decimal("0.00") and largo_barril == Decimal("0.00"):
                        total_htas=Decimal("0.00")
                        contra=Decimal("0.00")
                    else:
                        total_htas=float(drilling_details.get('totalHta'))
                        contra=float(drilling_details.get('counter'))


                    detalle_perforacion = DetallesPerforaciones.objects.create(
                        reporte=ultimoReporteOperacional,
                        diametros=Diametros.objects.get(id=drilling_details.get('diameter')),  # Usando el ID correcto
                        perforado=drilling_details.get('drilledMeters'),  # Correspondiente al dato "recuperado"
                        desde=drilling_details.get('from'),
                        hasta=drilling_details.get('to'),
                        recuperacion=drilling_details.get('recovery'),  # Correspondiente al dato "recuperado"
                        porcentajeRecuperacion=float(drilling_details.get('recoveryPercent').replace('%', '')),  # Extracción del porcentaje
                        barra=int(drilling_details.get('bar')),
                        largoBarra=float(drilling_details.get('lengthB')),
                        totalHtas=total_htas,
                        contra=contra,
                        tipoTerreno=TipoTerreno.objects.get(id=drilling_details.get('terrain')),  # Usando el ID correcto
                        orientacion=Orientacion.objects.get(id=drilling_details.get('orientation')),  # Usando el ID correcto
                        fechacreacion=to_utc(item["entry"]["checklistDate"]),
                        status=drilling_details.get('status', True),  # Asignar True si no está explícito
                    )
          
                for time_control in item["digitalReport"]['timeTracking']:
                    # Convertir la cadena a datetime
                    hora_inicio_dt = datetime.fromisoformat(time_control["startTime"])
                    hora_final_dt = datetime.fromisoformat(time_control["endTime"])

                    # Extraer solo la hora en el formato correcto
                    hora_inicio = hora_inicio_dt.strftime("%H:%M")
                    hora_final = hora_final_dt.strftime("%H:%M")
                    total_horas = self.format_total_hours(time_control["totalHours"])
                    total_horas = datetime.strptime(total_horas, "%H:%M:%S.%f")
                    control_horario = ControlesHorarios.objects.create(
                        reporte=ultimoReporteOperacional,
                        posicion=1,
                        inicio=hora_inicio,
                        final=hora_final,
                        total=total_horas,
                        detalleControlHorario=DetalleControlHorario.objects.get(id=time_control.get('detail')),  # Relación con el modelo relacionado
                        fechacreacion=to_utc(item["entry"]["checklistDate"]),
                        status=True,  # Si aplica un estado por defecto
                    )


                longitud_pozos = LongitudPozos.objects.create(
                    reporte=ultimoReporteOperacional,
                    largoBarril=largo_barril,
                    largoBarra=0.0,
                    puntoMuerto=punto_muerto,
                    restoBarra=resto_barra,
                    numeroBarras=int(item["digitalReport"]["wellLength"]['numberOfBars']),  
                    longitudPozo=Decimal(item["digitalReport"]["wellLength"]['wellDepth']),
                    htaEnPozo=item["digitalReport"]["wellLength"]['remainsInWell'],
                    mtsDeHta=Decimal(item["digitalReport"]["wellLength"]['htaMeters']),
                    profundidadHta=Decimal(item["digitalReport"]["wellLength"]['remainingDepth']),
                    status=True
                )
         
                cantidadAgua_id = item["digitalReport"]['supplyControl']['water']
                # if cantidadAgua_id == "":
                #     cantidadAgua_id = None
                insumos_reportes = Insumos.objects.create(
                    reporte=ultimoReporteOperacional,
                    corona=item["digitalReport"]['supplyControl']['crown'],
                    escareador=item["digitalReport"]['supplyControl']['reamer'],
                    casing=item["digitalReport"]['supplyControl']['casing'],
                    zapata=item["digitalReport"]['supplyControl']['shoe'],
                    status=True,
                    cantidadAgua=(CantidadAgua.objects.filter(id=cantidadAgua_id).first() if cantidadAgua_id else None)
                )
       
                for additive in item["digitalReport"]['additives']:
                    detalle_aditivos = DetalleAditivos.objects.create(
                            reporte=ultimoReporteOperacional,
                            aditivo=Aditivos.objects.get(id=int(additive['detail'])),
                            cantidad=int(additive['sackQuantity']),  # Convertir cantidad a entero
                            fechacreacion=to_utc(item["entry"]["checklistDate"]),
                            status=True,  
                    )
   
                comments = item["digitalReport"]['comments']
                # if comments == "":
                #     comments = None
                observaciones_reportes = ObservacionesReportes.objects.create(
                reporte=ultimoReporteOperacional,
                observaciones=comments,
                status=True,
                )
                
            if item.get("exit"):
                for key, value in item["exit"]['items'].items():
                    key = key.replace("id_", "", 1)
                    now = timezone.now()
                    checklistSalida = ChecklistMaterialesSonda.objects.create(
                        item_id=key,
                        cantidad=value,
                        creador=creador,
                        status=True,
                        etapa="Salida",   
                        jornada=item["exit"]["workday"], 
                        turno=item["exit"]["shift"],
                        sonda=Sondas.objects.get(id=item["exit"]["drillingRig"]),
                        sondajeCodigo=Sondajes.objects.get(id=item["exit"]["drillingType"]),
                        sondajeSerie=item["exit"]["drillingNumber"],
                        sondajeEstado=item["exit"].get("twin"),
                        id_checklist=new_id_checklist,
                        progreso="Por Revisar",
                        fecha_checklist=to_utc(item["exit"]["checklistDate"]),
                        fechacreacion=to_utc(item["exit"]["checklistDate"]),
                    
                )

    def get_match(self, checklist, item):

        creador = item["digitalReport"]['drillingSupervisor']

        crear_nuevos_valores = {}

        for key, value in item["entry"]['items'].items():
            delete_ket = key
            key = key.replace("id_", "", 1)

            if checklist.item_id == int(key) and checklist.etapa == "Entrada":
                del item["entry"]['items'][delete_ket]

        return item

    def update_data(self, data):
        for item in data:
            id_checklist =item['idChecklist']
            item = item['value']
            creador = item["digitalReport"]['drillingSupervisor']
            current_checklists = ChecklistMaterialesSonda.objects.filter(
                    progreso="Por Corregir",
                    id_checklist=id_checklist,
                    status=True
                )
            for checklist in current_checklists:
                checklist.status = False
                checklist.save()

            current_reporte_operacionales = ReportesOperacionales.objects.filter(
                    progreso="Por Corregir",
                    id_checklist=id_checklist,
                    status=True
                )  
            
            for current_reporte_operacional in current_reporte_operacionales:
                current_reporte_operacional.status = False
                current_reporte_operacional.save()
                
                reporte_id= int(current_reporte_operacional.id)

                current_detalle_perforaciones = DetallesPerforaciones.objects.filter(
                    reporte_id=reporte_id,
                    status=True
                )   
                
                for current_detalle_perforacion in current_detalle_perforaciones:
                    current_detalle_perforacion.status = False
                    current_detalle_perforacion.save()

                current_controles_horarios = ControlesHorarios.objects.filter(
                    reporte_id=reporte_id,
                    status=True
                )     

                for current_control_horario in current_controles_horarios:
                    current_control_horario.status = False
                    current_control_horario.save()

                current_longitudes_pozos = LongitudPozos.objects.filter(
                    reporte_id=reporte_id,
                    status=True
                )     

                for current_longitud_pozo in current_longitudes_pozos:
                    current_longitud_pozo.status = False
                    current_longitud_pozo.save()

                current_insumos = Insumos.objects.filter(
                    reporte_id=reporte_id,
                    status=True
                )     

                for current_insumo in current_insumos:
                    current_insumo.status = False
                    current_insumo.save()

                current_aditivos = DetalleAditivos.objects.filter(
                    reporte_id=reporte_id,
                    status=True
                )     

                for current_aditivo in current_aditivos:
                    current_aditivo.status = False
                    current_aditivo.save()

                current_observaciones = ObservacionesReportes.objects.filter(
                    reporte_id=reporte_id,
                    status=True
                )     

                for current_observacion in current_observaciones:
                    current_observacion.status = False
                    current_observacion.save()

            if item.get("entry"):
                for key, value in item["entry"]['items'].items():
                    key = key.replace("id_", "", 1)
                    now = timezone.now()
                    checklistEntrada = ChecklistMaterialesSonda.objects.create(
                        item_id=key,
                        cantidad=value,
                        creador=creador,
                        status=True,
                        etapa="Entrada",   
                        jornada=item["entry"]["workday"], 
                        turno=item["entry"]["shift"],
                        sonda=Sondas.objects.get(id=item["entry"]["drillingRig"]),
                        sondajeCodigo=Sondajes.objects.get(id=item["entry"]["drillingType"]),
                        sondajeSerie=int(item["entry"]["drillingNumber"]),
                        sondajeEstado=item["entry"].get("twin"),
                        id_checklist=id_checklist,
                        progreso="Por Revisar",
                        fecha_checklist=to_utc(item["entry"]["checklistDate"]),
                        fechacreacion=now,
                    )
            if item.get("digitalReport"):
                item_entry = item["entry"]
                reporte = ReportesOperacionales.objects.filter(
                        sondajeCodigo=int(item_entry["drillingType"]), 
                        sondajeSerie=int(item_entry["drillingNumber"]), 
                        sondajeEstado=item_entry.get("twin"), 
                        status=True
                    ).order_by('-correlativo').first()
                correlativo = 1 if reporte is None else reporte.correlativo + 1
                
                # --- CORRECCIÓN: ELIMINAR ESTAS LÍNEAS ---
                # Estas líneas borraban el reporte aprobado anterior.
                # try:
                #    ReportesOperacionales.objects.filter(id=reporte.id).update(status=False)
                # except:
                #    pass
                # -----------------------------------------

                controlador = Usuario.objects.get(id=item["digitalReport"]["idSupervisor"])
                reporte_operacional = ReportesOperacionales.objects.create(
                    turno=item["entry"]["shift"],
                    perforista_id=item["digitalReport"]["driller"],
                    sonda_id=int(item["entry"]["drillingRig"]),
                    sondajeCodigo_id=int(item["entry"]["drillingType"]),
                    sondajeSerie=int(item["entry"]["drillingNumber"]),
                    sondajeEstado=item["entry"].get("twin"),
                    metroInicial=Decimal(item["digitalReport"]["initialMeter"]),
                    metroFinal=Decimal(item["digitalReport"]["finalMeter"]),
                    totalPerforado=Decimal(item["digitalReport"]["totalMetersDrilled"]), 
                    controlador=controlador,
                    creador=item["digitalReport"]["drillingSupervisor"],
                    id_checklist=id_checklist,
                    correlativo=correlativo,
                    progreso="Por Revisar",
                    status=True,
                )
                item_entry = item["entry"]
                ultimoReporteOperacional = ReportesOperacionales.objects.filter(
                        id_checklist=id_checklist,
                        status=True
                    ).order_by('-fechacreacion').first()
                
                # punto muerto y largo barril para longitud de pozo
                punto_muerto_raw = Decimal(item["digitalReport"]["wellLength"]['deadPoint'])
                punto_muerto = Decimal("0.00") if punto_muerto_raw <= Decimal("0.1") else punto_muerto_raw

                largo_barril_raw = Decimal(item["digitalReport"]["wellLength"]['barrelLength'])
                largo_barril = Decimal("0.00") if largo_barril_raw <= Decimal("0.1") else largo_barril_raw

                if punto_muerto == Decimal("0.00") and largo_barril == Decimal("0.00"):
                    resto_barra=Decimal("0.00")
                    total_htas=Decimal("0.00")
                    contra=Decimal("0.00")
                else:
                    resto_barra=Decimal(item["digitalReport"]["wellLength"]['remainingBar'])

                for drilling_details in item["digitalReport"]['drillingDetails']:   
                    if punto_muerto == Decimal("0.00") and largo_barril == Decimal("0.00"):
                        total_htas=Decimal("0.00")
                        contra=Decimal("0.00")
                    else:
                        total_htas=float(drilling_details.get('totalHta'))
                        contra=float(drilling_details.get('counter'))

                for drilling_details in item["digitalReport"]['drillingDetails']:       
                    detalle_perforacion = DetallesPerforaciones.objects.create(
                        reporte=ultimoReporteOperacional,
                        diametros=Diametros.objects.get(id=drilling_details.get('diameter')),  # Usando el ID correcto
                        perforado=drilling_details.get('drilledMeters'),  # Correspondiente al dato "recuperado"
                        desde=drilling_details.get('from'),
                        hasta=drilling_details.get('to'),
                        recuperacion=drilling_details.get('recovery'),  # Correspondiente al dato "recuperado"
                        porcentajeRecuperacion=float(drilling_details.get('recoveryPercent').replace('%', '')),  # Extracción del porcentaje
                        barra=int(drilling_details.get('bar')),
                        largoBarra=float(drilling_details.get('lengthB')),

                        totalHtas=total_htas,
                        contra=contra,

                        tipoTerreno=TipoTerreno.objects.get(id=drilling_details.get('terrain')),  # Usando el ID correcto
                        orientacion=Orientacion.objects.get(id=drilling_details.get('orientation')),  # Usando el ID correcto
                        status=drilling_details.get('status', True),  # Asignar True si no está explícito
                    )
                for time_control in item["digitalReport"]['timeTracking']:
                    # Convertir la cadena a datetime
                    hora_inicio_dt = datetime.fromisoformat(time_control["startTime"])
                    hora_final_dt = datetime.fromisoformat(time_control["endTime"])
                    # Extraer solo la hora en el formato correcto
                    hora_inicio = hora_inicio_dt.strftime("%H:%M")
                    hora_final = hora_final_dt.strftime("%H:%M")
                    total_horas = self.format_total_hours(time_control["totalHours"])
                    control_horario = ControlesHorarios.objects.create(
                        reporte=ultimoReporteOperacional,
                        posicion=1,
                        inicio=hora_inicio,
                        final=hora_final,
                        total=total_horas,
                        detalleControlHorario=DetalleControlHorario.objects.get(id=time_control.get('detail')),  # Relación con el modelo relacionado
                        status=True,  # Si aplica un estado por defecto
                    )
                longitud_pozos = LongitudPozos.objects.create(
                    reporte=ultimoReporteOperacional,
                    largoBarril=largo_barril,
                    largoBarra=0.0,
                    puntoMuerto=punto_muerto,
                    restoBarra=resto_barra,
                    numeroBarras=int(item["digitalReport"]["wellLength"]['numberOfBars']),  # Convertir a entero
                    longitudPozo=Decimal(item["digitalReport"]["wellLength"]['wellDepth']),
                    htaEnPozo=item["digitalReport"]["wellLength"]['remainsInWell'],
                    mtsDeHta=Decimal(item["digitalReport"]["wellLength"]['htaMeters']),
                    profundidadHta=Decimal(item["digitalReport"]["wellLength"]['remainingDepth']),
                    status=True
                )
                cantidadAgua_id = item["digitalReport"]['supplyControl']['water']
                # if cantidadAgua_id == "":
                #     cantidadAgua_id = None
                insumos_reportes = Insumos.objects.create(
                    reporte=ultimoReporteOperacional,
                    corona=item["digitalReport"]['supplyControl']['crown'],
                    escareador=item["digitalReport"]['supplyControl']['reamer'],
                    casing=item["digitalReport"]['supplyControl']['casing'],
                    zapata=item["digitalReport"]['supplyControl']['shoe'],
                    status=True,
                    cantidadAgua=(CantidadAgua.objects.filter(id=cantidadAgua_id).first() if cantidadAgua_id else None)
                )
                for additive in item["digitalReport"]['additives']:
                    detalle_aditivos = DetalleAditivos.objects.create(
                            reporte=ultimoReporteOperacional,
                            aditivo=Aditivos.objects.get(id=int(additive['detail'])),
                            cantidad=int(additive['sackQuantity']),  # Convertir cantidad a entero
                            status=True,  
                    )
                comments = item["digitalReport"]['comments']
                # if comments == "":
                #     comments = None
                observaciones_reportes = ObservacionesReportes.objects.create(
                reporte=ultimoReporteOperacional,
                observaciones=comments,
                status=True,
                )
                
            if item.get("exit"):
                for key, value in item["exit"]['items'].items():
                    key = key.replace("id_", "", 1)
                    now = timezone.now()
                    checklistSalida = ChecklistMaterialesSonda.objects.create(
                        item_id=key,
                        cantidad=value,
                        creador=creador,
                        status=True,
                        etapa="Salida",   
                        jornada=item["exit"]["workday"], 
                        turno=item["exit"]["shift"],
                        sonda=Sondas.objects.get(id=int(item["exit"]["drillingRig"])),
                        sondajeCodigo=Sondajes.objects.get(id=item["exit"]["drillingType"]),
                        sondajeSerie=int(item["exit"]["drillingNumber"]),
                        sondajeEstado=item["exit"].get("twin"),
                        id_checklist=id_checklist,
                        progreso="Por Revisar",
                        fecha_checklist=to_utc(item["exit"]["checklistDate"]),
                        fechacreacion=now,
                    
                )


    def post(self, request):
        data = request.data  # Lista de objetos enviada por el cliente
        resultados = {"procesados": [], "errores": []}
        new_data = data['create']
        update_data = data['update']
        try:
            with transaction.atomic():
                if new_data:
                    self.create_data(new_data)
                if update_data:
                    self.update_data(update_data)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Reporte guardado exitosamente'}, status=status.HTTP_201_CREATED)
class ReadReport_v1(APIView):

    def get(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "Se requiere el parámetro 'user_id'"}, status=status.HTTP_400_BAD_REQUEST)

        materiales_sondas = (
            ChecklistMaterialesSonda.objects.filter(status=True, progreso__in=["Aprobado", "Por Corregir"])
            .select_related("sondajeCodigo", "sonda", "item")
            .order_by("-fecha_checklist")
        )

        reportes_query = (
            ReportesOperacionales.objects.filter(status=True, progreso__in=["Aprobado", "Por Corregir"])
            .select_related("perforista", "controlador", "sondajeCodigo")
            .order_by('id')
        )
        
        reportes = {
            (r.id_checklist, r.progreso): r
            for r in reportes_query
        }

        detalles_perforaciones_map = {}
        for d in DetallesPerforaciones.objects.filter(status=True).select_related(
            "diametros", "tipoTerreno", "orientacion"
        ):
            detalles_perforaciones_map.setdefault(d.reporte_id, []).append(d)

        controles_horarios_map = {}
        for c in ControlesHorarios.objects.filter(status=True).select_related("detalleControlHorario").order_by('id'):
            controles_horarios_map.setdefault(c.reporte_id, []).append(c)

        longitud_pozo_map = {
            lp.reporte_id: lp
            for lp in LongitudPozos.objects.filter(status=True).order_by('id')
        }

        insumos_map = {
            ins.reporte_id: ins
            for ins in Insumos.objects.filter(status=True).select_related("cantidadAgua").order_by('id')
        }

        aditivos_map = {}
        for ad in DetalleAditivos.objects.filter(status=True).select_related("aditivo").order_by('id'):
            aditivos_map.setdefault(ad.reporte_id, []).append(ad)

        observaciones_map = {
            o.reporte_id: o
            for o in ObservacionesReportes.objects.filter(status=True).order_by('id')
        }

        now = timezone.now().astimezone(timezone.utc)
        data = []
        index = set() 

        for material in materiales_sondas:
            # Clave única para evitar procesar el mismo par checklist-estado dos veces
            unique_key = (material.id_checklist, material.progreso)
            
            if unique_key in index:
                continue
            # Buscar el reporte correspondiente basado en checklist y progreso
            reporte = reportes.get((material.id_checklist, material.progreso))
            
            if not reporte:
                continue
                
            index.add(unique_key)

            reporte_digital = {
                "driller": reporte.perforista.id,
                "drillingSupervisor": reporte.creador,
                "initialMeter": str(reporte.metroInicial),
                "finalMeter": str(reporte.metroFinal),
                "totalMetersDrilled": str(reporte.totalPerforado),
                "idSupervisor": reporte.controlador.id,
            }
            detalles = detalles_perforaciones_map.get(reporte.id, [])
            reporte_digital["drillingDetails"] = [
                {
                    "diameter": d.diametros.id,
                    "drilledMeters": str(d.perforado),
                    "from": str(d.desde),
                    "to": str(d.hasta),
                    "recovery": str(d.recuperacion),
                    "recoveryPercent": str(d.porcentajeRecuperacion),
                    "bar": str(d.barra),
                    "lengthB": str(d.largoBarra),
                    "totalHta": str(d.totalHtas),
                    "counter": str(d.contra),
                    "terrain": d.tipoTerreno.id,
                    "orientation": d.orientacion.id,
                }
                for d in detalles
            ]

            controles = controles_horarios_map.get(reporte.id, [])
            reporte_digital["timeTracking"] = [
                {
                    "startTime": c.inicio.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                    "endTime": c.final.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                    "totalHours": c.total.strftime("%H.%M").lstrip("0"),
                    "detail": c.detalleControlHorario.id,
                }
                for c in controles
            ]

            longitud_pozo = longitud_pozo_map.get(reporte.id)
            if longitud_pozo:
                reporte_digital["wellLength"] = {
                    "barrelLength": str(longitud_pozo.largoBarril),
                    "deadPoint": str(longitud_pozo.puntoMuerto),
                    "remainingBar": str(longitud_pozo.restoBarra),
                    "numberOfBars": str(longitud_pozo.numeroBarras),
                    "wellDepth": str(longitud_pozo.longitudPozo),
                    "remainsInWell": longitud_pozo.htaEnPozo,
                    "htaMeters": str(longitud_pozo.mtsDeHta),
                    "remainingDepth": str(longitud_pozo.profundidadHta),
                }

            insumo = insumos_map.get(reporte.id)
            if insumo:
                reporte_digital["supplyControl"] = {
                    "crown": insumo.corona,
                    "reamer": insumo.escareador,
                    "water": str(insumo.cantidadAgua.id) if insumo.cantidadAgua else "",
                    "casing": insumo.casing,
                    "shoe": insumo.zapata,
                }

            aditivos = aditivos_map.get(reporte.id, [])
            reporte_digital["additives"] = [
                {"detail": a.aditivo.id, "sackQuantity": str(a.cantidad)} for a in aditivos
            ]

            observ = observaciones_map.get(reporte.id)
            reporte_digital["comments"] = str(observ.observaciones) if observ else ""

            data.append(
                {
                    "dateTime": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                    "drillingType": material.sondajeCodigo.id,
                    "drillingNumber": material.sondajeSerie,
                    "twin": material.sondajeEstado,
                    "idChecklist": material.id_checklist,
                    "progress": reporte.progreso,
                    "value": {"digitalReport": reporte_digital},
                }
            )

        # Segunda parte: materiales entrada/salida
        for material in materiales_sondas:
            existing_entry = next(
                (item for item in data 
                 if item["idChecklist"] == material.id_checklist and item["progress"] == material.progreso), 
                None
            )
            if not existing_entry:
                continue

            items_field = "entry" if material.etapa == "Entrada" else "exit"
            items_key = f"id_{material.item.id}"
            items_dict = existing_entry["value"].get(items_field, {}).get("items", {})
            items_dict[items_key] = str(material.cantidad)

            value = {
                "checklistDate": material.fecha_checklist.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                "shift": str(material.jornada),
                "drillingRig": material.sonda.id,
                "drillingType": material.sondajeCodigo.id,
                "drillingNumber": str(material.sondajeSerie),
                "twin": str(material.sondajeEstado),
                "items": items_dict,
                "workday": "1" if material.etapa == "Entrada" else "2",
            }

            existing_entry["value"][items_field] = value
            if material.etapa == "Salida":
                existing_entry["dateTime"] = material.fecha_checklist.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        return Response({"read": data}, status=status.HTTP_200_OK)
class ReadReport_v0(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")  # Captura el valor desde la URL ( es el Rut)

        if not user_id:
            return Response({"error": "Se requiere el parámetro 'user_id'"}, status=status.HTTP_400_BAD_REQUEST)
    

        data = []
        index=[]


        materiales_sondas = ChecklistMaterialesSonda.objects.filter(
            status=True
        ).order_by('-fecha_checklist')

        now = timezone.now().astimezone(timezone.utc) 

        if materiales_sondas:
            for material in materiales_sondas:

                if material.id_checklist not in index:
                
                    reporte = ReportesOperacionales.objects.filter(
                            sondajeCodigo=int(material.sondajeCodigo.id), 
                            sondajeSerie=int(material.sondajeSerie), 
                            sondajeEstado=material.sondajeEstado, 
                            id_checklist=material.id_checklist,
                            status=True
                        ).first()
                    
                    if not reporte:
                        continue
                    index.append(material.id_checklist)
                    reporte_digital = {
                            "driller": reporte.perforista.id,
                            "drillingSupervisor": reporte.creador,
                            "initialMeter": str(reporte.metroInicial),
                            "finalMeter": str(reporte.metroFinal),
                            "totalMetersDrilled": str(reporte.totalPerforado),
                            "idSupervisor":reporte.controlador.id
                            }


                    detalles_perforaciones = DetallesPerforaciones.objects.filter(
                        reporte=reporte.id,
                        status=True
                        )
                    detalles_perforacion = []
                    for detalle in detalles_perforaciones:
                        detalles_perforacion.append(
                            {
                            "diameter": detalle.diametros.id,
                            "drilledMeters": str(detalle.perforado),
                            "from": str(detalle.desde),
                            "to": str(detalle.hasta),
                            "recovery": str(detalle.recuperacion),
                            "recoveryPercent": str(detalle.porcentajeRecuperacion),
                            "bar": str(detalle.barra),
                            "lengthB": str(detalle.largoBarra),
                            "totalHta": str(detalle.totalHtas),
                            "counter": str(detalle.contra),
                            "terrain": detalle.tipoTerreno.id,
                            "orientation": detalle.orientacion.id
                            }
                        )

                    reporte_digital["drillingDetails"] = detalles_perforacion

                    control_horarios = ControlesHorarios.objects.filter(
                        reporte=reporte.id,
                        status=True
                    )

                    seguimiento_horario = []
                    for control_horario in control_horarios:
                        seguimiento_horario.append(

                            {
                            "startTime": control_horario.inicio.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                            "endTime": control_horario.final.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                            "totalHours": control_horario.total.strftime('%H.%M').lstrip("0"),
                            "detail": control_horario.detalleControlHorario.id
                            }
                        )

                    reporte_digital["timeTracking"] = seguimiento_horario
                    longitud_pozo = LongitudPozos.objects.filter(
                        reporte=reporte.id,
                        status=True
                    ).first()
                    reporte_digital["wellLength"] = {
                                "barrelLength": str(longitud_pozo.largoBarril),
                                "deadPoint": str(longitud_pozo.puntoMuerto),
                                "remainingBar": str(longitud_pozo.restoBarra),
                                "numberOfBars": str(longitud_pozo.numeroBarras),
                                "wellDepth": str(longitud_pozo.longitudPozo),
                                "remainsInWell": longitud_pozo.htaEnPozo,
                                "htaMeters": str(longitud_pozo.mtsDeHta),
                                "remainingDepth": str(longitud_pozo.profundidadHta)
                            }
                    
                    insumos = Insumos.objects.filter(
                        reporte=reporte.id,
                        status=True
                    ).first()       


                    cantidad_agua = CantidadAgua.objects.filter(
                        id=insumos.cantidadAgua.id if insumos.cantidadAgua else None
                    ).first()

                    if not cantidad_agua:
                        cantidad_agua = ""
                    
                    else:
                        cantidad_agua = str(cantidad_agua.id)

                    
                    reporte_digital["supplyControl"] = ({
                                "crown": insumos.corona,
                                "reamer": insumos.escareador,
                                "water":  cantidad_agua,
                                "casing": insumos.casing,
                                "shoe": insumos.zapata
                            })   

                    detalle_aditivos = DetalleAditivos.objects.filter(
                        reporte=reporte.id,
                        status=True
                    )

                    aditivos = []
                    for aditivo in detalle_aditivos:
                        aditivos.append(
                            {
                            "detail": aditivo.aditivo.id,
                            "sackQuantity": str(aditivo.cantidad)
                            }
                    )

                    reporte_digital["additives"] = aditivos

                    observaciones_reportes = ObservacionesReportes.objects.filter(
                        reporte=reporte.id,
                        status=True
                    ).first()

                    reporte_digital["comments"] = str(observaciones_reportes.observaciones)

                    data.append({
                        "dateTime":now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                        "drillingType":material.sondajeCodigo.id,
                        "drillingNumber":material.sondajeSerie,
                        "twin":material.sondajeEstado,
                        "idChecklist":material.id_checklist,
                        "progress": reporte.progreso,
                        "value":{
                            "digitalReport": reporte_digital
                        }
                        }
                    )  

            items_id_entrada = {}
            items_id_salida = {}

            for material in materiales_sondas:
                existing_entry = next((item for item in data if item["idChecklist"] == material.id_checklist), None)

                if existing_entry:
                    
                    # Crear un nuevo diccionario en cada iteración
                    if material.etapa == "Entrada": 
                        data_type = "entry"
                        items_id_entrada = existing_entry["value"].get("entry", {}).get("items", {}).copy()
                        items_id_entrada[f'id_{material.item.id}'] = str(material.cantidad)
                        value = {
                            "checklistDate": material.fecha_checklist.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                            "shift": str(material.jornada),
                            "drillingRig": material.sonda.id,
                            "drillingType": material.sondajeCodigo.id,
                            "drillingNumber": str(material.sondajeSerie),
                            "twin": str(material.sondajeEstado),
                            "items": items_id_entrada,
                            "workday": "1"
                        }
                    
                    else:
                        
                        
                        data_type = "exit"
                        items_id_salida = existing_entry["value"].get("exit", {}).get("items", {}).copy()
                        items_id_salida[f'id_{material.item.id}'] = str(material.cantidad)
                        value = {
                            "checklistDate": material.fecha_checklist.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                            "shift": str(material.jornada),
                            "drillingRig": material.sonda.id,
                            "drillingType": material.sondajeCodigo.id,
                            "drillingNumber": str(material.sondajeSerie),
                            "twin": str(material.sondajeEstado),
                            "items": items_id_salida,
                            "workday": "2"
                        }
                        existing_entry['dateTime'] = material.fecha_checklist.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                        
                    existing_entry["value"][data_type] = value

        resultado = {
            "read": data
        }

        return Response(resultado, status=status.HTTP_200_OK)
class SelectorReport(APIView):
    def get(self, request):
        usuarios = User.objects.filter(is_active=True).order_by('first_name')
        perforistas = Perforistas.objects.filter(status=True).order_by('perforista')
        sondas = Sondas.objects.filter(status=True)
        sondajes = Sondajes.objects.filter(status=True)
        diametros = Diametros.objects.filter(status=True)
        tipo_terreno = TipoTerreno.objects.filter(status=True)
        orientacion = Orientacion.objects.filter(status=True)
        cantidad_agua = CantidadAgua.objects.filter(status=True).order_by('cantidadAgua')
        aditivos = Aditivos.objects.filter(status=True).order_by('aditivo')
        detalle_control_horario = DetalleControlHorario.objects.filter(status=True).order_by('detalle')
        materiales_sonda = MaterialesSonda.objects.filter(status=True).order_by('material')
        materiales_caseta = MaterialesCaseta.objects.filter(status=True)


        serializerUsuarios = UsuariosSerializer(usuarios, many=True)#.order_by('detalle')
        serializerPerforistas = PerforistasSerializer(perforistas, many=True)#.order_by('detalle')
        serializerSondas = SondasSerializer(sondas, many=True)
        serializerSondajes = SondajesSerializer(sondajes, many=True)
        serializerDiametros = DiametrosSerializer(diametros, many=True)
        serializerTipoTerreno = TipoTerrenoSerializer(tipo_terreno, many=True)
        serializerOrientacion = OrientacionSerializer(orientacion, many=True)
        serializerCantidadAgua = CantidadAguaSerializer(cantidad_agua, many=True)
        serializerAditivos = AditivosSerializer(aditivos, many=True)
        serializerDetalleControlHorario = DetalleControlHorarioSerializer(detalle_control_horario, many=True)
        serializerMaterialesSonda = MaterialesSondaSerializer(materiales_sonda, many=True)
        serializerMaterialesCaseta = MaterialesCasetaSerializer(materiales_caseta, many=True)

        data = {
            "usuarios": serializerUsuarios.data,
            "perforistas": serializerPerforistas.data,
            "sondas": serializerSondas.data,
            "sondajes": serializerSondajes.data,
            "diametros": serializerDiametros.data,
            "tipo_terreno": serializerTipoTerreno.data,
            "orientacion": serializerOrientacion.data,
            "cantidad_agua": serializerCantidadAgua.data,
            "aditivos": serializerAditivos.data,
            "detalle_control_horario": serializerDetalleControlHorario.data,
            "turno": [{"value": choice[0], "display": choice[1]} for choice in turno],
            "gemelo": [{"value": choice[0], "display": choice[1]} for choice in gemelo],
            "jornada": [{"value": choice[0], "display": choice[1]} for choice in jornada],
            "materiales_sonda": serializerMaterialesSonda.data,
            "materiales_caseta": serializerMaterialesCaseta.data,
        }

        return Response(data, status=status.HTTP_200_OK)

class DashboardInventarioVehiculo(APIView):
    def get(self, request):

        #stock_items_historicos = Items.objects.all()
        stock_items_historicos = Items.objects.filter(seccion__seccion="Vehicular")

        serializer = ItemsSerializer(stock_items_historicos, many=True)
        items_data = serializer.data  # Convertimos a lista para modificar

        # Iterar sobre los items y agregar información 

        for item in items_data:
            stock_item = StockItems.objects.filter(item=item['id']).last()
            item['cantidad'] = stock_item.cantidad
            item['stock_minimo']=int(item['stock_minimo'])
            item['stock_maximo']=int(item['stock_maximo'])
            item['fechacreacion'] = datetime.strptime(item['fechacreacion'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

        return Response(items_data)

class DashboardInventarioSondaje(APIView):
    def get(self, request):

        #stock_items_historicos = Items.objects.all()
        stock_items_historicos = Items.objects.filter(seccion__seccion="Sondaje")

        serializer = ItemsSerializer(stock_items_historicos, many=True)
        items_data = serializer.data  # Convertimos a lista para modificar

        # Iterar sobre los items y agregar información 

        for item in items_data:
            stock_item = StockItems.objects.filter(item=item['id']).last()
            item['cantidad'] = stock_item.cantidad
            item['stock_minimo']=int(item['stock_minimo'])
            item['stock_maximo']=int(item['stock_maximo'])
            item['fechacreacion'] = datetime.strptime(item['fechacreacion'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

        return Response(items_data)

class DashboardInventarioPrevencion(APIView):
    def get(self, request):

        #stock_items_historicos = Items.objects.all()
        stock_items_historicos = Items.objects.filter(seccion__seccion="Prevención")

        serializer = ItemsSerializer(stock_items_historicos, many=True)
        items_data = serializer.data  # Convertimos a lista para modificar

        # Iterar sobre los items y agregar información 

        for item in items_data:
            stock_item = StockItems.objects.filter(item=item['id']).last()
            item['cantidad'] = stock_item.cantidad
            item['stock_minimo']=int(item['stock_minimo'])
            item['stock_maximo']=int(item['stock_maximo'])
            item['fechacreacion'] = datetime.strptime(item['fechacreacion'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

        return Response(items_data)
    
class DashboardSondas(APIView):
    def get(self, request):
        
        faena = Faena.objects.get(status=True)
        campanas = Campana.objects.filter(status=True)
        programas = Programa.objects.filter(status=True)
        recomendaciones = Recomendacion.objects.filter(status=True)
        recomendaciones_ajuste = RecomendacionAjuste.objects.filter(status=True)
        recomendaciones_final = RecomendacionFinal.objects.filter(status=True)
        reportes_digitales = ReportesOperacionales.objects.filter(status=True)
        sondas = Sondas.objects.get(status=True)
        sondajes = Sondajes.objects.get(status=True)

        serializerFaena = FaenaSerializer(faena)
        serializerCampana = CampanaSerializer(campanas, many=True)
        serializerPrograma = ProgramaSerializer(programas, many=True)
        serializerRecomendaciones = RecomendacionSerializer(recomendaciones, many=True)
        serializerRecomendacionesAjuste = RecomendacionAjusteSerializer(recomendaciones_ajuste, many=True)
        serializerRecomendacionesFinal = RecomendacionFinalSerializer(recomendaciones_final, many=True)
        serializerPlanificacionPrograma = PlanificacionProgramaSerializer(reportes_digitales, many=True)
        serializerSondas = SondasSerializer(sondas)
        serializerSondajes = SondajesSerializer(sondajes)
        
        
        resultado = {
            "faenas": serializerFaena.data,
            "campanas":serializerCampana.data,
            "programas": serializerPrograma.data,
            "recomendaciones": serializerRecomendaciones.data,
            "recomendaciones_ajuste": serializerRecomendacionesAjuste.data,
            "recomendaciones_finales": serializerRecomendacionesFinal.data,
            "planificacion_programas":serializerPlanificacionPrograma.data,
            "sondas": serializerSondas.data,
            "sondajes": serializerSondajes.data
        }
        return Response(resultado)
class DashboardSondajeTotalAPI(APIView):
    def get(self, request):
        # 1. MAPA DE PLANIFICACIÓN
        mapa_plan = {}
        recomendaciones = Recomendacion.objects.filter(status=True).select_related('campana', 'programa', 'campana__faena')
        
        for rec in recomendaciones:
            if rec.pozo:
                clave_pozo = str(rec.pozo).strip().upper()
                mapa_plan[clave_pozo] = {
                    'faena': rec.campana.faena.faena if rec.campana and rec.campana.faena else 'Sin Faena',
                    'campana': rec.campana.campana if rec.campana else 'Sin Campaña',
                    'programa': rec.programa.programa if rec.programa else 'Sin Programa',
                    'meta_total': float(rec.largo_programado or 0)
                }

        # 2. DATOS REALES
        reportes = ReportesOperacionales.objects.filter(
            status=True,
            progreso='Aprobado' 
        ).select_related('sondajeCodigo')

        data_agrupada = defaultdict(lambda: {'metros_real': 0.0, 'meta_total': 0.0})
        
        nombres_meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }

        for rep in reportes:
            # A. Construir Nombre del Pozo
            codigo = rep.sondajeCodigo.sondaje if rep.sondajeCodigo else ''
            serie = str(rep.sondajeSerie) if rep.sondajeSerie is not None else ''
            gemelo = rep.sondajeEstado if rep.sondajeEstado else ''
            
            nombre_pozo_real = f"{codigo}-{serie}{gemelo}".strip().upper()

            # B. Obtener Fecha
            if rep.fechacreacion:
                anio = rep.fechacreacion.year
                mes_num = rep.fechacreacion.month
            else:
                anio = datetime.now().year
                mes_num = datetime.now().month

            # C. CRUCE (Aquí está el cambio para filtrar)
            info_plan = mapa_plan.get(nombre_pozo_real)

            # --- FILTRO ESTRICTO ---
            # Si el pozo del reporte NO existe en la planificación activa, LO IGNORAMOS.
            if not info_plan:
                continue 

            # Si existe, tomamos sus datos
            faena = info_plan['faena']
            campana = info_plan['campana']
            programa = info_plan['programa']
            meta = info_plan['meta_total']

            # D. Sumar a la agrupación
            clave = (faena, campana, programa, anio, mes_num)
            data_agrupada[clave]['metros_real'] += float(rep.totalPerforado or 0)
            
            if data_agrupada[clave]['meta_total'] == 0:
                data_agrupada[clave]['meta_total'] = meta

        # 3. RESPUESTA
        response_data = []
        for (faena, campana, programa, anio, mes_num), valores in data_agrupada.items():
            
            real = valores['metros_real']
            meta = valores['meta_total']
            pendiente = max(0, meta - real)
            avance_pct = (real / meta * 100) if meta > 0 else 0

            response_data.append({
                'faena': faena,
                'campaña': campana,
                'programa': programa,
                'año': anio,
                'mes programa': nombres_meses.get(mes_num, 'Desconocido'),
                'total mes programa': meta,
                'perforacion avance (m)': real,
                'por perforar': pendiente,
                '% avance': round(avance_pct, 1)
            })

        return Response({"data": response_data}, status=status.HTTP_200_OK)
    

class DashboardSondajeDiarioAPI(APIView):
    def get(self, request):
        try:
            # 1. MAPA DE PLANIFICACIÓN
            mapa_plan = {}
            recomendaciones = Recomendacion.objects.filter(status=True).select_related(
                'campana', 'programa', 'campana__faena'
            ).only(
                'pozo', 'recomendacion', 
                'campana__campana', 'programa__programa', 'campana__faena__faena'
            )
            
            for rec in recomendaciones:
                if rec.pozo:
                    clave_pozo = str(rec.pozo).strip().upper()
                    mapa_plan[clave_pozo] = {
                        'faena': rec.campana.faena.faena if rec.campana and rec.campana.faena else 'Sin Faena',
                        'campaña': rec.campana.campana if rec.campana else 'Sin Campaña', # <--- CORREGIDO: Clave con 'ñ'
                        'programa': rec.programa.programa if rec.programa else 'Sin Programa',
                        'recomendacion': rec.recomendacion or 'S/I'
                    }

            # 2. CARGA MASIVA DE OBSERVACIONES
            obs_dict = {}
            observaciones_qs = ObservacionesReportes.objects.filter(status=True).values('reporte_id', 'observaciones')
            for obs in observaciones_qs:
                obs_dict[obs['reporte_id']] = obs['observaciones'] or "Sin observación"

            # 3. OBTENER REPORTES DIARIOS
            reportes = ReportesOperacionales.objects.filter(
                status=True,
                progreso='Aprobado'
            ).select_related('sondajeCodigo', 'sonda').order_by('-fechacreacion')

            response_data = []

            for rep in reportes:
                # A. Identificar Pozo
                codigo = rep.sondajeCodigo.sondaje if rep.sondajeCodigo else ''
                serie = str(rep.sondajeSerie) if rep.sondajeSerie is not None else ''
                gemelo = rep.sondajeEstado if rep.sondajeEstado else ''
                nombre_pozo = f"{codigo}-{serie}{gemelo}".strip().upper()

                # B. Buscar Observación
                observacion_texto = obs_dict.get(rep.id, "Sin observación")

                # C. Cruce con Planificación
                plan = mapa_plan.get(nombre_pozo, {
                    'faena': 'No Asignado',
                    'campaña': 'No Asignado', # Coincide con la clave del mapa
                    'programa': 'No Asignado',
                    'recomendacion': 'S/I'
                })

                # D. Formatear Fecha
                fecha_str = rep.fechacreacion.strftime("%Y-%m-%d") if rep.fechacreacion else "Sin Fecha"
                
                # E. Turno Seguro
                try:
                    turno_display = rep.get_turno_display()
                except:
                    turno_display = str(rep.turno)

                # F. Construir Fila
                response_data.append({
                    "faena": plan['faena'],
                    "campaña": plan['campaña'], # Ahora sí existe la clave
                    "programa": plan['programa'],
                    "recomendación": plan['recomendacion'],
                    "sonda": rep.sonda.sonda if rep.sonda else "Sin Sonda",
                    "sondaje": nombre_pozo,
                    "turno": turno_display,
                    "fecha": fecha_str,
                    "desde": float(rep.metroInicial or 0),
                    "hasta": float(rep.metroFinal or 0),
                    "perforado": float(rep.totalPerforado or 0),
                    "observacion": observacion_texto,
                })

            return Response({"data": response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from prevencion.models import PrevencionDocumento, VigilanciaMedica
from prevencion.views import _calcular_porcentaje_promedio_documento

class DashboardPrevencionReportesAPI(APIView):
    def get(self, request):
        try:
            documentos_qs = PrevencionDocumento.objects.filter(status=True).select_related('faena', 'plantilla_base').order_by('-fecha_creacion')
            
            response_data = []
            for doc in documentos_qs:
                tipo_display = doc.plantilla_base.get_tipo_display() if doc.plantilla_base else "Sin Tipo"
                plantilla_nombre = doc.plantilla_base.nombre if doc.plantilla_base else "Sin Plantilla"
                faena_nombre = doc.faena.faena if doc.faena else "Sin Faena"
                
                # We calculate the fulfillment percentage dynamically just like the frontend table does.
                porcentaje = _calcular_porcentaje_promedio_documento(doc.contenido)
                
                response_data.append({
                    "id": doc.id,
                    "tipo": tipo_display,
                    "faena": faena_nombre,
                    "porcentaje": porcentaje,
                    "plantilla_base": plantilla_nombre,
                    "creador": doc.creador,
                    "fecha": doc.fecha_creacion.strftime("%d/%m/%Y %H:%M") if doc.fecha_creacion else ""
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardVigilanciaMedicaAPI(APIView):
    """
    API view para extraer los datos de Vigilancia Médica y mandarlos a Google Sheets para Power BI
    """
    def get(self, request):
        try:
            vigilancias_qs = VigilanciaMedica.objects.all().select_related('faena').order_by('-id')
            
            response_data = []
            for vig in vigilancias_qs:
                faena_nombre = vig.faena.faena if vig.faena else "Sin Faena"
                
                response_data.append({
                    "id": vig.id,
                    "rut_trabajador": vig.rut_trabajador,
                    "nombre_completo": vig.nombre_completo,
                    "faena": faena_nombre,
                    "cargo": vig.cargo or "",
                    "fecha_ingreso": vig.fecha_ingreso.strftime("%d/%m/%Y") if vig.fecha_ingreso else "",
                    "antiguedad_anos": vig.antiguedad_anos,
                    "ges": vig.ges or "",
                    
                    # Silice
                    "silice_eval_riesgo": vig.silice_eval_riesgo or "",
                    "silice_nivel_riesgo": vig.silice_nivel_riesgo or "",
                    "silice_fecha_vence": vig.silice_fecha_vence.strftime("%d/%m/%Y") if vig.silice_fecha_vence else "",
                    "silice_vigencia": vig.silice_vigencia or "",
                    
                    # Ruido
                    "ruido_eval_riesgo": vig.ruido_eval_riesgo or "",
                    "ruido_nivel_seguimiento": vig.ruido_nivel_seguimiento or "",
                    "ruido_fecha_vence": vig.ruido_fecha_vence.strftime("%d/%m/%Y") if vig.ruido_fecha_vence else "",
                    "ruido_vigencia": vig.ruido_vigencia or "",
                    
                    # Hipobaria
                    "hipo_exposicion": vig.hipo_exposicion or "",
                    "hipo_fecha_vence": vig.hipo_fecha_vence.strftime("%d/%m/%Y") if vig.hipo_fecha_vence else "",
                    "hipo_vigencia": vig.hipo_vigencia or ""
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
