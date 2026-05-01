from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from pathlib import Path
from shop.models import Brand

class Command(BaseCommand):
    help = "Seed brands with logos"

    def handle(self, *args, **options):
        brands = [
            ("100Mile", "100mile"),
            ("100Percent", "100percent"),
            ("BlackDiamond", "blackdiamond"),
            ("NITECORE", "nitecore"),
            ("Suunto", "suunto"),
            ("Sis", "sis"),
            ("Soar", "Soar"),
            ("Runderwear", "runderwear"),
        ]

        base_logo_path = Path(settings.BASE_DIR) / "media" / "seed" / "brands"

        for name, slug in brands:
            brand, _ = Brand.objects.get_or_create(
                slug=slug,
                defaults={"name": name},
            )

            logo_path = base_logo_path / f"{slug}.png"
            if logo_path.exists():
                with open(logo_path, "rb") as f:
                    brand.logo.save(f"{slug}.png", File(f), save=True)

            self.stdout.write(self.style.SUCCESS(f"✅ Seeded {name}"))
