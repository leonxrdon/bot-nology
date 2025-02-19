import json
import re
from django.contrib import admin
from django.http import HttpResponse
from django.template import Context, Template
# Register your models here.
from .models import Product, Questions
from .choices import FieldChoices


MAX_UTTERANCE_LENGTH = 500

admin.site.site_header = "Botnology Admin"
admin.site.site_title = "Botnology Admin"
admin.site.index_title = "Bienvenido al panel de administración de Botnology"


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('field',)
    search_fields = ('text', 'field')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'price', 'brand', 'model', 'product_name',)
    search_fields = ('product_name', 'brand', 'model', 'product_code', 'processor', 'graphics', 'hard_disk', 'ram', 'screen', 'battery', 'warranty', 'so_software', 'general', 'connections', 'audio', 'webcam', 'certifications', 'packing_size', 'memory_reader', 'keyboard', 'optical_driver')
    list_filter = ('brand',)
    actions = ['export_products', 'generate_clu_json']

    def export_products(self, request, queryset):
        from django.http import HttpResponse
        import csv
        from io import StringIO

        # Crear un archivo CSV en memoria
        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Nombre del producto', 'Precio', 'Marca', 'Modelo', 'Código del producto', 'Procesador', 'Gráficos', 'Disco duro', 'RAM', 'Pantalla', 'Batería', 'Garantía', 'Sistema operativo', 'General', 'Conexiones', 'Audio', 'Webcam', 'Certificaciones', 'Tamaño del embalaje', 'Lector de tarjetas de memoria', 'Teclado', 'Unidad óptica'])
        for product in queryset:
            csv_writer.writerow([product.product_name, product.price, product.brand, product.model, product.product_code, product.processor, product.graphics, product.hard_disk, product.ram, product.screen, product.battery, product.warranty, product.so_software, product.general, product.connections, product.audio, product.webcam, product.certifications, product.packing_size, product.memory_reader, product.keyboard, product.optical_driver])

        # Crear la respuesta HTTP para descargar el archivo CSV
        response = HttpResponse(csv_file.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_export.csv"'
        return response

    export_products.short_description = "Exportar productos a CSV"


    def generate_clu_json(self, request, queryset):
        # Preparamos el JSON base
        json_data = {
            "projectFileVersion": "2024-11-15-preview",
            "stringIndexType": "Utf16CodeUnit",
            "metadata": {
                "projectKind": "Conversation",
                "settings": {
                    "confidenceThreshold": 0,
                    "normalizeCasing": False,
                    "augmentDiacritics": False
                },
                "projectName": "CLU-Botnology",
                "multilingual": True,
                "description": "Proyecto de CLU para productos seleccionados",
                "language": "es"
            },
            "assets": {
                "projectKind": "Conversation",
                "intents": [],
                "entities": [],
                "utterances": []
            }
        }

        # Crear un conjunto de intenciones y de utterances existentes
        unique_intents = set()
        existing_utterances = set()

        # Iteramos sobre los productos seleccionados
        for product in queryset:
            for question in Questions.objects.all():
                question_texts = question.text.splitlines()

                for question_text in question_texts:
                    question_text = question_text.strip()
                    if not question_text:
                        continue

                    question_text = question_text.replace("\n", " ").replace("\r", " ")

                    # Generar el intent como get_{question.field}
                    intent_name = f"get_{question.field}"
                    if intent_name not in unique_intents:
                        json_data["assets"]["intents"].append({"category": intent_name})
                        unique_intents.add(intent_name)

                    field_value = getattr(product, question.field, None)
                    if not field_value or str(field_value).strip() == "":
                        continue

                    template = Template(question_text)
                    context = Context({"product": product})
                    utterance_text = template.render(context).strip()

                    if not utterance_text or utterance_text == "" or utterance_text in existing_utterances:
                        continue

                    # Validar la longitud de la utterance
                    if len(utterance_text) > MAX_UTTERANCE_LENGTH:
                        continue  # Omitimos las utterances demasiado largas

                    # Normalizar el valor eliminando las comas en el campo y en la utterance
                    field_value_str = str(field_value).strip().replace(",", "")
                    utterance_text_normalized = utterance_text.replace(",", "")

                    # Intentar encontrar el offset y la longitud después de normalizar
                    match = re.search(re.escape(field_value_str), utterance_text_normalized)
                    if match:
                        offset = match.start()
                        length = match.end() - match.start()

                        # Crear las entidades solo si el valor se encuentra en el texto
                        entities = [
                            {
                                "category": question.field,
                                "offset": offset,
                                "length": length
                            }
                        ]

                        # Agregar la utterance y las entidades
                        utterance = {
                            "text": utterance_text,
                            "language": "es",
                            "intent": intent_name,
                            "entities": entities,
                            "dataset": "Train"
                        }
                        json_data["assets"]["utterances"].append(utterance)
                        existing_utterances.add(utterance_text)

                        # Verificar si la entidad ya existe en el conjunto de entidades
                        entity_exists = any(entity.get("category") == question.field for entity in json_data["assets"]["entities"])
                        if not entity_exists:
                            print(f"Agregando entidad {question.field}")
                            json_data["assets"]["entities"].append({"category": question.field, "compositionSetting": "combineComponents"})

        response = HttpResponse(
            json.dumps(json_data, ensure_ascii=False, indent=4),
            content_type="application/json"
        )
        response['Content-Disposition'] = 'attachment; filename="clu_botnology.json"'
        return response

    generate_clu_json.short_description = "Generar JSON CLU"
