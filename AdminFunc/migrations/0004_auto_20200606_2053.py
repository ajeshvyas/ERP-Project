# Generated by Django 3.0.5 on 2020-06-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminFunc', '0003_employee_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_details',
            name='created_by',
            field=models.CharField(default='ajesh', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee_details',
            name='address',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='employee_details',
            name='emp_type',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='employee_details',
            name='gender',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='employee_details',
            name='specialization',
            field=models.CharField(max_length=50),
        ),
    ]