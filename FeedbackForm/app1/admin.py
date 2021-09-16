from django.contrib import admin
from .models import TempModel


# Register your models here.
# admin.site.register(TempModel)

@admin.register(TempModel)
class TempModel(admin.ModelAdmin):
    list_display = ['question', 'type', 'options']
