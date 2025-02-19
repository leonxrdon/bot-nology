import json
from django.http import JsonResponse
from botnology.settings import *
from .utils import search_keywords, search_product

# Import namespaces
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient


def chatbot_response(request):
    if request.method == "POST":
        domain = request.build_absolute_uri("/")[:-1]
        language = request.session.get('language', 'español')
        user_message = request.POST.get("message", "").lower()

        # Buscar productos antes de llamar a GPT

        products = search_product(user_message)
        if products.exists():
            product_links = "\n".join(
                [f"🔗 [{p.product_name}]({domain}/product/{p.id})\n" for p in products[:3]]
            )
            bot_response = f"Aquí tienes algunos productos que podrían interesarte:\n\n{product_links}"
        else:
            print("No se encontraron productos en la base de datos.")
            bot_response = gpt_response(user_message, domain, language)
        return JsonResponse({"response": bot_response})

    return JsonResponse({"error": "Método no permitido"}, status=405)


def detect_intent(intent, domain):
    print("Intento detectar la intención:", intent)
    try:
        ls_prediction_endpoint = LS_CONVERSATIONS_ENDPOINT
        ls_prediction_key = LS_CONVERSATIONS_KEY
        ls_prediction_project_name = LS_CONVERSATIONS_PROJECT_NAME
        ls_deployment_name = LS_DEPLOYMENT_NAME

        client = ConversationAnalysisClient(
            endpoint=ls_prediction_endpoint,
            credential=AzureKeyCredential(ls_prediction_key)
        )

        with client:
            query = intent
            result = client.analyze_conversation(
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "es",
                            "text": query
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {
                        "projectName": ls_prediction_project_name,
                        "deploymentName": ls_deployment_name,
                        "verbose": True
                    }
                }
            )

        top_intent = result["result"]["prediction"]["topIntent"]
        entities = result["result"]["prediction"]["entities"]

        print("Intención detectada:", top_intent)
        print("Entidades detectadas:", entities)

        if top_intent:
            if len(entities) > 0:
                for entity in entities:
                    output_text = gpt_response(f"Procesador {entity['text']}", domain)
                    return output_text

        else:
            print("Intención no reconocida:", top_intent)
            return gpt_response(intent, domain)               

    except Exception as e:
        # Capturar excepciones y devolver un mensaje de error en lugar de None
        error_output = {"error": str(e)}
        return json.dumps(error_output), None  # Retornar el error en formato JSON y None para la intención


def gpt_response(command, domain, language):
    print("Llamando a OpenAI con el comando:", command)
    try:
        # Llamar a GPT primero para analizar la intención del usuario
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            api_version="2024-02-01"
        )
        model = AZURE_OPENAI_MODEL
        gpt_analysis = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un asistente de una tienda en línea. Si un usuario pregunta por productos, devuelve solo palabras clave relevantes de la consulta."},
                {"role": "user", "content": f"Genera una consulta o filtro en Django para buscar productos basados en esta consulta: {command}"}
            ],
            temperature=0,
        )
        query = gpt_analysis.choices[0].message.content.strip()
        products = search_keywords(query)
        if products.exists():
            # Generar enlaces a los productos encontrados
            prompt = ''
            for p in products[:3]:
                prompt += f"""
                    Tienes el producto con esta información:
                    Producto: {p.product_name}
                    Precio: {p.price}
                    Marca: {p.brand}
                    Modelo: {p.model}
                    Precio: {p.price}
                    Procesador: {p.processor}
                    Gráficos: {p.graphics}
                    Disco Duro: {p.hard_disk}
                    RAM: {p.ram}
                    Pantalla: {p.screen}
                    Batería: {p.battery}
                    Garantía: {p.warranty}
                    Sistema Operativo: {p.so_software}
                    General: {p.general}
                    Conexiones: {p.connections}
                    Audio: {p.audio}
                    Webcam: {p.webcam}
                    según las palabras clave: {query} genera un mensaje basado en esta información
                    y luego devuelve la respuesta al usuario. agregando un enlace al producto.
                    Usa esta estructura para el enlace:
                    🔗 [{p.product_name}]({domain}/product/{p.id})
                    si se pone formato en el texto usa con etiquetas html como <strong> o <em> para resaltar la información.
                    También puedes agregar emojis. retorna todo en formato html, o texto plano, usando etiquetas simples, no
                    uses formato markdown. responde en {language} o detecta el idioma del usuario.
                """
            gpt_response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Eres un asistente de una tienda en línea. Si un usuario pregunta por productos y no se encuentran en la base de datos, responde de manera útil."},
                    {"role": "user", "content": f"""
                                        Responde de acuerdo al esta información {prompt}
                                    """}
                ],
                temperature=0,
            )
            return gpt_response.choices[0].message.content
        else:
            response = f"😬 Lo siento, No se encontre información con tu pregunta\n ¿Hay algo más en lo que pueda ayudarte?"
            return response
    except Exception as e:
        print("Error en la llamada a OpenAI:", e)
        return "Lo siento, ocurrió un error al procesar tu solicitud."
