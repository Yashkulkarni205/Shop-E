# Generated by Django 3.1.3 on 2020-11-28 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20201128_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='image',
        ),
    ]
