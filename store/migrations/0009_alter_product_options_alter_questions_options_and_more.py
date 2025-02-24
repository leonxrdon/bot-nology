# Generated by Django 4.2 on 2025-02-18 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_questions_entidades_remove_questions_intent_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='questions',
            options={'verbose_name': 'Pregunta', 'verbose_name_plural': 'Preguntas'},
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
