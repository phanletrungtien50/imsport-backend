from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import (
    Brand,
    Category,
    Collection,
    Product,
    ProductVariant,
    ProductType,
    Attribute,
    AttributeValue,
)

class Command(BaseCommand):
    help = "Seed collections = categories (skip first root category)"

    def handle(self, *args, **options):
        self.stdout.write("⏳ Seeding collections by category (skip first root)...")

        # ===== BRAND =====
        brand, _ = Brand.objects.get_or_create(
            slug="imsports",
            defaults={"name": "IMSPORTS"}
        )

        # ===== PRODUCT TYPE =====
        product_type, _ = ProductType.objects.get_or_create(
            slug="ao",
            defaults={"name": "Áo"}
        )

        # ===== ATTRIBUTE SIZE =====
        size_attr, _ = Attribute.objects.get_or_create(
            code="size",
            defaults={"name": "Size"}
        )
        size_m, _ = AttributeValue.objects.get_or_create(
            attribute=size_attr,
            value="M"
        )

        # ===== ROOT CATEGORIES (BỎ CATEGORY ĐẦU) =====
        root_categories = list(
            Category.objects.filter(parent__isnull=True, is_active=True)
            .order_by("order", "id")
        )

        if len(root_categories) <= 1:
            self.stdout.write("⚠️ Không đủ category để seed")
            return

        categories_to_seed = root_categories[1:]

        for order, category in enumerate(categories_to_seed):
            image_path = f"collections/{category.slug}.jpg"

            # ===== COLLECTION = CATEGORY =====
            collection, _ = Collection.objects.get_or_create(
                slug=category.slug,
                defaults={
                    "name": category.name,
                    "order": order,
                    "is_active": True,
                    "image": image_path,   
                }
            )

            # ===== PRODUCTS (6 / CATEGORY) =====
            for i in range(1, 7):
                product_name = f"{category.name} {i}"

                product, created = Product.objects.get_or_create(
                    slug=slugify(product_name),
                    defaults={
                        "name": product_name,
                        "brand": brand,
                        "category": category,
                        "product_type": product_type,
                        "price": 1_200_000 + i * 100_000,
                        "original_price": None,
                        "is_active": True,
                    }
                )

                product.collections.add(collection)

                if created:
                    variant = ProductVariant.objects.create(
                        product=product,
                        sku=f"{product.slug}-M",
                        stock_quantity=20,
                    )
                    variant.attributes.add(size_m)

        self.stdout.write(
            self.style.SUCCESS("✅ Seed collections = categories (skip first) DONE")
        )
