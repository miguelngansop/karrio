# Generated by Django 4.1.3 on 2022-11-25 17:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0042_auto_20221215_1642"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genericsettings",
            name="account_number",
            field=models.CharField(blank=True, default="", max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="genericsettings",
            name="custom_carrier_name",
            field=models.CharField(
                help_text="Unique carrier slug, lowercase alphanumeric characters and underscores only",
                max_length=30,
                validators=[django.core.validators.RegexValidator("^[a-z0-9_]+$")],
            ),
        ),
        migrations.AlterField(
            model_name="genericsettings",
            name="display_name",
            field=models.CharField(help_text="Carrier display name", max_length=30),
        ),
    ]
