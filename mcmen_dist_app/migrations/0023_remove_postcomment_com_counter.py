# Generated by Django 4.0.1 on 2022-05-26 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcmen_dist_app', '0022_remove_article_com_counter_alter_article_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='com_counter',
        ),
    ]
