# Generated by Django 5.1.1 on 2024-10-08 09:59

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_chatgroup_is_private_chatgroup_members_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatgroup",
            name="group_name",
        ),
        migrations.AddField(
            model_name="chatgroup",
            name="chatGroupId",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="ABCDEF0123456789",
                length=10,
                max_length=21,
                prefix="chatGroup",
                unique=True,
            ),
        ),
    ]
