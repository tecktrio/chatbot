# Generated by Django 4.2.1 on 2023-06-01 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0018_templates_v1_admin_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templates_v1',
            name='admin_email',
        ),
        migrations.RemoveField(
            model_name='templates_v1',
            name='bot_number',
        ),
    ]