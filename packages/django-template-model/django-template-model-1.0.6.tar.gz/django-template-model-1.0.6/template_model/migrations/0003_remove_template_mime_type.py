# Generated by Django 2.2.4 on 2019-09-16 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template_model', '0002_text_to_file_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='mime_type',
        ),
    ]
