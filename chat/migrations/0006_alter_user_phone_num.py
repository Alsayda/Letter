# Generated by Django 5.1.1 on 2024-09-30 00:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_alter_user_email_alter_user_password_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_num",
            field=models.CharField(default=8253650018, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
