# Generated by Django 4.0.1 on 2022-03-11 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fairytales", "0011_fairytale_thumbnail"),
    ]

    operations = [
        migrations.AddField(
            model_name="fairytale",
            name="with_flag",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]