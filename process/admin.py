from django.contrib import admin
from django.db.models import Q

# Register your models here.
from .models import UploadedPDF, StatusChoices
from .tasks import process_pdf

@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'pdf_file', 'status', 'message', 'created_at')
    list_filter = ('status',)
    actions = ['process_selected_pdfs']

    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el método save_model para procesar el PDF automáticamente
        después de que se guarda.
        """
        super().save_model(request, obj, form, change)

        if not change:  # Solo procesar si es un nuevo registro
            process_pdf.delay(obj.pk)
            obj.status = StatusChoices.PROCESSING
            obj.message = "Enviado para procesamiento."
            obj.save()

    def process_selected_pdfs(self, request, queryset):
        """
        Acción personalizada para procesar varios PDFs seleccionados.
        """
        for uploaded_pdf in queryset.filter(Q(status=StatusChoices.PENDING) | Q(status=StatusChoices.ERROR)):
            process_pdf.delay(uploaded_pdf.pk)
            uploaded_pdf.status = StatusChoices.PROCESSING
            uploaded_pdf.message = "Enviado para procesamiento."
            uploaded_pdf.save()

        self.message_user(request, f"{queryset.count()} PDF(s) enviados para procesamiento.")

    process_selected_pdfs.short_description = "Procesar PDFs seleccionados"

