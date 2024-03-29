# Generated by Django 4.2.1 on 2023-06-02 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0020_templates_v1_template_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='templates_v1',
            name='admin_email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='contact_q',
            field=models.CharField(default='Please provide your contact ?', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='email_q',
            field=models.CharField(default='what is your Mail id?', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='first_name_q',
            field=models.CharField(default='what is your First name?', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='last_name_q',
            field=models.CharField(default='what is your Last name?', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='quetion_1_q',
            field=models.CharField(default='question 1', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='quetion_2_q',
            field=models.CharField(default='question 2', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='quetion_3_q',
            field=models.CharField(default='question 3', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='quetion_4_q',
            field=models.CharField(default='question 4', max_length=100),
        ),
        migrations.AddField(
            model_name='templates_v1',
            name='quetion_5_q',
            field=models.CharField(default='question 5', max_length=100),
        ),
    ]
