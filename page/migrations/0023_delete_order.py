# Generated by Django 5.0.6 on 2024-08-16 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0022_checkout_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
