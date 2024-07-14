# Generated by Django 4.2.13 on 2024-07-07 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0003_remove_car_id_alter_car_car_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('trip_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=255)),
                ('pick_up_photos', models.JSONField()),
                ('drop_off_photos', models.JSONField(blank=True, null=True)),
                ('pick_up_odometer', models.CharField(max_length=255)),
                ('drop_off_odometer', models.CharField(blank=True, max_length=255, null=True)),
                ('pick_up_time', models.DateTimeField()),
                ('drop_off_time', models.DateTimeField(blank=True, null=True)),
                ('pick_up_location', models.CharField(max_length=255)),
                ('drop_off_location', models.CharField(blank=True, max_length=255, null=True)),
                ('pick_up_note', models.TextField(blank=True, null=True)),
                ('drop_off_note', models.TextField(blank=True, null=True)),
                ('front_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('rear_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('left_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('right_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('odometer_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('optional_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('drop_off_front_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('drop_off_rear_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('drop_off_left_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('drop_off_right_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('drop_off_odometer_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('drop_off_optional_photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('fuel_details', models.JSONField(blank=True, default=list)),
                ('trip_details', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]