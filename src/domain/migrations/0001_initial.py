# Generated by Django 4.2.16 on 2024-11-12 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_message', models.TextField(verbose_name='Origin message')),
                ('message_element', models.CharField(max_length=255, verbose_name='Message element')),
                ('resolution', models.CharField(max_length=50, verbose_name='Resolution')),
                ('found', models.BooleanField(default=False, verbose_name='Found')),
                ('probable', models.BooleanField(default=False, verbose_name='Probable')),
                ('ip', models.GenericIPAddressField(verbose_name='IP address')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['-created_at'],
            },
        ),
    ]