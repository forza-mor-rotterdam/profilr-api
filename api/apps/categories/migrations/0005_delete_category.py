# Generated by Django 3.2.16 on 2023-01-18 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("incidents", "0003_auto_20230118_1546"),
        ("categories", "0004_auto_20230118_1546"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Category",
        ),
    ]