# Generated by Django 4.0.1 on 2022-03-15 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_dist_app', '0017_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='title',
            field=models.CharField(default='untitled', max_length=30),
        ),
    ]
