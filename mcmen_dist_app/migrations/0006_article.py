# Generated by Django 4.0.1 on 2022-02-15 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_dist_app', '0005_remove_truck_drivers_truck_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('text', models.TextField(max_length=500)),
                ('pub_date', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcmen_dist_app.driver')),
            ],
        ),
    ]
