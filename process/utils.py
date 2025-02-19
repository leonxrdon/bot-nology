from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from store.models import Product
from django.conf import settings

def save_product(data):
    price = normalize_decimal(data.get('price'))
    product = Product.objects.create(
        price=price,
        product_name=data.get('product_name'),
        brand=data.get('brand'),
        model=data.get('model'),
        product_code=data.get('product_code'),
        processor=data.get('processor'),
        graphics=data.get('graphics'),
        hard_disk=data.get('hard_disk'),
        ram=data.get('ram'),
        screen=data.get('screen'),
        battery=data.get('battery'),
        warranty=data.get('warranty'),
        so_software=data.get('so_software'),
        general=data.get('general'),
        connections=data.get('connections'),
        audio=data.get('audio'),
        webcam=data.get('webcam'),
        certifications=data.get('certifications'),
        packing_size=data.get('packing_size'),
        memory_reader=data.get('memory_reader'),
        keyboard=data.get('keyboard'),
        optical_driver=data.get('optical_driver')
    )
    return product

def normalize_decimal(value):
    if isinstance(value, str):
        normalized_value = value.replace('.', '').replace(',', '.')
        try:
            return float(normalized_value)
        except ValueError:
            return None
    return value