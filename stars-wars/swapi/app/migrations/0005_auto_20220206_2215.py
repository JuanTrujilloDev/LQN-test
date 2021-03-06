# Generated by Django 2.2.13 on 2022-02-07 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220205_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='eye_color',
            field=models.CharField(blank=True, choices=[('black', 'Black'), ('brown', 'Brown'), ('yellow', 'Yellow'), ('red', 'Red'), ('green', 'Green'), ('purple', 'Purple'), ('unknown', 'Unknown')], default='Unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='people',
            name='hair_color',
            field=models.CharField(blank=True, choices=[('black', 'Black'), ('brown', 'Brown'), ('blond', 'Blond'), ('red', 'Red'), ('white', 'White'), ('bald', 'Bald')], default='bald', max_length=32),
        ),
    ]
