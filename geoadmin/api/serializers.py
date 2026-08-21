from rest_framework import serializers
from core.models import (Perforistas, DetalleControlHorario, Sondas, Sondajes, Diametros, TipoTerreno, 
                        Orientacion, CantidadAgua, Aditivos, MaterialesSonda, MaterialesCaseta,Campana,Programa,
                        Recomendacion,RecomendacionAjuste,RecomendacionFinal)
from planning.models import PlanificacionPrograma, PlanificacionCampanas
from drilling.models import (ReportesOperacionales, DetallesPerforaciones, ControlesHorarios,
                        Insumos, DetalleAditivos, LongitudPozos, ObservacionesReportes,)
from user.models import User
from django.core.exceptions import ValidationError
from vehicle.models import Vehiculo, InformacionTecnicaVehiculo, NuevoKilometraje
from mining.models import VehiculoAsignado
from core.models import Tipo, Marca, Modelo, Ano, Color, Faena
from checklist.models import ChecklistMaterialesSonda, ChecklistMaterialesCaseta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from inventory.models import Items, StockItems,SeccionItems, CategoriaItems, DuracionItems

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'role']
        
class PerforistasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perforistas
        fields = '__all__'

class SondasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sondas
        fields = '__all__'

class SondajesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sondajes
        fields = '__all__'

class DiametrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diametros
        fields = '__all__'

class TipoTerrenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTerreno
        fields = '__all__'

class OrientacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientacion
        fields = '__all__'

class CantidadAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CantidadAgua
        fields = '__all__'

class AditivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aditivos
        fields = '__all__'

class DetalleControlHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleControlHorario
        fields = '__all__'

class ReportesOperacionalesActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportesOperacionales
        fields = '__all__'

class DetallesPerforacionesActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesPerforaciones
        fields = '__all__'

class ControlesHorariosActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlesHorarios
        fields = '__all__'

class InsumosActivosSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Insumos
        fields = '__all__'

class DetalleAditivosActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleAditivos
        fields = '__all__'

class LongitudPozosActivosSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LongitudPozos
        fields = '__all__'

class ObservacionesReportesActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservacionesReportes
        fields = '__all__'
        
class MaterialesSondaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialesSonda
        fields = '__all__'

class MaterialesCasetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialesCaseta
        fields = '__all__'

class MaterialesSondaActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistMaterialesSonda
        fields = '__all__'

class MaterialesCasetaActivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistMaterialesCaseta
        fields = '__all__'

"""

class ControlesHorariosSerializer(serializers.Serializer):
    posicion = serializers.IntegerField()
    inicio = serializers.TimeField(format='%H:%M')
    final = serializers.TimeField(format='%H:%M')
    total = serializers.TimeField(format='%H:%M')
    detalleControlHorario_id = serializers.IntegerField()

class InsumosSerializer(serializers.Serializer):
    corona = serializers.CharField(max_length=100)
    escareador = serializers.CharField(max_length=100)
    cantidadAgua_id = serializers.IntegerField()
    casing = serializers.CharField(max_length=100)
    zapata = serializers.CharField(max_length=100)

class DetalleAditivosSerializer(serializers.Serializer):
    aditivo_id = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=2)

class LongitudPozosSerializer(serializers.Serializer):
    largoBarril = serializers.DecimalField(max_digits=10, decimal_places=2)
    puntoMuerto = serializers.DecimalField(max_digits=10, decimal_places=2)
    restoBarra = serializers.DecimalField(max_digits=10, decimal_places=2)
    numeroBarras = serializers.IntegerField()
    longitudPozo = serializers.DecimalField(max_digits=10, decimal_places=2)

class ObservacionesReportesSerializer(serializers.Serializer):
    observaciones = serializers.CharField()

class ReporteOperacionalSerializer(serializers.Serializer):
    # Campos comunes esperados en los objetos
    turno = serializers.CharField(required=False, allow_null=True)
    perforista = serializers.IntegerField(required=False, allow_null=True)
    sonda = serializers.IntegerField(required=False, allow_null=True)
    sondajeCodigo = serializers.IntegerField(required=False, allow_null=True)
    sondajeSerie = serializers.CharField(required=False, allow_null=True)
    sondajeEstado = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    metroInicial = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    metroFinal = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    totalPerforado = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    controlador = serializers.CharField(required=False, allow_null=True)
    # Otros campos posibles
    id = serializers.IntegerField(required=False)
    origen = serializers.CharField(required=False)
    fechacreacion = serializers.DateTimeField(required=False, allow_null=True)
    fechaedicion = serializers.DateTimeField(required=False, allow_null=True)
    progreso = serializers.CharField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    perforado = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    desde = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    hasta = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    recuperacion = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    porcentajeRecuperacion = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    barra = serializers.CharField(required=False, allow_null=True)
    largoBarra = serializers.CharField(required=False, allow_null=True)
    totalHtas = serializers.CharField(required=False, allow_null=True)
    contra = serializers.CharField(required=False, allow_null=True)
    reporte = serializers.IntegerField(required=False, allow_null=True)
    diametros = serializers.IntegerField(required=False, allow_null=True)
    tipoTerreno = serializers.IntegerField(required=False, allow_null=True)
    orientacion = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        # Validar que cada entrada tenga los campos mínimos necesarios
        if "origen" not in data:
            raise ValidationError("El campo 'origen' es obligatorio.")
        # Validaciones adicionales específicas según el tipo de reporte
        if data.get("origen") == "movil":
            if "id" not in data:
                raise ValidationError("El campo 'id' es obligatorio para los datos con origen 'movil'.")
        return data

    def create(self, validated_data):
        # Lógica para guardar el objeto según el formato validado
        if validated_data.get("turno"):
            # Crear un Reporte Operacional
            return ReportesOperacionales.objects.create(**validated_data)
        elif validated_data.get("perforado"):
            # Crear un detalle relacionado con perforaciones
            return DetallesPerforaciones.objects.create(**validated_data)
        else:
            # Manejar otros casos o lanzar error
            raise ValidationError("Formato de datos no reconocido.")

class DetallesPerforacionesSerializer(serializers.Serializer):
    diametros_id = serializers.IntegerField()
    perforado = serializers.DecimalField(max_digits=10, decimal_places=2)
    desde = serializers.DecimalField(max_digits=10, decimal_places=2)
    hasta = serializers.DecimalField(max_digits=10, decimal_places=2)
    recuperacion = serializers.DecimalField(max_digits=10, decimal_places=2)
    porcentajeRecuperacion = serializers.DecimalField(max_digits=5, decimal_places=2)
    barra = serializers.IntegerField()
    largoBarra = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalHtas = serializers.DecimalField(max_digits=10, decimal_places=2)
    contra = serializers.DecimalField(max_digits=10, decimal_places=2)
    tipoTerreno_id = serializers.IntegerField()
    orientacion_id = serializers.IntegerField()
    reporte_id = serializers.IntegerField()
    
    def create(self, validated_data):
        detalle_perforacion = DetallesPerforaciones.objects.create(**validated_data)
        return detalle_perforacion

"""

class VehiculosSerializer(serializers.ModelSerializer):
    tenencia = serializers.CharField(source='get_tenencia_display', read_only=True)  # Sobrescribe tenencia con la etiqueta amigable
    tieneTag = serializers.CharField(source='get_tieneTag_display', read_only=True)  # Sobrescribe tieneTag con la etiqueta amigable
    tipo = serializers.CharField(source='tipo.tipo', read_only=True)
    ano = serializers.CharField(source='ano.ano', read_only=True)
    marca = serializers.CharField(source='marca.marca', read_only=True)
    modelo = serializers.CharField(source='modelo.modelo', read_only=True)
    color = serializers.CharField(source='color.color', read_only=True)

    class Meta:
        model = Vehiculo
        fields = '__all__'
        
class VehiculosKilometrajesSerializer(serializers.ModelSerializer):
    vehiculo = serializers.CharField(source='vehiculo.placaPatente', read_only=True)
    
    class Meta:
        model = NuevoKilometraje
        fields = '__all__'
    
class VehiculosFaenasSerializer(serializers.ModelSerializer):
    vehiculo = serializers.CharField(source='vehiculo.placaPatente', read_only=True)
    faena = serializers.CharField(source='faena.faena', read_only=True)
    
    class Meta:
        model = VehiculoAsignado
        fields = '__all__'

class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = '__all__' 

class RecomendacionAjusteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecomendacionAjuste
        fields = '__all__' 

class RecomendacionFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecomendacionFinal
        fields = '__all__' 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Agregar first_name y last_name a la respuesta del token
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["id"] = self.user.id

        return data


class ItemsSerializer(serializers.ModelSerializer):
    # Si deseas personalizar la salida de los campos puedes hacerlo aquí.
    
    faena = serializers.CharField(source='faena.faena', read_only=True)  
    seccion = serializers.CharField(source='seccion.seccion', read_only=True)
    categoria = serializers.CharField(source='categoria.categoria', read_only=True)
    duracion = serializers.IntegerField(source='duracion.duracion', read_only=True) 

    

    imagen_item = serializers.ImageField(required=False)

    class Meta:
        model = Items
        fields = '__all__' 

class StockItemsSerializer(serializers.ModelSerializer):
    # Si deseas personalizar la salida de los campos puedes hacerlo aquí.

    class Meta:
        model = StockItems
        fields = '__all__' 

class DataReporteAvanceCampañaSerializer(serializers.ModelSerializer):
    def get(self, request):
        pass

class RecomendacionSerializerAvanceCampana(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = (
            'id', 'recomendacion', 'pozo', 'fecha_inicio', 'sector', 'azimut',
            'inclinacion', 'largo_programado', 'largo_real', 'este', 'norte',
            'cota', 'creador', 'status', 'fechacreacion', 'sonda'
        )


class FaenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faena
        fields = '__all__'
class CampanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campana
        fields = '__all__'  

class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'  

class PlanificacionProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionPrograma
        fields = '__all__'