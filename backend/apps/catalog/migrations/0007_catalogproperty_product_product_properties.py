from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_stockmovement"),
    ]

    operations = [
        migrations.CreateModel(
            name="CatalogProperty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("property_name", models.CharField(max_length=100, unique=True)),
                ("property_values", models.JSONField(blank=True, default=list)),
            ],
            options={
                "verbose_name": "Property",
                "verbose_name_plural": "Properties",
                "db_table": "catalog_properties",
                "ordering": ["property_name"],
            },
        ),
        migrations.AddField(
            model_name="product",
            name="product_properties",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text='Key-value map of dynamic properties, e.g. {"Color": "Red", "Material": "Cotton"}.',
            ),
        ),
    ]
