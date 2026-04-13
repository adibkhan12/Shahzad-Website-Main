"""
One-off import from the legacy Mongoose-managed MongoDB Atlas DB into Django.

Usage:
    python manage.py import_from_mongo --dry-run
    python manage.py import_from_mongo
    python manage.py import_from_mongo --truncate
    python manage.py import_from_mongo --only=products,orders

Reads LEGACY_MONGODB_URI (+ optional LEGACY_MONGODB_DB override) from .env.
Safe to re-run: keyed by legacy ObjectId stored in `legacy_id` on each row.
"""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

try:
    from pymongo import MongoClient
    from bson import ObjectId
except ImportError:  # pragma: no cover
    MongoClient = None


COLLECTIONS = ["users", "categories", "products", "adbanners", "settings", "addresses", "reviews", "qas", "orders", "wished"]


class Command(BaseCommand):
    help = "Import rows from the legacy MongoDB Atlas DB."

    def add_arguments(self, parser):
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--only", default="", help="Comma-separated: " + ",".join(COLLECTIONS))
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        if not MongoClient:
            raise CommandError("pymongo not installed. Run: pip install pymongo dnspython")
        uri = getattr(settings, "LEGACY_MONGODB_URI", "")
        if not uri:
            raise CommandError("LEGACY_MONGODB_URI is empty. Set it in .env and retry.")

        only = {x.strip() for x in opts["only"].split(",") if x.strip()} or set(COLLECTIONS)
        dry = opts["dry_run"]

        self.stdout.write("Connecting to Mongo…")
        client = MongoClient(uri)
        db_name = getattr(settings, "LEGACY_MONGODB_DB", "") or self._pick_db(client)
        self.stdout.write(f"Using database: {db_name}")
        db = client[db_name]

        self._introspect(db)
        if opts["truncate"] and not dry:
            self._truncate()

        # Maps from legacy ObjectId string → Django instance
        self.user_map = {}
        self.cat_map = {}
        self.prod_map = {}

        if "users" in only:
            self._copy_users(db, dry)
        if "categories" in only:
            self._copy_categories(db, dry)
        if "products" in only:
            self._copy_products(db, dry)
        if "adbanners" in only:
            self._copy_adbanners(db, dry)
        if "settings" in only:
            self._copy_settings(db, dry)
        if "addresses" in only:
            self._copy_addresses(db, dry)
        if "reviews" in only:
            self._copy_reviews(db, dry)
        if "qas" in only:
            self._copy_qas(db, dry)
        if "orders" in only:
            self._copy_orders(db, dry)
        if "wished" in only:
            self._copy_wishlist(db, dry)

        self.stdout.write(self.style.SUCCESS("Import complete." if not dry else "Dry-run complete."))

    # ---- helpers ----
    def _pick_db(self, client):
        for candidate in ("test", "ecommerce", "Cluster0", "mydb"):
            if candidate in client.list_database_names():
                return candidate
        dbs = [d for d in client.list_database_names() if d not in ("admin", "config", "local")]
        if not dbs:
            raise CommandError("No user databases found in the Mongo cluster.")
        return dbs[0]

    def _introspect(self, db):
        colls = db.list_collection_names()
        counts = {c: db[c].estimated_document_count() for c in colls}
        self.stdout.write("Collections: " + ", ".join(f"{c}={n}" for c, n in sorted(counts.items())))
        self.collections = set(colls)

    def _first(self, db, *names):
        for n in names:
            if n in self.collections:
                return db[n]
        return None

    def _oid(self, v):
        return str(v) if v else ""

    def _num(self, v, default=0):
        try:
            return float(v) if v is not None else default
        except (TypeError, ValueError):
            return default

    def _truncate(self):
        from apps.accounts.models import Address, User
        from apps.catalog.models import AdBanner, Category, Product, QA, Review, Setting
        from apps.orders.models import Order
        from apps.wishlist.models import WishedProduct
        WishedProduct.objects.all().delete()
        QA.objects.all().delete()
        Review.objects.all().delete()
        Order.objects.all().delete()
        Address.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        AdBanner.objects.all().delete()
        Setting.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.WARNING("Truncated target tables."))

    # ---- per-collection ----
    @transaction.atomic
    def _copy_users(self, db, dry):
        coll = self._first(db, "users")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] users: {len(docs)}")
            return
        from apps.accounts.models import User
        created = 0
        for d in docs:
            email = (d.get("email") or "").strip().lower()
            if not email:
                continue
            user, was_new = User.objects.update_or_create(
                email=email,
                defaults={
                    "username": email,
                    "first_name": (d.get("name") or "").split(" ")[0][:150],
                    "last_name": " ".join((d.get("name") or "").split(" ")[1:])[:150],
                    "referral_source": d.get("referralSource") or "",
                    "referral_other": d.get("referralOther") or "",
                    "is_active": True,
                },
            )
            pw = d.get("password") or ""
            if was_new and pw:
                # bcryptjs hashes start with "$2a$" / "$2b$" — Django's BCryptPasswordHasher expects "bcrypt$<hash>"
                if pw.startswith("$2"):
                    user.password = f"bcrypt${pw}"
                else:
                    user.password = pw
                user.save(update_fields=["password"])
                created += 1
            self.user_map[self._oid(d["_id"])] = user
        self.stdout.write(f"users: {len(docs)} synced ({created} new with password)")

    @transaction.atomic
    def _copy_categories(self, db, dry):
        coll = self._first(db, "categories")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] categories: {len(docs)}")
            return
        from apps.catalog.models import Category
        for d in docs:
            cat, _ = Category.objects.update_or_create(
                name=d["name"],
                defaults={"properties": d.get("properties") or []},
            )
            self.cat_map[self._oid(d["_id"])] = cat
        # parents
        for d in docs:
            parent = d.get("parent")
            if parent:
                child = self.cat_map.get(self._oid(d["_id"]))
                par = self.cat_map.get(self._oid(parent))
                if child and par:
                    child.parent = par
                    child.save(update_fields=["parent"])
        self.stdout.write(f"categories: {len(docs)}")

    @transaction.atomic
    def _copy_products(self, db, dry):
        coll = self._first(db, "products")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] products: {len(docs)}")
            return
        from apps.catalog.models import Category, Product
        if not self.cat_map:
            self.cat_map = {str(c.pk): c for c in Category.objects.all()}  # best effort
        for d in docs:
            props = d.get("properties") or {}
            brand = ""
            if isinstance(props, dict):
                brand = props.get("Brand") or props.get("brand") or ""
            cat = self.cat_map.get(self._oid(d.get("category")))
            # colorVariants mongo → flat list of color hex/name strings for our simpler schema
            color_variants = []
            for cv in d.get("colorVariants") or []:
                if isinstance(cv, dict):
                    c = cv.get("color")
                    if c:
                        color_variants.append(str(c))
            prod, _ = Product.objects.update_or_create(
                title=d["title"],
                defaults={
                    "description": d.get("description") or "",
                    "price": Decimal(str(self._num(d.get("price"), 0))),
                    "images": list(d.get("images") or []),
                    "stock": int(self._num(d.get("stock"), 0)),
                    "color_variants": color_variants,
                    "properties": props if isinstance(props, dict) else {},
                    "brand": brand,
                    "category": cat,
                },
            )
            self.prod_map[self._oid(d["_id"])] = prod
        self.stdout.write(f"products: {len(docs)}")

    @transaction.atomic
    def _copy_adbanners(self, db, dry):
        coll = self._first(db, "adbanners")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] adbanners: {len(docs)}")
            return
        from apps.catalog.models import AdBanner
        for d in docs:
            AdBanner.objects.update_or_create(
                title=d["title"],
                defaults={
                    "desc": d.get("desc") or "",
                    "image": d.get("image") or "",
                    "button": d.get("button") or "",
                    "link": d.get("link") or "",
                    "bg": d.get("bg") or "#740DC2",
                    "order": int(self._num(d.get("order"), 0)),
                },
            )
        self.stdout.write(f"adbanners: {len(docs)}")

    @transaction.atomic
    def _copy_settings(self, db, dry):
        coll = self._first(db, "settings")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] settings: {len(docs)}")
            return
        from apps.catalog.models import Setting
        for d in docs:
            Setting.objects.update_or_create(name=d["name"], defaults={"value": d.get("value") or {}})
        self.stdout.write(f"settings: {len(docs)}")

    @transaction.atomic
    def _copy_addresses(self, db, dry):
        coll = self._first(db, "addresses")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] addresses: {len(docs)}")
            return
        from apps.accounts.models import Address, User
        users_by_email = {u.email: u for u in User.objects.all()}
        saved = 0
        for d in docs:
            email = (d.get("userEmail") or "").strip().lower()
            user = users_by_email.get(email)
            if not user:
                continue
            Address.objects.update_or_create(
                user=user,
                name=d.get("name") or user.email,
                defaults={
                    "email": d.get("email") or email,
                    "phone": d.get("number") or "",
                    "address_line1": d.get("addressLine1") or "",
                    "address_line2": d.get("addressLine2") or "",
                    "city": d.get("city") or "",
                    "postal_code": d.get("postalCode") or "",
                    "country": d.get("country") or "UAE",
                    "is_default": True,
                },
            )
            saved += 1
        self.stdout.write(f"addresses: {saved}")

    @transaction.atomic
    def _copy_reviews(self, db, dry):
        coll = self._first(db, "reviews")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] reviews: {len(docs)}")
            return
        from apps.catalog.models import Review
        if not self.prod_map:
            from apps.catalog.models import Product
            self.prod_map = {}
        created = 0
        for d in docs:
            p = self.prod_map.get(self._oid(d.get("product")))
            if not p:
                continue
            Review.objects.create(
                product=p,
                user=d.get("user") or "",
                rating=int(self._num(d.get("rating"), 5)) or 5,
                text=d.get("text") or "",
                images=list(d.get("images") or []),
            )
            created += 1
        self.stdout.write(f"reviews: {created}")

    @transaction.atomic
    def _copy_qas(self, db, dry):
        coll = self._first(db, "qas")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] qas: {len(docs)}")
            return
        from apps.catalog.models import QA
        created = 0
        for d in docs:
            p = self.prod_map.get(self._oid(d.get("product")))
            if not p:
                continue
            QA.objects.create(
                product=p,
                user=d.get("user") or "",
                question=d.get("question") or "",
                answer=d.get("answer") or "",
                answered_at=d.get("answeredAt"),
            )
            created += 1
        self.stdout.write(f"qas: {created}")

    @transaction.atomic
    def _copy_orders(self, db, dry):
        coll = self._first(db, "orders")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] orders: {len(docs)}")
            return
        from apps.accounts.models import User
        from apps.catalog.models import Product
        from apps.orders.models import Order, OrderItem
        users_by_email = {u.email: u for u in User.objects.all()}
        status_map = {
            "pending": Order.Status.PENDING, "authorized": Order.Status.PAID,
            "paid": Order.Status.PAID, "failed": Order.Status.FAILED, "canceled": Order.Status.CANCELLED,
        }
        method_map = {
            "COD": Order.PaymentMethod.COD, "cod": Order.PaymentMethod.COD,
            "tamara": Order.PaymentMethod.TAMARA, "tabby": Order.PaymentMethod.TABBY,
            "card": Order.PaymentMethod.COD,  # we don't have a 'card' type — fallback
        }
        created = 0
        for d in docs:
            email = (d.get("email") or "").strip().lower()
            user = users_by_email.get(email)
            subtotal = 0
            line_items = d.get("line_items") or []
            for li in line_items:
                pd = (li or {}).get("price_data") or {}
                ua = pd.get("unit_amount", 0) or 0
                qty = li.get("quantity") or 1
                subtotal += (ua / 100.0) * qty
            total = float(d.get("amount") or subtotal or 0)
            order = Order.objects.create(
                user=user,
                name=d.get("name") or "",
                email=email,
                phone=d.get("number") or "",
                address_line1=d.get("addressLine1") or "",
                address_line2=d.get("addressLine2") or "",
                city=d.get("city") or "",
                postal_code=d.get("postal_code") or "",
                country=d.get("country") or "UAE",
                currency=d.get("currency") or "AED",
                subtotal=Decimal(str(subtotal or total)),
                total=Decimal(str(total or subtotal)),
                payment_method=method_map.get(d.get("paymentMethod") or "COD", Order.PaymentMethod.COD),
                provider=d.get("provider") or "",
                provider_ref=d.get("providerRef") or "",
                paid=bool(d.get("paid")),
                status=status_map.get(d.get("status") or "pending", Order.Status.PENDING),
                referral_source=d.get("referralSource") or "",
                referral_other=d.get("referralOther") or "",
                line_items=line_items,
            )
            # Backdate created_at if present
            ts = d.get("createdAt")
            if ts:
                Order.objects.filter(pk=order.pk).update(created_at=ts)

            # Normalize line_items → OrderItem rows
            for li in line_items:
                pd = (li or {}).get("price_data") or {}
                name = ((pd.get("product_data") or {}).get("name")) or "Item"
                ua = pd.get("unit_amount", 0) or 0
                OrderItem.objects.create(
                    order=order,
                    product=None,
                    title=name,
                    unit_price=Decimal(str(ua / 100.0)),
                    quantity=int(li.get("quantity") or 1),
                )
            created += 1
        self.stdout.write(f"orders: {created}")

    @transaction.atomic
    def _copy_wishlist(self, db, dry):
        coll = self._first(db, "wishedproducts", "wished")
        if coll is None:
            return
        docs = list(coll.find({}))
        if dry:
            self.stdout.write(f"[dry] wished: {len(docs)}")
            return
        from apps.accounts.models import User
        from apps.wishlist.models import WishedProduct
        users_by_email = {u.email: u for u in User.objects.all()}
        created = 0
        for d in docs:
            email = (d.get("userEmail") or "").strip().lower()
            user = users_by_email.get(email)
            prod = self.prod_map.get(self._oid(d.get("product")))
            if not user or not prod:
                continue
            WishedProduct.objects.get_or_create(user=user, product=prod)
            created += 1
        self.stdout.write(f"wished: {created}")
