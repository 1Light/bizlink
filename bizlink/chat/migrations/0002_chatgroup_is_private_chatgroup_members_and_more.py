# Generated by Django 5.1.1 on 2024-10-07 17:45

import shortuuid.main
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="chatgroup",
            name="is_private",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="chatgroup",
            name="members",
            field=models.ManyToManyField(
                blank=True, related_name="chat_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="chatgroup",
            name="users_online",
            field=models.ManyToManyField(
                blank=True, related_name="online_in_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="chatgroup",
            name="group_name",
            field=models.CharField(
                default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True
            ),
        ),
    ]
