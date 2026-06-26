# Guía de Despliegue Django + Render
configuración completa para subir un proyecto Django a Render.

---

## 1. Estructura del Proyecto

```
proyecto/
├── core/ # Carpeta de configuración (django-admin startproject)
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── miapp/ # Apps de Django
├── manage.py
├── requirements.txt
├── runtime.txt # Versión de Python
├── build.sh # Script de build
├── Procfile # Comando de inicio
└── .gitignore
```

## 2. Archivos Clave

### requirements.txt
```
django>=5.0,<6.1
whitenoise
gunicorn
requests # Solo si usas APIs externas
```

### runtime.txt
```
python-3.12.1
```

### build.sh
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
# Opcional: python manage.py import_pokemon # Comandos personalizados
```

### Procfile
```
web: gunicorn core.wsgi
```

### core/settings.py — Configuración obligatoria para Render

```python
import os

ALLOWED_HOSTS = [
"localhost",
"127.0.0.1",
"tuapp.onrender.com", # Reemplazar con tu dominio Render
]

MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
"whitenoise.middleware.WhiteNoiseMiddleware", # Justo después de SecurityMiddleware
# ... resto de middleware
]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
"default": {
"BACKEND": "django.core.files.storage.FileSystemStorage",
},
"staticfiles": {
"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
},
}
```

### .gitignore
```
.venv/
*.pyc
__pycache__/
db.sqlite3
*.sqlite3
.env
.env.*
.DS_Store
staticfiles/
```

## 3. Configuración en Render Dashboard

| Campo | Valor |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `./build.sh` |
| **Start Command** | Dejar **vacío** (Render usa el Procfile) |
| **Region** | La más cercana a tus usuarios |

O si no usas Procfile, poner en Start Command:
```
gunicorn core.wsgi
```

## 4. Crear Superuser (Admin)

Una vez desplegada la app, crear un admin desde **Render Dashboard → tu servicio → Shell**:

```shell
python manage.py createsuperuser
```

O de forma automática en cada deploy agregando esto al `build.sh`:
```bash
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell
```
Esto crea el usuario `admin` / `admin123` solo si no existe.

---

## 5. Variables de Entorno (opcional)

En Render Dashboard → Environment Variables:
- `DJANGO_SECRET_KEY` → clave secreta para producción (generar con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DJANGO_DEBUG` → `False`
- `DATABASE_URL` → si usas PostgreSQL

En `settings.py` leerlas así:
```python
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-dev-only")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
```

## 6. Resumen de Comandos Render

| Acción | Comando |
|---|---|
| Build | `./build.sh` |
| Start | `gunicorn core.wsgi` |
| Puerto | Render asigna `$PORT` automáticamente |

## 7. Troubleshooting Común

**Error: `No module named 'app'`**
→ El Start Command apunta a `app.wsgi` pero el proyecto se llama distinto. Usar `gunicorn core.wsgi`.

**Error: `DisallowedHost`**
→ Agregar el dominio Render a `ALLOWED_HOSTS`.

**Error: `No open ports detected`**
→ Asegurar que el servidor bindea a `0.0.0.0:$PORT`. Con Gunicorn + Procfile esto se maneja automáticamente.

**Error: `STATICFILES_STORAGE` no soportado**
→ En Django 5.1+ usar `STORAGES` en vez de `STATICFILES_STORAGE`.

---

*Documento generado para uso como prompt de IA en configuraciones Django + Render.*