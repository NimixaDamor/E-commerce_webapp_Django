# Generated by Django 5.0.6 on 2024-08-05 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_additem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.CharField(default='', max_length=50),
        ),
    ]
