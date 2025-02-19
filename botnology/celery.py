import os
from celery import Celery

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botnology.settings')

# Crear la aplicación Celery
app = Celery('botnology')

# Configurar Celery usando las variables de entorno de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas automáticamente en todas las aplicaciones instaladas
app.autodiscover_tasks()