from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0008_product_has_color_variants_product_is_price_same_colorvariant_productimage_color_variant",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_box_packed",
            field=models.BooleanField(
                default=False,
                help_text='Check for new / box-packed items. Uncheck for used / open-box. Automatically keeps the "Type" property in sync.',
            ),
        ),
    ]
