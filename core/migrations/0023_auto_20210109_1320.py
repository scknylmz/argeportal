# Generated by Django 3.1.1 on 2021-01-09 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_personel_expense_center'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personel',
            old_name='expense_center',
            new_name='expensecenter',
        ),
    ]