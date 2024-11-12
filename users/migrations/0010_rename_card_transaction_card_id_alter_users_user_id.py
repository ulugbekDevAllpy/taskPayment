# Generated by Django 5.1.3 on 2024-11-12 18:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_transaction_card_alter_users_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='card',
            new_name='card_id',
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('e4e96c96-500d-4126-8a65-de6555dfdfa1'), unique=True),
        ),
    ]