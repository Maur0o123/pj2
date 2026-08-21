from pathlib import Path
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from .decorators import admin_or_base_datos_required
from user.models import UsuarioProfile

@login_required
@admin_or_base_datos_required
def technical_docs(request, path="index.html"):
    perfil = get_object_or_404(UsuarioProfile, user=request.user)
    roles_permitidos = ['ADMINISTRADOR', 'BASE DATOS']
    if perfil.seccionAdministracion not in roles_permitidos:
        return redirect("select")  
    request.session['seccion'] = 'administracion'
    docs_root = Path(settings.BASE_DIR) / "docs" / "_build" / "html"
    if not docs_root.exists():
        raise Http404("La documentación técnica no está generada.")
    normalized_path = path or "index.html"
    return serve(request, normalized_path, document_root=str(docs_root), show_indexes=False)