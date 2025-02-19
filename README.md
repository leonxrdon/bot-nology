# Botnology: Catalogo de Productos con Chatbot y Azure Document Intelligence
![BotNology](https://github.com/user-attachments/assets/8ab2201c-dd47-4971-95d1-9936d2e80278)


**Botnology** es un proyecto que permite gestionar un catálogo de productos en formato PDF y consultarlos a través de un chatbot que utiliza GPT-4o mini de Azure OpenAI. El sistema utiliza Azure Document Intelligence para extraer la información relevante de los archivos PDF y almacenarla en una base de datos para su posterior consulta y gestión.

## Descripción

El sistema se divide en dos partes principales:

1. **Azure Document Intelligence**:
   - Se entrena un modelo en Azure para extraer y reconocer información dentro de los archivos PDF cargados. Esta información se extrae y se almacena en la base de datos para su consulta posterior.

2. **Aplicación Django**:
   - El proyecto está implementado en Django con un template de eCommerce que permite ver la información de los productos.
   - Se integra la SDK de Azure Document Intelligence para extraer la información de los nuevos archivos PDF y almacenarla en una base de datos.
   - Se utiliza un chatbot que permite hacer consultas a la base de datos utilizando el modelo `gpt-4o-mini` de Azure OpenAI para proporcionar respuestas interactivas y estructuradas con enlaces que dirigen a información detallada de los productos.
   
Adicionalmente, se usa **Celery** para gestionar las tareas de carga de archivos PDF y extracción de la información de forma asíncrona, evitando sobrecargar el sistema.

## Requisitos

- **Python 3.x**
- **Django 4.2**
- **Celery**
- **Azure SDKs**:
  - Azure Document Intelligence
  - Azure OpenAI

## Instalación

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/leonxrdon/botnology
   cd botnology
   ```
## Instalación

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone <repositorio_url>
   cd <nombre_del_directorio>
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea el archivo `.env` con las siguientes variables y completa la información correspondiente de Azure:

   ```bash
   SECRET_KEY='django-insecure-!d3yz0a6fw0iwm0@-5ufi(&sshq&y#3%n6l*!ma7*vjz%xyvut'

   # Azure
   AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=''
   AZURE_DOCUMENT_INTELLIGENCE_KEY=''
   AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID=""

   AZURE_OPENAI_ENDPOINT=''
   AZURE_OPENAI_KEY=''
   AZURE_OPENAI_MODEL='gpt-4o-mini'
   ```
Asegúrate de completar los campos con la información proporcionada por Azure para los servicios de Document Intelligence y OpenAI.

5. Realiza las migraciones de la base de datos:

   ```bash
   python manage.py migrate
   ```

6. Para ejecutar el proyecto en desarrollo:

   ```bash
   python manage.py runserver
   ```
7. Asegurate de ejecutar las tareas de celery para que funcione la carga de productos a partir de PDFs.
    ```bash
    celery -A botnology worker --beat
    ```

## Uso

1. **Carga de Productos**: 
   Desde el panel de administración de Django, puedes cargar archivos PDF con la información de los productos. El sistema utilizará la SDK de Azure Document Intelligence para extraer la información y almacenarla en la base de datos.

2. **Consultas mediante el Chatbot**:
   Los usuarios pueden interactuar con el chatbot para realizar consultas sobre los productos almacenados. El chatbot utilizará el modelo `gpt-4o-mini` para ofrecer respuestas interactivas con enlaces a la información detallada de cada producto.
