# Generated by Django 2.1.7 on 2019-03-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunder', '0007_auto_20190320_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(related_name='projects', through='crowdfunder.Tagging', to='crowdfunder.Tag'),
        ),
    ]