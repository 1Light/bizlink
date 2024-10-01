# Generated by Django 5.1.1 on 2024-10-01 11:25

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("userauth", "0002_notification"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={"verbose_name_plural": "Notifications"},
        ),
        migrations.AddField(
            model_name="notification",
            name="notificationId",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="ABCDEF0123456789",
                length=10,
                max_length=25,
                prefix="notification",
            ),
        ),
    ]
