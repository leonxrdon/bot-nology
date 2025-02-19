from django.db import models
from .choices import FieldChoices
# Create your models here.

class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Nombre del producto")
    brand = models.TextField(null=True, blank=True, verbose_name="Marca")
    model = models.TextField(null=True, blank=True, verbose_name="Modelo")
    product_code = models.TextField(null=True, blank=True, verbose_name="Código del producto")
    processor = models.TextField(null=True, blank=True, verbose_name="Procesador")
    graphics = models.TextField(null=True, blank=True, verbose_name="Gráficos")
    hard_disk = models.TextField(null=True, blank=True, verbose_name="Disco duro")
    ram = models.TextField(null=True, blank=True, verbose_name="RAM")
    screen = models.TextField(null=True, blank=True, verbose_name="Pantalla")
    battery = models.TextField(null=True, blank=True, verbose_name="Batería")
    warranty = models.TextField(null=True, blank=True, verbose_name="Garantía")
    so_software = models.TextField(null=True, blank=True, verbose_name="Sistema operativo")
    general = models.TextField(null=True, blank=True, verbose_name="General")
    connections = models.TextField(null=True, blank=True, verbose_name="Conexiones")
    audio = models.TextField(null=True, blank=True, verbose_name="Audio")
    webcam = models.TextField(null=True, blank=True, verbose_name="Webcam")
    certifications = models.TextField(null=True, blank=True, verbose_name="Certificaciones")
    packing_size = models.TextField(null=True, blank=True, verbose_name="Tamaño del embalaje")
    memory_reader = models.TextField(null=True, blank=True, verbose_name="Lector de tarjetas de memoria")
    keyboard = models.TextField(null=True, blank=True, verbose_name="Teclado")
    optical_driver = models.TextField(null=True, blank=True, verbose_name="Unidad óptica")

    description = models.TextField(null=True, blank=True)
    # opcional
    image = models.ImageField(upload_to="products", null=True, blank=True)

    def __str__(self):
        return self.product_name or "Sin nombre"


    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Questions(models.Model):
    text = models.TextField()
    field = models.CharField(max_length=255, choices=FieldChoices.choices, default=FieldChoices.GENERAL)
    
    def __str__(self):
        return self.field

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"