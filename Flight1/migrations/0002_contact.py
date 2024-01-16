# Generated by Django 4.2.5 on 2023-12-26 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flight1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('number', models.CharField(max_length=12)),
                ('message', models.TextField()),
                ('contact_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]