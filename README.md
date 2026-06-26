# FloraNativa CL

Plataforma de visualización e identificación de plantas nativas de Chile, con integración de la API de Perenual.

## Stack técnico

- **Backend:** Django 6.0 (FBV)
- **Base de datos:** SQLite
- **Frontend:** Tailwind CSS (CDN)
- **API externa:** Perenual (https://perenual.com/)

## Requisitos

- Python 3.12+
- pip

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd flora_nativa_project

# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py migrate

# Cargar datos de ejemplo (opcional)
python manage.py seed_data

# Iniciar servidor de desarrollo
python manage.py runserver
```

## Variables de entorno

Copiar `.env.example` a `.env` y configurar:

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django |
| `DJANGO_DEBUG` | `True` para desarrollo |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos (separados por coma) |
| `PERENUAL_API_KEY` | API Key de Perenual |
| `DB_PATH` | Ruta de la base de datos SQLite |

## Seed data

Incluye:

- **16 regiones** de Chile con sus números oficiales
- **10 plantas nativas**: Araucaria, Boldo, Quillay, Litre, Copihue, Canelo, Arrayán, Peumo, Espino, Palma Chilena
- **Usuario admin**: `admin` / `admin123`

## Despliegue en Render

1. Conectar repositorio
2. Crear servicio Web con:
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_data`
   - Start command: `gunicorn config.wsgi`
3. Configurar volumen persistente en `/data` y `DB_PATH=/data/db.sqlite3`
4. Agregar `PERENUAL_API_KEY` en Environment Variables

## Tests

```bash
python manage.py test
```

## Rutas

| Ruta | Descripción |
|---|---|
| `/` | Catálogo con filtros |
| `/planta/<id>/` | Detalle de planta |
| `/registro/` | Registro de usuario |
| `/login/` | Inicio de sesión |
| `/logout/` | Cierre de sesión |
| `/admin/` | Panel de administración |
