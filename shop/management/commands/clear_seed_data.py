from django.core.management.base import BaseCommand
from shop.models import (
    ProductVariant,
    Product,
    Collection,
    Category,
    Brand,
)

class Command(BaseCommand):
    help = "Clear old seeded data (products, collections, categories, brands)"

    def handle(self, *args, **options):
        self.stdout.write("⚠️ Clearing old seed data...")

        # XÓA THEO THỨ TỰ FK
        # ProductVariant.objects.all().delete()
        # Product.objects.all().delete()
        Collection.objects.all().delete()

        # ⚠️ Nếu category do seed tạo → xóa
        # Category.objects.all().delete()

        # ⚠️ Nếu brand chỉ có IMSPORTS
        # Brand.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ Old seed data cleared"))
