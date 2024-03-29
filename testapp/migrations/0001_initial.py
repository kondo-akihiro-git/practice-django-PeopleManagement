# Generated by Django 4.2.11 on 2024-03-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('user_name', models.CharField(blank=True, max_length=255)),
                ('mail_address', models.CharField(blank=True, max_length=255)),
                ('password', models.CharField(blank=True, max_length=255)),
                ('picture', models.CharField(blank=True, max_length=255)),
                ('test_empty', models.CharField(blank=True, max_length=255)),
                ('test_flg', models.BooleanField(default=False)),
                ('test_datetime', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField()),
            ],
        ),
    ]
