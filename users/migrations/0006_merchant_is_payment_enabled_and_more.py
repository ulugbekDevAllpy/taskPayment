# Generated by Django 5.1.3 on 2024-11-12 17:09

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_users_phone_number_alter_users_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='is_payment_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='merchantcategory',
            name='is_payment_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 11, 12, 17, 9, 23, 134049, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('e3134602-aba4-4eb9-b99d-bbd5ab0815ee'), unique=True),
        ),
    ]
