# Generated by Django 4.2.1 on 2023-06-02 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0030_rename_contact_users_bot_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='contact',
            field=models.CharField(default='', max_length=100),
        ),
    ]