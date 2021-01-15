# Generated by Django 3.1.2 on 2020-12-07 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201201_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adamay',
            name='projeAdamAy',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.personel', verbose_name='Projede Çalışan Personel'),
        ),
        migrations.AlterField(
            model_name='adamay',
            name='projeKodu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.projects', verbose_name='Proje Kodu'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjeKapsamindaYapilacakFaaliyetler',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Proje Kapsamında Yapılacak Faaliyetler:'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjeKonusu',
            field=models.TextField(max_length=1000, verbose_name='Proje Konusu:'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjeKonusunuBelirleyenIhtiyaclar',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Projenin Konusunu Belirleyen İhtiyaçlar:'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjeOzeti',
            field=models.TextField(max_length=1000, verbose_name='Proje Özeti:'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjeninBeklenenCiktilariFaydalari',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Projenin Beklenen Çıktıları:'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='ProjeninYenilikciYonuArgeNiteligi',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Projenin Yenilikçi Yönü ve AR-GE Niteliği:'),
        ),
    ]