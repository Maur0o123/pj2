from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from .views import register, CustomLoginView, CustomLogoutView, save_password_change, password_reset_send
from .views import new_user, save_new_user, manage_users, status_user, edit_user_profile, save_edit_user_profile, edit_my_profile, save_edit_my_profile
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', CustomLoginView.as_view(), name='logincustom'),
    path('logout/', CustomLogoutView.as_view(), name='logoutcustom'),
    path('register',register, name="register" ),
    path('new_user',new_user, name="new_user"),
    path('save_new_user',save_new_user, name="save_new_user"),
    path('manage_users',manage_users, name="manage_users"),
    path('status_user',status_user, name="status_user"),
    path('edit_user_profile',edit_user_profile, name="edit_user_profile"),
    path('save_edit_user_profile',save_edit_user_profile, name="save_edit_user_profile"),
    path('edit_my_profile',edit_my_profile, name="edit_my_profile"),
    path('save_edit_my_profile',save_edit_my_profile, name="save_edit_my_profile"),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"),name='password_change'),
    path('save_password_change',save_password_change, name="save_password_change"),
    path('pasword_reset/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name='password_reset'),
    path('pasword_reset_send',password_reset_send, name="password_reset_send"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name='password_reset_complete'),    
]