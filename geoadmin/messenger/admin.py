from django.contrib import admin
from .models import NotificationGroup

@admin.register(NotificationGroup)
class NotificationGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    search_fields = ('name', 'slug')
    list_filter = ('category',)
    filter_horizontal = ('users',)
