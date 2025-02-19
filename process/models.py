from django.db import models
from django.core.validators import FileExtensionValidator
from .choices import StatusChoices


# Create your models here.
class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
        )
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name

    class Meta:
        verbose_name = "PDF"
        verbose_name_plural = "PDFs"
