# Generated by Django 3.2.25 on 2025-04-17 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_campschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('units', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('bloodbank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_stock', to='core.bloodbankregistration')),
            ],
            options={
                'unique_together': {('bloodbank', 'blood_group')},
            },
        ),
    ]
