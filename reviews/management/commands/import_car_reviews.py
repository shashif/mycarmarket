# ==========================================
# MyCarMarket
# Version: v1.11.1
# File: reviews/management/commands/import_car_reviews.py
# Description:
# Bulk import car reviews from CSV.
# Usage:
# python manage.py import_car_reviews mycarmarket_200_car_reviews.csv
# ==========================================

import csv

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from reviews.models import CarReview


class Command(BaseCommand):
    help = "Import car reviews from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to CSV file"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        try:
            with open(csv_file, newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    title = row.get("title", "").strip()

                    if not title:
                        skipped_count += 1
                        continue

                    slug = row.get("slug", "").strip()

                    if not slug:
                        slug = slugify(title)

                    review, created = CarReview.objects.update_or_create(
                        slug=slug,
                        defaults={
                            "title": title,
                            "make": row.get("make", "").strip(),
                            "model": row.get("model", "").strip(),
                            "year": row.get("year") or None,
                            "body_type": row.get("body_type", "").strip(),
                           
                            "rating": row.get("rating") or 0,
                            "summary": row.get("summary", "").strip(),
                            "pros": row.get("pros", "").strip(),
                            "cons": row.get("cons", "").strip(),
                            "content": row.get("content", "").strip(),
                            "faq": row.get("faq", "").strip(),
                            "meta_title": row.get("meta_title", "").strip(),
                            "meta_description": row.get("meta_description", "").strip(),
                            "is_published": row.get("is_published", "TRUE").upper() == "TRUE",
                            "is_featured": row.get("is_featured", "FALSE").upper() == "TRUE",
                        }
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"CSV file not found: {csv_file}")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Created: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}"
            )
        )