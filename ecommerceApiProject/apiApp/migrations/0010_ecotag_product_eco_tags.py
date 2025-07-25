# Generated by Django 5.2.4 on 2025-07-08 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0009_wishlist"),
    ]

    operations = [
        migrations.CreateModel(
            name="EcoTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="eco_tags",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="products", to="apiApp.ecotag"
            ),
        ),
    ]
