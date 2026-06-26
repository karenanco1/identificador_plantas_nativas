# Product Requirement Document (PRD) - v2
## Proyecto: FloraNativa CL – Plataforma de Visualización e Identificación (Integración Perenual API)

### 1. Visión General del Proyecto
**FloraNativa CL** es una aplicación web diseñada para catalogar, visualizar y aprender sobre las plantas nativas de Chile, organizadas por su distribución geográfica (regiones y ubicaciones específicas). El sistema servirá como base de conocimiento estructurada (características morfológicas y usos). En esta versión, el sistema integra la API externa de **Perenual (https://perenual.com/)** para enriquecer la base de datos local con guías de cuidado, datos botánicos globales e imágenes complementarias, manteniendo el objetivo a largo plazo de construir un identificador de plantas propio mediante Machine Learning.

---

### 2. Objetivos del Sistema
* **Catalogación Precisa y Enriquecida:** Permitir el registro de plantas locales integrando datos globales y guías de cuidado automatizadas a través de la API de Perenual.
* **Filtro Geográfico:** Facilitar a los usuarios la búsqueda de plantas según la región de Chile en la que se encuentran.
* **Autenticación Base:** Controlar el acceso mediante un sistema robusto de usuarios (Registro, Login, Logout) para proteger la gestión de datos.
* **Simplicidad Técnica:** Mantener un stack ligero (Django 6.0 + SQLite) fácil de desplegar en entornos como **Render**.

---

### 3. Arquitectura y Stack Técnico
* **Backend:** Django 6.0 (utilizando Vistas Basadas en Funciones - FBV) con la librería `requests` para el consumo de APIs REST.
* **Base de Datos:** SQLite (mapeada localmente para facilitar el despliegue directo).
* **API Externa:** Perenual API (https://perenual.com/) para búsqueda de especies y sincronización de datos botánicos.
* **Frontend:** HTML5 + Django Templates + **Tailwind CSS (vía CDN)**.
* **Despliegue:** Render (Configurado con `WhiteNoise` y volumen persistente para SQLite).

---

### 4. Requerimientos Funcionales

#### RF-01: Gestión de Usuarios (Autenticación)
* **Registro:** Formulario para nuevos usuarios (Username, Email, Password).
* **Login:** Acceso para usuarios registrados.
* **Logout:** Cierre de sesión seguro.

#### RF-02: Catálogo de Plantas e Integración de API
Cada planta debe registrar obligatoriamente en base de datos o consultar dinámicamente:
* **Identificación:** Nombre común y Nombre científico (llave de cruce con la API).
* **Ubicación Local:** Región(es) de Chile y hábitat/ubicación específica.
* **Morfología (Detalles de Identificación):** Descripción técnica de hojas, tallo, flores, frutos y raíces.
* **Usos Comunes:** Clasificación taggeada (Medicinal, Comestible, Venenosa, Ornamental, Industrial/Forestal).
* **Datos Enriquecidos (Perenual API):** Frecuencia de riego, necesidades de luz solar, ciclo de vida e ID de referencia externa de Perenual para sincronización.

#### RF-03: Visualización y Filtros
* Vista de catálogo o listado filtrable por **Región**.
* Buscador por nombre común o científico con fallback de búsqueda en tiempo real en la API de Perenual si la planta no existe localmente.

---

### 5. Estructura de Datos (Modelos de Django)

Se actualiza `models.py` para incluir el campo de referencia a Perenual:

```python
from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    numero = models.IntegerField(help_text="Número de la región")

    def __str__(self):
        return self.nombre

class Planta(models.Model):
    USOS_CHOICES = [
        ('MED', 'Medicinal'),
        ('COM', 'Comestible'),
        ('VEN', 'Venenosa'),
        ('ORN', 'Ornamental'),
        ('IND', 'Industrial/Forestal'),
    ]

    nombre_comun = models.CharField(max_length=150)
    nombre_cientifico = models.CharField(max_length=150, unique=True)
    regiones = models.ManyToManyField(Region, related_name="plantas")
    ubicacion_especifica = models.TextField(help_text="Detalles del hábitat chileno")
    
    # Morfología local para Identificación
    descripcion_hoja = models.TextField(blank=True, null=True)
    descripcion_tallo = models.TextField(blank=True, null=True)
    descripcion_flor = models.TextField(blank=True, null=True)
    descripcion_detalle = models.TextField(help_text="Detalles claves de identificación")
    
    # Usos
    uso_principal = models.CharField(max_length=3, choices=USOS_CHOICES, default='ORN')
    detalles_uso = models.TextField(blank=True, null=True)
    
    # Imagen local / Fallback
    imagen_real = models.ImageField(upload_to='plantas/', blank=True, null=True)
    
    # Integración Perenual API (https://perenual.com/)
    perenual_id = models.IntegerField(blank=True, null=True, help_text="ID de la planta en la API de Perenual")
    riego_frecuencia = models.CharField(max_length=100, blank=True, null=True, help_text="Dato obtenido de la API")
    luz_solar = models.CharField(max_length=100, blank=True, null=True, help_text="Dato obtenido de la API")

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"
```

---

### 6. Estructura del Proyecto y Enrutamiento (URLs y Views)

#### Estructura de Carpetas Recomendada:
```text
flora_nativa_project/
│
├── core/                  # Aplicación principal
│   ├── templates/
│   │   ├── base.html      # Tailwind CDN
│   │   ├── index.html
│   │   ├── detalle.html   # Muestra datos locales + Perenual API
│   │   ├── login.html
│   │   └── registro.html
│   ├── models.py
│   ├── urls.py
│   └── views.py           # FBV con lógica de requests API
│
├── docs/                  # Documentación
│   ├── prd.md             # Este documento (v2)
│   ├── progreso.md        # Registro de avances
│   └── futuras_impl.md    # Notas sobre el Identificador ML
│
├── manage.py
├── requirements.txt       # Incluir 'requests' y 'requests-cache' (opcional)
└── static/
```

#### Enrutamiento (`urls.py`):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('planta/<int:pk>/', views.detalle_planta, name='detalle_planta'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]
```

#### Lógica de Control (`views.py`) con Consumo de API:
```python
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Planta, Region

PERENUAL_API_KEY = "TU_API_KEY_AQUI" # Idealmente usar python-dotenv en Render

def home(request):
    region_id = request.GET.get('region')
    query = request.GET.get('q')
    
    plantas = Planta.objects.all()
    if region_id:
        plantas = plantas.filter(regiones__id=region_id)
    if query:
        plantas = plantas.filter(nombre_comun__icontains=query) | plantas.filter(nombre_cientifico__icontains=query)
    
    regiones = Region.objects.all()
    return render(request, 'index.html', {'plantas': plantas, 'regiones': regiones, 'query': query})

def detalle_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk)
    api_data = None

    # Si la planta cuenta con una referencia o queremos buscarla en perenual.com por su nombre científico
    if planta.perenual_id or planta.nombre_cientifico:
        try:
            # Opción A: Buscar por ID asignado
            if planta.perenual_id:
                url = f"https://perenual.com/api/species/details/{planta.perenual_id}?key={PERENUAL_API_KEY}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    api_data = response.json()
            # Opción B: Si no tiene ID, buscar por nombre científico para sincronizarlo
            else:
                search_url = f"https://perenual.com/api/species-list?key={PERENUAL_API_KEY}&q={planta.nombre_cientifico}"
                res = requests.get(search_url, timeout=5)
                if res.status_code == 200 and res.json().get('data'):
                    first_match = res.json()['data'][0]
                    # Guardamos el ID para futuras consultas más rápidas
                    planta.perenual_id = first_match.get('id')
                    planta.save()
                    
                    # Traer los detalles completos
                    detail_url = f"https://perenual.com/api/species/details/{planta.perenual_id}?key={PERENUAL_API_KEY}"
                    api_data = requests.get(detail_url, timeout=5).json()
        except requests.exceptions.RequestException:
            api_data = {"error": "No se pudo conectar con la API de Perenual en este momento."}

    return render(request, 'detalle.html', {'planta': planta, 'api_data': api_data})

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('home')
```

---

### 7. Estrategia de Despliegue (Render + SQLite)
1. **Variables de Entorno:** Configurar la clave de Perenual (`PERENUAL_API_KEY`) directamente en la sección "Environment" de Render.
2. **Caché en Consultas a la API:** Para optimizar las llamadas y evitar sobrepasar los límites de la API gratuita de Perenual, se recomienda implementar una capa de caché en Django para las respuestas HTTP del endpoint de detalles.
3. **Persistencia de Base de Datos:** Configurar el volumen persistente en Render (`/data`) y cambiar la ruta de `db.sqlite3` en `settings.py` a `/data/db.sqlite3`.

---

### 8. Próximas Implementaciones (Roadmap en `docs/futuras_impl.md`)
* **Sincronización Asíncrona (Celery/Cron):** Crear un comando de Django que actualice semanalmente los datos de riego y sol de las plantas registradas consumiendo la API de Perenual de fondo.
* **Identificador de Plantas por Imagen:** Integrar el endpoint de identificación por visión computacional (si es soportado por Perenual en sus planes avanzados o mediante un modelo propio de TensorFlow), enviando la imagen cargada por el usuario desde el ecosistema web.
