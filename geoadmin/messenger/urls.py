from django.urls import path
from . import views

urlpatterns = [
    path('manage_notifications/', views.manage_notifications, name='manage_notifications'),
    path('update_notification_group/', views.update_notification_group, name='update_notification_group'),
]