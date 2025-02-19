import json
from django.http import JsonResponse
from botnology.settings import *

# Import namespaces
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
from .prompt import AIPrompt, AISystem

def gpt_generative(prompt, system):
    try:
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            api_version="2024-02-01"
        )
        model = AZURE_OPENAI_MODEL
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        return response.choices[0].message.content

    except Exception as e:
        print("Error en la llamada a OpenAI:", e)
        return "Lo siento, ocurrió un error al procesar tu solicitud."