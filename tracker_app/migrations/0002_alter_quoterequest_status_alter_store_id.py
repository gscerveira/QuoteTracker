# Generated by Django 5.0.1 on 2024-01-15 00:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quoterequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("need_to_send", "Need to Send Request"),
                    ("sent", "Request Sent"),
                    ("received", "Quote Received"),
                    ("need_to_resend", "Need to Resend Request"),
                ],
                default="need_to_send",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="store",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("b5f6bf0b-4c95-44d4-9f10-dc720267ae37"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
