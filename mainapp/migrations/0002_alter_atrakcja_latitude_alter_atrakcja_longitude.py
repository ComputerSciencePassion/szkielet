# Generated by Django 4.1.7 on 2023-06-01 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atrakcja',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='atrakcja',
            name='longitude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
