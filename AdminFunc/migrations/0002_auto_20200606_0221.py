# Generated by Django 3.0.5 on 2020-06-05 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminFunc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_details',
            name='alt_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='father_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='father_no',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='father_occupation',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='gender',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='mother_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='mother_no',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='student_details',
            name='mother_occupation',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]