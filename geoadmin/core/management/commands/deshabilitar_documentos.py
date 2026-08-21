from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import TipoDocumentoFaenaGeneral

class Command(BaseCommand):
    help = 'Deshabilita documentos generales que ya pasaron su fecha de caducidad'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()
        
        documentos_vencidos = TipoDocumentoFaenaGeneral.objects.filter(
            status=True, 
            fechacaducidad__lt=hoy
        )
        
        cantidad = documentos_vencidos.count()
        if cantidad > 0:
            documentos_vencidos.update(status=False)
            self.stdout.write(self.style.SUCCESS(f'Éxito: Se deshabilitaron {cantidad} documentos vencidos.'))
        else:
            self.stdout.write(self.style.SUCCESS('No hay documentos por deshabilitar hoy.'))