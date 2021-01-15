# Generated by Django 3.1.1 on 2020-12-20 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20201220_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='argetesvik',
            name='ayliktesviktoplam',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Toplam Ar-Ge Teşviği'),
        ),
        migrations.AddField(
            model_name='argetesvik',
            name='ayliktesvikyuzde',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2, verbose_name='Ar-Ge Teşviği Oran'),
        ),
    ]
