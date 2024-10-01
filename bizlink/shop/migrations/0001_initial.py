# Generated by Django 5.1.1 on 2024-09-29 16:57

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CartOrder",
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
                    "price",
                    models.DecimalField(
                        decimal_places=2, default="1.99", max_digits=15
                    ),
                ),
                ("paid_status", models.BooleanField(default=False)),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                (
                    "product_status",
                    models.CharField(
                        choices=[
                            ("processing", "Processing"),
                            ("shipped", "Shipped"),
                            ("delivered", "Delivered"),
                        ],
                        default="processing",
                        max_length=30,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cart Order",
            },
        ),
        migrations.CreateModel(
            name="CartOrderProduct",
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
                ("invoice_number", models.CharField(max_length=255)),
                ("product_status", models.CharField(max_length=255)),
                ("product", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default="1.99", max_digits=15
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, default="1.99", max_digits=15
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cart Order Products",
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                    "categoryId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=21,
                        prefix="category",
                        unique=True,
                    ),
                ),
                ("name", models.CharField(default="Food", max_length=255)),
                ("description", models.TextField(default="This is a category")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="category.jpg",
                        null=True,
                        upload_to="category_directory_path",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="DiscountedProduct",
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
                    "discountProductId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=27,
                        prefix="discountedProduct",
                        unique=True,
                    ),
                ),
                (
                    "new_price",
                    models.DecimalField(decimal_places=2, default=3.99, max_digits=15),
                ),
                ("discount_until", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Discounted Products",
                "ordering": ("product__name",),
            },
        ),
        migrations.CreateModel(
            name="Feature",
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
                    "featureId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=21,
                        prefix="feature",
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="feature_directory_path"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="FeaturedProduct",
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
                    "featuredProductId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=27,
                        prefix="featuredProduct",
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Featured Products",
                "ordering": ("product__name",),
            },
        ),
        migrations.CreateModel(
            name="MoreProductImage",
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
                    "mpiId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=21,
                        prefix="mpi",
                        unique=True,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="more_product_image.jpg",
                        null=True,
                        upload_to="mpi_directory_path",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "More Product Images",
            },
        ),
        migrations.CreateModel(
            name="MoreProductVideo",
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
                    "mpvId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=21,
                        prefix="mpv",
                        unique=True,
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        default="more_product_video.jpg",
                        null=True,
                        upload_to="mpv_directory_path",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="This is a demo video for the product",
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "More Product Videos",
            },
        ),
        migrations.CreateModel(
            name="NewArrival",
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
                    "newArrivalId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=23,
                        prefix="newArrival",
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "New Arrivals",
                "ordering": ("product__name",),
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                    "productId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=21,
                        prefix="product",
                        unique=True,
                    ),
                ),
                ("name", models.CharField(default="Fresh Pear", max_length=255)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="product.jpg",
                        null=True,
                        upload_to="product_directory_path",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="This is the product", null=True
                    ),
                ),
                ("specifications", models.TextField(blank=True, null=True)),
                (
                    "life",
                    models.CharField(
                        blank=True, default="Not Specified", max_length=255, null=True
                    ),
                ),
                ("mfg", models.DateTimeField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=1.99, max_digits=15),
                ),
                ("stock_quantity", models.PositiveIntegerField(default="5")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product_status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("disabled", "Disabled"),
                            ("rejected", "Rejected"),
                            ("in_review", "In Review"),
                            ("published", "Published"),
                        ],
                        default="in_review",
                        max_length=20,
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("in_stock", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=False)),
                ("digital", models.BooleanField(default=False)),
                (
                    "sku",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="0123456789",
                        length=4,
                        max_length=10,
                        prefix="sku",
                        unique=True,
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ProductReview",
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
                ("review", models.TextField()),
                (
                    "rating",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "★☆☆☆☆"),
                            (2, "★★☆☆☆"),
                            (3, "★★★☆☆"),
                            (4, "★★★★☆"),
                            (5, "★★★★★"),
                        ],
                        default=None,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Product Reviews",
            },
        ),
        migrations.CreateModel(
            name="ProductVideo",
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
                    "description",
                    models.TextField(
                        blank=True,
                        default="This is a demo video for the product",
                        null=True,
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True, null=True, upload_to="product_video_directory_path"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Product Videos",
            },
        ),
        migrations.CreateModel(
            name="Shop",
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
                    "shopId",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="ABCDEF0123456789",
                        length=10,
                        max_length=21,
                        prefix="shop",
                        unique=True,
                    ),
                ),
                ("name", models.CharField(default="Nestify", max_length=255)),
                ("description", models.TextField(default="This is a shop")),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="shop_directory_path"
                    ),
                ),
                ("address", models.TextField(default="This is my address")),
                (
                    "contact",
                    models.CharField(default="+251 97 654 2331", max_length=255),
                ),
                ("chat_resp_time", models.CharField(default="100", max_length=255)),
                ("shipping_on_time", models.CharField(default="100", max_length=255)),
                ("authentic_rating", models.CharField(default="100", max_length=255)),
                ("days_return", models.CharField(default="100", max_length=255)),
                ("warranty_period", models.CharField(default="100", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
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
            ],
        ),
        migrations.CreateModel(
            name="Wishlist",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Wishlists",
            },
        ),
    ]
