# Generated by Django 4.2.1 on 2023-06-02 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0023_alter_templates_v1_contact_alter_templates_v1_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates_v1',
            name='contact',
            field=models.CharField(default='disable', max_length=50),
        ),
        migrations.AlterField(
            model_name='templates_v1',
            name='email',
            field=models.CharField(default='disable', max_length=50),
        ),
        migrations.AlterField(
            model_name='templates_v1',
            name='first_name',
            field=models.CharField(default='disable', max_length=50),
        ),
        migrations.AlterField(
            model_name='templates_v1',
            name='last_name',
            field=models.CharField(default='disable', max_length=50),
        ),
    ]
