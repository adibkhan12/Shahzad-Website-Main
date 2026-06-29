import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_catalogproperty_product_product_properties"),
    ]

    operations = [
        # New boolean flags on Product
        migrations.AddField(
            model_name="product",
            name="has_color_variants",
            field=models.BooleanField(
                default=False,
                help_text="Enable per-color image sets and optional per-color pricing.",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="is_price_same",
            field=models.BooleanField(
                default=True,
                help_text="When color variants are on, uncheck this to give each color its own price.",
            ),
        ),
        # New ColorVariant table
        migrations.CreateModel(
            name="ColorVariant",
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
                (
                    "color_name",
                    models.CharField(
                        max_length=100,
                        help_text="Color label or hex code, e.g. Red or #FF0000.",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Leave blank to inherit the product's main price.",
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="color_variants_data",
                        to="catalog.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Color Variant",
                "verbose_name_plural": "Color Variants",
                "ordering": ["order", "color_name"],
            },
        ),
        # FK from ProductImage → ColorVariant (nullable)
        migrations.AddField(
            model_name="productimage",
            name="color_variant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="catalog.colorvariant",
                verbose_name="Color variant",
            ),
        ),
    ]
