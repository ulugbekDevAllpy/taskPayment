# Generated by Django 5.1.3 on 2024-11-12 17:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_merchant_is_payment_enabled_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('ab79aa14-0f1e-423f-b272-bb924ae17b7c'), unique=True),
        ),
    ]