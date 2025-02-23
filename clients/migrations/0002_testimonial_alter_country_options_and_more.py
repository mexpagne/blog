# Generated by Django 5.1 on 2024-08-25 22:20

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimony', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('testifier', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, default='images/logo3.PNG', upload_to='uploads/testimony')),
                ('occupation', models.CharField(max_length=200)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'countries'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='email',
        ),
        migrations.RemoveField(
            model_name='client',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_name',
        ),
    ]
