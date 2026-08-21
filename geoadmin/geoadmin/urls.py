from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from core.admin_views import technical_docs

urlpatterns = [
    path('isamax/informacion-tecnica/', technical_docs, name='admin_technical_docs'),
    re_path(r'^isamax/informacion-tecnica/(?P<path>.*)$', technical_docs, name='admin_technical_docs_file'),
    path('isamax/', admin.site.urls),
    path('',include('core.urls')), 
    path('user/',include('user.urls')), 
    path('',include('vehicle.urls')), 
    path('',include('mining.urls')),
    path('',include('maintenance.urls')),
    path('',include('machine.urls')),
    path('',include('documentation.urls')),
    path('',include('messenger.urls')),
    path('',include('planning.urls')),
    path('',include('drilling.urls')),
    path('',include('offline.urls')),
    path('',include('api.urls')),
    path('',include('checklist.urls')),
    path('',include('inventory.urls')),
    path('',include('equipment.urls')),
    path('prevencion/', include('prevencion.urls')),
    path('admin-system/', include('administration.urls')),
]

urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
handler400 = 'core.views.error_400'
handler403 = 'core.views.error_403'
handler404 = 'core.views.error_404'
handler413 = 'core.views.error_413'
handler500 = 'core.views.error_500'
