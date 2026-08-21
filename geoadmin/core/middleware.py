from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse, NoReverseMatch, resolve, Resolver404


class AdminAccessRedirectMiddleware:
    """
    Redirige a los usuarios autenticados sin privilegios de administración fuera de /isamax/.
    """

    admin_prefix = "/isamax/"
    perforista_role = "PERFORISTA"
    perforista_allowed_route_names = {
        "edit_my_profile",
        "save_edit_my_profile",
        "password_change",
        "save_password_change",
        "view_general_mining_documents",
        "view_all_approval_notifications",
        "ajax_list_approval_notifications",
        "view_review_approval_notification",
        "manage_capacitaciones",
        "view_documento",
        "documento_pdf_view",
        "logoutcustom",
    }

    def __init__(self, get_response):
        self.get_response = get_response
        self.perforista_allowed_paths = set()
        for route_name in self.perforista_allowed_route_names:
            try:
                self.perforista_allowed_paths.add(reverse(route_name))
            except NoReverseMatch:
                continue

    def __call__(self, request):
        user = getattr(request, "user", None)

        perfil = getattr(user, 'usuarioprofile', None)
        es_admin_de_seccion = perfil and (
        perfil.seccionAdministracion in ["ADMINISTRADOR", "BASE DATOS"] or 
        perfil.seccionVehicular in ["ADMINISTRADOR", "BASE DATOS", "JEFE MANTENCION", "SUPERVISOR"] or 
        perfil.seccionSondaje in ["ADMINISTRADOR", "BASE DATOS", "JEFE MANTENCION", "SUPERVISOR"] or
        perfil.seccionInventario in ["ADMINISTRADOR", "BASE DATOS"] or
        perfil.seccionPrevencion in ["ADMINISTRADOR", "BASE DATOS", "PREVENCIONISTA", "SUPERVISOR"]
        )

        if (
            request.path.startswith(self.admin_prefix)
            and user
            and user.is_authenticated
            and not (user.is_superuser or es_admin_de_seccion)
        ):
            return redirect("select")

        perfil = getattr(user, 'usuarioprofile', None)
        if user and user.is_authenticated and perfil and perfil.seccionSondaje == self.perforista_role:
            request_path = request.path
            static_url = getattr(settings, "STATIC_URL", "")
            media_url = getattr(settings, "MEDIA_URL", "")

            is_static_or_media = (
                (static_url and request_path.startswith(static_url))
                or (media_url and request_path.startswith(media_url))
            )
            is_allowed_profile_route = request_path in self.perforista_allowed_paths
            is_allowed_named_route = False
            try:
                resolved = resolve(request.path_info)
                is_allowed_named_route = resolved.url_name in self.perforista_allowed_route_names
            except Resolver404:
                is_allowed_named_route = False

            if not is_static_or_media and not is_allowed_profile_route and not is_allowed_named_route:
                return redirect("edit_my_profile")

        return self.get_response(request)
