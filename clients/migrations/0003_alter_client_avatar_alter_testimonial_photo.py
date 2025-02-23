# Generated by Django 5.1 on 2024-08-26 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_testimonial_alter_country_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(blank=True, default='images/logo4.PNG', null=True, upload_to='uploads/avatars'),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='photo',
            field=models.ImageField(blank=True, default='images/logo5.PNG', upload_to='uploads/testimony'),
        ),
    ]
