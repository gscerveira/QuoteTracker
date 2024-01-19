# Generated by Django 5.0.1 on 2024-01-18 18:26

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker_app", "0002_alter_store_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("0938b9d5-71b4-4505-b378-0d44fa373cc1"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]