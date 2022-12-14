# Generated by Django 3.2.16 on 2022-11-08 15:35

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gemeente",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=255)),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locations.areatype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Wijk",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=255)),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locations.areatype",
                    ),
                ),
                (
                    "gemeente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locations.gemeente",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Buurt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=255)),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="locations.areatype",
                    ),
                ),
                (
                    "wijk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="locations.wijk"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
