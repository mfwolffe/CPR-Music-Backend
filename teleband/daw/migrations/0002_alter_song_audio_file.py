# Generated by Django 3.2.11 on 2024-07-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio_file',
            field=models.FileField(blank=True, upload_to='sample_audio/'),
        ),
    ]
