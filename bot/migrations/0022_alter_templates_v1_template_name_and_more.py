# Generated by Django 4.2.1 on 2023-06-02 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0021_templates_v1_admin_email_templates_v1_contact_q_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates_v1',
            name='template_name',
            field=models.CharField(default='new template', max_length=100),
        ),
        migrations.AlterField(
            model_name='templates_v1',
            name='template_status',
            field=models.CharField(default='disable', max_length=100),
        ),
    ]
