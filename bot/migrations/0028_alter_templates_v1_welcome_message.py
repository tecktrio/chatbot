# Generated by Django 4.2.1 on 2023-06-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0027_templates_v1_welcome_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates_v1',
            name='welcome_message',
            field=models.CharField(default='hi', max_length=100),
        ),
    ]
