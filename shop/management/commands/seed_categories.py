from django.core.management.base import BaseCommand
from shop.models import Category


class Command(BaseCommand):
    help = "Seed category menu (Giới thiệu, Đồ Nam, Đồ Nữ, Đồng Hồ, Sale)"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Seeding categories...")

        # ===== ROOT CATEGORIES =====
        root_categories = {
            "gioi-thieu": "Giới thiệu",
            "do-nam": "Đồ Nam",
            "do-nu": "Đồ Nữ",
            "dong-ho": "Đồng Hồ",
            "sale": "Sale",
        }

        roots = {}
        for slug, name in root_categories.items():
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "parent": None},
            )
            roots[slug] = cat
            self.stdout.write(f"✅ Root: {name}")

        # ===== CHILD CATEGORIES =====
        children_map = {
            "do-nam": [
                ("ao-nam", "Áo"),
                ("quan-nam", "Quần"),
                ("giay-chay-bo-nam", "Giày chạy bộ"),
                ("giay-dia-hinh-nam", "Giày địa hình"),
            ],
            "do-nu": [
                ("ao-nu", "Áo"),
                ("quan-nu", "Quần"),
                ("giay-chay-bo-nu", "Giày chạy bộ"),
                ("giay-dia-hinh-nu", "Giày địa hình"),
            ],
            "dong-ho": [
                ("suunto", "Suunto"),
                ("garmin", "Garmin"),
                ("coros", "Coros"),
            ],
        }

        for parent_slug, children in children_map.items():
            parent = roots[parent_slug]

            for slug, name in children:
                Category.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "name": name,
                        "parent": parent,
                    },
                )
                self.stdout.write(f"   └─ {parent.name} → {name}")

        self.stdout.write(self.style.SUCCESS("🎉 Seed categories DONE"))
