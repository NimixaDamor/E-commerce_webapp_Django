# Generated by Django 5.0.6 on 2024-08-08 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_additem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additem',
            name='price',
        ),
    ]
