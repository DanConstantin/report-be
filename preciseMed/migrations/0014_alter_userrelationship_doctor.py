# Generated by Django 4.2.16 on 2024-10-22 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preciseMed', '0013_alter_userrelationship_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrelationship',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_relationships', to='preciseMed.doctor'),
        ),
    ]
