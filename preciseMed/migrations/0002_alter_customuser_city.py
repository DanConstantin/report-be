# Generated by Django 4.2.16 on 2024-10-07 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preciseMed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
