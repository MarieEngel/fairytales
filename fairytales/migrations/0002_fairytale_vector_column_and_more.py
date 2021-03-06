# Generated by Django 4.0.1 on 2022-02-17 10:14

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fairytales", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fairytale",
            name="vector_column",
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name="fairytale",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["vector_column"], name="fairytales__vector__40665f_gin"
            ),
        ),
    ]
