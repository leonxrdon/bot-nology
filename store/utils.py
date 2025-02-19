import os
from functools import reduce
from django.db.models import Q
from .models import Product

def search_product(query):
    products = Product.objects.filter(
        Q(product_name__icontains=query) |
        Q(brand__icontains=query) |
        Q(model__icontains=query) |
        Q(product_code__icontains=query) |
        Q(processor__icontains=query) |
        Q(graphics__icontains=query) |
        Q(hard_disk__icontains=query) |
        Q(ram__icontains=query) |
        Q(screen__icontains=query) |
        Q(battery__icontains=query) |
        Q(warranty__icontains=query) |
        Q(so_software__icontains=query) |
        Q(general__icontains=query) |
        Q(connections__icontains=query) |
        Q(audio__icontains=query) |
        Q(webcam__icontains=query) |
        Q(certifications__icontains=query) |
        Q(packing_size__icontains=query) |
        Q(memory_reader__icontains=query) |
        Q(keyboard__icontains=query) |
        Q(optical_driver__icontains=query)
    ).filter(price__isnull=False).distinct()
    
    return products


def search_keywords(keywords):
    keywords = keywords.split()
    for keyword in keywords:
        print("Palabra:", keyword)
        products = Product.objects.filter(
            Q(price__icontains=keyword) |
            Q(product_name__icontains=keyword) |
            Q(brand__icontains=keyword) |
            Q(model__icontains=keyword) |
            Q(product_code__icontains=keyword) |
            Q(processor__icontains=keyword) |
            Q(graphics__icontains=keyword) |
            Q(hard_disk__icontains=keyword) |
            Q(ram__icontains=keyword) |
            Q(screen__icontains=keyword) |
            Q(battery__icontains=keyword) |
            Q(warranty__icontains=keyword) |
            Q(so_software__icontains=keyword) |
            Q(general__icontains=keyword) |
            Q(connections__icontains=keyword) |
            Q(audio__icontains=keyword) |
            Q(webcam__icontains=keyword) |
            Q(certifications__icontains=keyword) |
            Q(packing_size__icontains=keyword) |
            Q(memory_reader__icontains=keyword) |
            Q(keyboard__icontains=keyword) |
            Q(optical_driver__icontains=keyword)
        ).filter(price__isnull=False).distinct()

    print(products)
    return products
