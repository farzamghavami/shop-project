# Generated by Django 4.2 on 2025-06-01 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_category_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="wishlist",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
