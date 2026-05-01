from django.core.management.base import BaseCommand
from shop.models import Product, ProductVariant, ProductImage, Category, Brand
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Seed 5 NEW products and 5 SALE products"

    def handle(self, *args, **kwargs):
        brand, _ = Brand.objects.get_or_create(
            name="IMS",
            slug="ims"
        )

        category, _ = Category.objects.get_or_create(
            name="Đồ Nam",
            slug="do-nam",
            parent=None
        )

        # ===== 5 SẢN PHẨM NEW =====
        for i in range(1, 6):
            product = Product.objects.create(
                name=f"Áo chạy bộ NEW {i}",
                slug=f"ao-chay-bo-new-{i}",
                brand=brand,
                category=category,
                description="Áo chạy bộ cao cấp, thoáng khí",
                price=1_200_000,
                original_price=None,
                is_active=True,
            )

            ProductVariant.objects.create(
                product=product,
                sku=f"NEW-{i}-M",
                size="M",
                stock_quantity=20,
            )

            ProductImage.objects.create(
                product=product,
                image=ContentFile(b"", name=f"new_{i}.jpg"),
                alt_text=product.name,
            )

        # ===== 5 SẢN PHẨM SALE =====
        for i in range(1, 6):
            product = Product.objects.create(
                name=f"Áo chạy bộ SALE {i}",
                slug=f"ao-chay-bo-sale-{i}",
                brand=brand,
                category=category,
                description="Áo chạy bộ giảm giá đặc biệt",
                original_price=1_500_000,
                price=990_000,
                is_active=True,
            )

            ProductVariant.objects.create(
                product=product,
                sku=f"SALE-{i}-M",
                size="M",
                stock_quantity=15,
            )

            ProductImage.objects.create(
                product=product,
                image=ContentFile(b"", name=f"sale_{i}.jpg"),
                alt_text=product.name,
            )

        self.stdout.write(self.style.SUCCESS("✅ Seeded 5 NEW + 5 SALE products"))
