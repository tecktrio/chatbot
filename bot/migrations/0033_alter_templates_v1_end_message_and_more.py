# Generated by Django 4.2.1 on 2023-06-02 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0032_remove_users_count_alter_users_bot_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates_v1',
            name='end_message',
            field=models.CharField(default='thank you', max_length=500),
        ),
        migrations.AlterField(
            model_name='templates_v1',
            name='welcome_message',
            field=models.CharField(default='hi', max_length=500),
        ),
    ]
