# Generated by Django 3.1.4 on 2024-11-26 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapi', '0003_auto_20220721_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='path',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
