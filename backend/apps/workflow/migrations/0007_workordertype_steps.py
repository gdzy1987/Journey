# Generated by Django 2.0.4 on 2019-08-29 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_workorderstep_step_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='workordertype',
            name='steps',
            field=models.TextField(blank=True, verbose_name='步骤配置'),
        ),
    ]