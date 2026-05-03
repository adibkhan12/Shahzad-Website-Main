"""
One-off import from the legacy Prisma-managed Postgres DB into Django models.

Usage:
    # Put LEGACY_DATABASE_URL=postgres://user:pass@host:5432/dbname in .env first
    python manage.py import_from_prisma
    python manage.py import_from_prisma --truncate   # wipe Django tables first
    python manage.py import_from_prisma --only=products,orders

Safe to re-run: uses update_or_create keyed on title/name/id.
"""

from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

try:
    import psycopg
except ImportError:  # pragma: no cover
    psycopg = None


TABLES_ORDER = [
    "users",
    "categories",
    "products",
    "adbanners",
    "settings",
    "reviews",
    "qas",
    "wished",
]


class Command(BaseCommand):
    help = "Import rows from the legacy Prisma-managed Postgres database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--truncate", action="store_true", help="Wipe target Django tables first"
        )
        parser.add_argument(
            "--only", default="", help="Comma-separated subset of: " + ",".join(TABLES_ORDER)
        )
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        if not psycopg:
            raise CommandError(
                "psycopg is not installed (it is in requirements.txt — run pip install)."
            )

        url = getattr(settings, "LEGACY_DATABASE_URL", "")
        if not url:
            raise CommandError(
                "LEGACY_DATABASE_URL is empty. Set it in .env to the old Postgres URL and re-run."
            )

        only = {x.strip() for x in opts["only"].split(",") if x.strip()} or set(TABLES_ORDER)
        dry = opts["dry_run"]

        self.stdout.write("Connecting to legacy DB…")
        with psycopg.connect(url, autocommit=False) as conn, conn.cursor() as cur:
            self._introspect(cur)

            if opts["truncate"] and not dry:
                self._truncate()

            if "users" in only:
                self._copy_users(cur, dry)
            if "categories" in only:
                self._copy_categories(cur, dry)
            if "products" in only:
                self._copy_products(cur, dry)
            if "adbanners" in only:
                self._copy_adbanners(cur, dry)
            if "settings" in only:
                self._copy_settings(cur, dry)
            if "reviews" in only:
                self._copy_reviews(cur, dry)
            if "qas" in only:
                self._copy_qas(cur, dry)
            if "wished" in only:
                self._copy_wishlist(cur, dry)

        self.stdout.write(self.style.SUCCESS("Import complete."))

    # ---- helpers ----
    def _introspect(self, cur):
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [r[0] for r in cur.fetchall()]
        self.stdout.write("Tables found: " + ", ".join(tables))
        self._tables = set(tables)

    def _has(self, *names):
        return any(n in self._tables for n in names)

    def _fetch(self, cur, sql):
        cur.execute(sql)
        cols = [d.name for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def _truncate(self):
        from apps.accounts.models import User
        from apps.catalog.models import QA, AdBanner, Category, Product, Review, Setting
        from apps.wishlist.models import WishedProduct

        WishedProduct.objects.all().delete()
        QA.objects.all().delete()
        Review.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        AdBanner.objects.all().delete()
        Setting.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.WARNING("Truncated Django tables."))

    # ---- per-entity ----
    @transaction.atomic
    def _copy_users(self, cur, dry):
        if not self._has("User", "users"):
            return
        table = "User" if "User" in self._tables else "users"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] users: {len(rows)}")
            return
        from apps.accounts.models import User

        for r in rows:
            email = r.get("email")
            if not email:
                continue
            defaults = {
                "username": email,
                "referral_source": r.get("referralSource") or r.get("referral_source") or "",
                "referral_other": r.get("referralOther") or r.get("referral_other") or "",
                "is_active": True,
            }
            user, created = User.objects.update_or_create(email=email, defaults=defaults)
            # Preserve bcrypt hash so users can keep logging in
            pw = r.get("password")
            if pw and created:
                user.password = f"bcrypt${pw}" if not pw.startswith(("bcrypt$", "pbkdf2_")) else pw
                user.save(update_fields=["password"])
        self.stdout.write(f"users: {len(rows)}")

    @transaction.atomic
    def _copy_categories(self, cur, dry):
        if not self._has("Category", "categories"):
            return
        table = "Category" if "Category" in self._tables else "categories"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] categories: {len(rows)}")
            return
        from apps.catalog.models import Category

        id_map = {}
        for r in rows:
            cat, _ = Category.objects.update_or_create(
                name=r["name"],
                defaults={"properties": r.get("properties") or []},
            )
            id_map[r["id"]] = cat
        # wire up parents
        for r in rows:
            parent_id = r.get("parentId") or r.get("parent_id")
            if parent_id and parent_id in id_map:
                cat = id_map[r["id"]]
                cat.parent = id_map[parent_id]
                cat.save(update_fields=["parent"])
        self.stdout.write(f"categories: {len(rows)}")
        self._cat_map = id_map

    @transaction.atomic
    def _copy_products(self, cur, dry):
        if not self._has("Product", "products"):
            return
        table = "Product" if "Product" in self._tables else "products"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] products: {len(rows)}")
            return
        from apps.catalog.models import Category, Product

        cat_map = getattr(self, "_cat_map", {c.id: c for c in Category.objects.all()})
        for r in rows:
            cat = cat_map.get(r.get("categoryId") or r.get("category_id"))
            props = r.get("properties") or {}
            brand = ""
            if isinstance(props, dict):
                brand = props.get("Brand", "") or props.get("brand", "")
            Product.objects.update_or_create(
                title=r["title"],
                defaults={
                    "description": r.get("description") or "",
                    "price": Decimal(str(r.get("price") or 0)),
                    "images": r.get("images") or [],
                    "stock": r.get("stock") or 0,
                    "color_variants": r.get("colorVariants") or r.get("color_variants") or [],
                    "properties": props,
                    "brand": brand,
                    "category": cat,
                },
            )
        self.stdout.write(f"products: {len(rows)}")

    @transaction.atomic
    def _copy_adbanners(self, cur, dry):
        if not self._has("AdBanner", "adbanners"):
            return
        table = "AdBanner" if "AdBanner" in self._tables else "adbanners"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] adbanners: {len(rows)}")
            return
        from apps.catalog.models import AdBanner

        for r in rows:
            AdBanner.objects.update_or_create(
                title=r["title"],
                defaults={
                    "desc": r.get("desc") or "",
                    "image": r.get("image") or "",
                    "button": r.get("button") or "",
                    "link": r.get("link") or "",
                    "bg": r.get("bg") or "#740DC2",
                    "order": r.get("order") or 0,
                },
            )
        self.stdout.write(f"adbanners: {len(rows)}")

    @transaction.atomic
    def _copy_settings(self, cur, dry):
        if not self._has("Setting", "settings"):
            return
        table = "Setting" if "Setting" in self._tables else "settings"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] settings: {len(rows)}")
            return
        from apps.catalog.models import Setting

        for r in rows:
            Setting.objects.update_or_create(
                name=r["name"], defaults={"value": r.get("value") or {}}
            )
        self.stdout.write(f"settings: {len(rows)}")

    @transaction.atomic
    def _copy_reviews(self, cur, dry):
        if not self._has("Review", "reviews"):
            return
        table = "Review" if "Review" in self._tables else "reviews"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] reviews: {len(rows)}")
            return
        from apps.catalog.models import Product, Review

        products = {p.id: p for p in Product.objects.all()}
        created = 0
        for r in rows:
            pid = r.get("productId") or r.get("product_id")
            if pid not in products:
                continue
            Review.objects.create(
                product=products[pid],
                user=r.get("user") or "",
                rating=r.get("rating") or 5,
                text=r.get("text") or "",
                images=r.get("images") or [],
            )
            created += 1
        self.stdout.write(f"reviews: {created}")

    @transaction.atomic
    def _copy_qas(self, cur, dry):
        if not self._has("QA", "qas"):
            return
        table = "QA" if "QA" in self._tables else "qas"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] qas: {len(rows)}")
            return
        from apps.catalog.models import QA, Product

        products = {p.id: p for p in Product.objects.all()}
        created = 0
        for r in rows:
            pid = r.get("productId") or r.get("product_id")
            if pid not in products:
                continue
            QA.objects.create(
                product=products[pid],
                user=r.get("user") or "",
                question=r.get("question") or "",
                answer=r.get("answer") or "",
                answered_at=r.get("answeredAt") or r.get("answered_at"),
            )
            created += 1
        self.stdout.write(f"qas: {created}")

    @transaction.atomic
    def _copy_wishlist(self, cur, dry):
        if not self._has("WishedProduct", "wished_products"):
            return
        table = "WishedProduct" if "WishedProduct" in self._tables else "wished_products"
        rows = self._fetch(cur, f'SELECT * FROM "{table}"')
        if dry:
            self.stdout.write(f"[dry] wished: {len(rows)}")
            return
        from apps.accounts.models import User
        from apps.catalog.models import Product
        from apps.wishlist.models import WishedProduct

        users_by_email = {u.email: u for u in User.objects.all()}
        products = {p.id: p for p in Product.objects.all()}
        created = 0
        for r in rows:
            email = r.get("userEmail") or r.get("user_email")
            pid = r.get("productId") or r.get("product_id")
            u = users_by_email.get(email)
            p = products.get(pid)
            if not u or not p:
                continue
            WishedProduct.objects.get_or_create(user=u, product=p)
            created += 1
        self.stdout.write(f"wished: {created}")
