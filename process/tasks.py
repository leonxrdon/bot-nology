from celery import shared_task
from botnology.settings import AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY, AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from .gpt import gpt_generative
from store.models import Product
from .utils import save_product
from .models import UploadedPDF, StatusChoices
from .prompt import AIPrompt, AISystem

@shared_task
def process_pdf(file_id):
    try:
        # Obtén el archivo PDF por su ID
        pdf_obj = UploadedPDF.objects.get(id=file_id)
        
        # Actualiza el estado a "PROCESANDO"
        pdf_obj.status = StatusChoices.PROCESSING
        pdf_obj.message = "Procesando PDF..."
        pdf_obj.save()
        print(f"Procesando PDF: {pdf_obj.pdf_file.path}")

        # Credenciales
        endpoint = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
        key = AZURE_DOCUMENT_INTELLIGENCE_KEY
        model_id = AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID
        
        print(f"Endpoint: {endpoint}")
        print(f"Model ID: {model_id}")
        print(f"Key: {key}")
        
        # Inicializar cliente de Azure Document Intelligence
        credential = AzureKeyCredential(key)
        client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)
        
        # Analizar el documento
        with open(pdf_obj.pdf_file.path, "rb") as f:
            poller = client.begin_analyze_document(model_id, document=f)
            result = poller.result()
        
        # Extraer datos del resultado
        data = {}
        for doc in result.documents:  # Itera sobre los documentos extraídos
            for field_name, field_value in doc.fields.items():  # Accede a los campos del documento
                if field_value.value is not None:
                    # quitamos los espacios en blanco al principio y al final y saltos de linea
                    data[field_name] = str(field_value.value).strip()
                else:
                    data[field_name] = None
        
        # Guardar datos en la base de datos usando save_product
        save_product(data)
        
        # Actualiza el estado a "COMPLETADO"
        pdf_obj.status = StatusChoices.COMPLETE
        pdf_obj.message = "Datos guardados en la base de datos."
        pdf_obj.save()
        print("Datos guardados en la base de datos.")

    except UploadedPDF.DoesNotExist:
        # Maneja el caso en el que el archivo PDF no existe
        print(f"No se encontró ningún archivo con el ID: {file_id}")
    
    except Exception as e:
        # Si ocurre cualquier otro error, actualiza el estado a "ERROR"
        print(f"Error al procesar el PDF: {e}")
        try:
            # Intenta actualizar el estado del objeto si existe
            pdf_obj.status = StatusChoices.ERROR
            pdf_obj.message = str(e)
            pdf_obj.save()
        except UnboundLocalError:
            # Si pdf_obj no está definido, simplemente imprime el error
            print(f"No se pudo actualizar el estado del PDF debido a un error previo.")