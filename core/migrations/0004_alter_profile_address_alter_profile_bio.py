# Generated by Django 4.1.3 on 2022-11-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
