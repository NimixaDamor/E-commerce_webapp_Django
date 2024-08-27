# Generated by Django 5.0.6 on 2024-08-09 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0008_favourite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
