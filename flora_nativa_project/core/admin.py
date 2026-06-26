from django.contrib import admin
from .models import Region, Planta


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["nombre", "numero"]
    search_fields = ["nombre"]


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ["nombre_comun", "nombre_cientifico", "uso_principal", "perenual_id", "fecha_registro"]
    list_filter = ["uso_principal", "regiones"]
    search_fields = ["nombre_comun", "nombre_cientifico"]
    filter_horizontal = ["regiones"]
