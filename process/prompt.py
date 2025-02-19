from django.db import models
from store.choices import FieldChoices

class AIPrompt(models.TextChoices):
    EXTRACT_INFO_PRODUCTS = 'EXTRACT_INFO_PRODUCTS', f"""
                            Con esta información, extrae los datos del producto, considerando que tengo estos campos,
                            {', '.join([f'{field[1]}' for field in FieldChoices.choices])}, crea un valor correspondiente para cada campo.
                            """,

class AISystem(models.TextChoices):
    PRODUCT_INFO = 'PRODUCT_INFO', """
                    Pon la información en texto plano y de forma corta y consisa.
                    """,
