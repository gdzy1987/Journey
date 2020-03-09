# Generated by Django 2.0.4 on 2019-12-30 08:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0044_auto_20191230_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('2fce5762-b3b9-46ce-9eb6-b014ff4191ce'), verbose_name='用户jwt加密秘钥'),
        ),
    ]