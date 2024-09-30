# Generated by Django 5.1.1 on 2024-09-20 00:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messanger_app", "0002_customuser_message_delete_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="contacts",
            field=models.ManyToManyField(null=True, to="messanger_app.customuser"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="dob",
            field=models.DateField(null=True),
        ),
    ]
