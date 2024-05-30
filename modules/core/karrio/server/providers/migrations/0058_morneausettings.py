# Generated by Django 4.2.8 on 2023-12-14 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0057_alter_servicelevel_weight_unit_belgianpostsettings"),
    ]

    operations = [
        migrations.CreateModel(
            name="MorneauSettings",
            fields=[
                (
                    "carrier_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="providers.carrier",
                    ),
                ),
                ("username", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=200)),
                ("billed_id", models.IntegerField(max_length=10)),
                ("division", models.CharField(default="Morneau", max_length=100)),
            ],
            options={
                "verbose_name": "Morneau Settings",
                "verbose_name_plural": "Morneau Settings",
                "db_table": "morneau-settings",
            },
            bases=("providers.carrier",),
        ),
    ]