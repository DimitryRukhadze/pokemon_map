# Generated by Django 3.1.14 on 2022-06-12 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_auto_20220611_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
