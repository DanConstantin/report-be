# Generated by Django 4.2.16 on 2024-10-22 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preciseMed', '0012_alter_userrelationship_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrelationship',
            name='doctor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_relationships', to='preciseMed.doctor'),
        ),
        migrations.AlterField(
            model_name='userrelationship',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_relationships', to='preciseMed.patient'),
        ),
    ]
