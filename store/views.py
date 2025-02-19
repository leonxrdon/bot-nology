import json
from django.shortcuts import render
from django.db.models import Min, Max, Q
from .utils import search_product
from .models import Product
from django.http import JsonResponse

# Create your views here.
def view_store(request):
    # Obtener todos los productos con precio no nulo
    products = Product.objects.filter(price__isnull=False).order_by('-pk')
    # Calcular valores mínimo y máximo de precios
    price_min_value = products.aggregate(Min('price'))['price__min']
    price_max_value = products.aggregate(Max('price'))['price__max']

    # Filtrar por parámetros GET (opcional)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    query = request.GET.get('q')
    if query:
        products = search_product(query)
        
    if price_min and price_max:
        products = products.filter(Q(price__gte=price_min) & Q(price__lte=price_max))

    language = request.session.get('language', 'es')
    return render(request, 'store.html', {
        'products': products,
        'price_min': price_min_value,
        'price_max': price_max_value,
        'query': query,
        'language': language,
    })

def view_product(request, product_id):
    language = request.session.get('language', 'es')
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {
        'product': product,
        'language': language,
    })


def change_language(request):
    if request.method == "POST":
        # Obtener el idioma desde la solicitud JSON
        data = json.loads(request.body)
        language = data.get('language', 'es')  # Si no se especifica idioma, por defecto 'es'

        # Guardar el idioma en la sesión
        request.session['language'] = language

        # Responder con un JSON indicando el idioma cambiado
        return JsonResponse({"language": language})

    return JsonResponse({"error": "Método no permitido"}, status=405)
