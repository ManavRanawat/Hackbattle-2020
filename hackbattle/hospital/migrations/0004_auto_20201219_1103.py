# Generated by Django 3.0.5 on 2020-12-19 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_auto_20201219_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciality',
            name='speciality',
            field=models.CharField(choices=[('1', 'Pediatrician'), ('2', 'Cardiologist'), ('3', 'Gynecologist'), ('4', 'Internist'), ('5', 'Dermatologist'), ('6', 'Family Medicine')], default=6, max_length=100),
        ),
    ]