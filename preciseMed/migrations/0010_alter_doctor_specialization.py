# Generated by Django 4.2.16 on 2024-10-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preciseMed', '0009_alter_doctor_options_alter_patient_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(choices=[('MEDICAL', 'Medical'), ('SURGICAL', 'Surgical'), ('RADIATION', 'Radiation'), ('NEURO', 'Neuro')], default='MEDICAL', max_length=50),
        ),
    ]
