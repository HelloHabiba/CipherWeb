# Generated by Django 4.2.5 on 2023-12-05 00:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spaces", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="files/"),
        ),
    ]
