from django.urls import path
from . import views, chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.view_store, name='store'),
    path('product/<int:product_id>/', views.view_product, name='product'),
    path('change_language/', views.change_language, name='change_language'),

    # Chatbot
    path('chatbot/', chat.chatbot_response, name='chatbot'),
    path('gpt_response/', chat.gpt_response, name='gpt_response'),
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)