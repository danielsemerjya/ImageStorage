# Generated by Django 3.2.7 on 2021-09-15 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210915_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='thumbnail200',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='thumbs'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='thumbnail400',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='thumbs'),
        ),
    ]
