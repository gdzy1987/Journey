# Generated by Django 2.0.4 on 2019-05-31 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0006_auto_20190531_1645'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LdapConfig',
        ),
    ]