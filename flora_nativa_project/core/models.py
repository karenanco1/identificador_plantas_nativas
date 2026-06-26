from django.db import models
from django.contrib.auth.models import User


class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    numero = models.IntegerField(help_text="Número de la región")

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return self.nombre


class Planta(models.Model):
    USOS_CHOICES = [
        ("MED", "Medicinal"),
        ("COM", "Comestible"),
        ("VEN", "Venenosa"),
        ("ORN", "Ornamental"),
        ("IND", "Industrial/Forestal"),
    ]

    nombre_comun = models.CharField(max_length=150)
    nombre_cientifico = models.CharField(max_length=150, unique=True)
    regiones = models.ManyToManyField(Region, related_name="plantas")
    ubicacion_especifica = models.TextField(help_text="Detalles del hábitat chileno")

    descripcion_hoja = models.TextField(blank=True, null=True)
    descripcion_tallo = models.TextField(blank=True, null=True)
    descripcion_flor = models.TextField(blank=True, null=True)
    descripcion_detalle = models.TextField(help_text="Detalles claves de identificación")

    uso_principal = models.CharField(max_length=3, choices=USOS_CHOICES, default="ORN")
    detalles_uso = models.TextField(blank=True, null=True)

    imagen_real = models.ImageField(upload_to="plantas/", blank=True, null=True)

    perenual_id = models.IntegerField(
        blank=True, null=True, help_text="ID de la planta en la API de Perenual"
    )
    riego_frecuencia = models.CharField(
        max_length=100, blank=True, null=True, help_text="Dato obtenido de la API"
    )
    luz_solar = models.CharField(
        max_length=100, blank=True, null=True, help_text="Dato obtenido de la API"
    )

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre_comun"]

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"
