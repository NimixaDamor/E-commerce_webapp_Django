# Generated by Django 5.0.6 on 2024-08-16 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0021_orderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='page.orderdetail'),
        ),
    ]
