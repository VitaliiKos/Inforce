# Generated by Django 5.0.6 on 2024-06-22 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0005_alter_menu_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="date",
            field=models.DateField(default=datetime.date(2024, 6, 22)),
        ),
    ]