# E-Commerce Rebuild Plan — Django + PostgreSQL

**Source project:** `../ecommerce-front` (Next.js 15 + Prisma + PostgreSQL + NextAuth)
**Target project:** `./` (this folder is the Django project root)
**Stack:** Django 5.x + Django REST Framework + PostgreSQL + Django templates (SSR) with HTMX/Alpine for interactivity. Optionally a decoupled React/Next front later.

---

## 1. What the existing Next.js site does (condensed)

**Auth:** NextAuth with Credentials (bcrypt) + Google OAuth; JWT sessions; password reset via email token (15-min TTL).

**Data model (13 entities):** User, Product, Category (self-referential hierarchy), Order, Cart, GuestCart, Review, QA, Address, WishedProduct, Setting (kv JSON store), AdBanner, plus NextAuth's Account/Session/VerificationToken.

**Storefront features:** product listing/filter/sort/search, category + brand pages, product detail with images/colorVariants/properties/reviews/Q&A, featured + new-product rails, ad banners, wishlist, guest cart (UUID in localStorage) that merges into auth cart, single address per user.

**Checkout & payments:** COD, Tamara, Tabby (Stripe installed but not wired). Flow: `/api/checkout` creates Order (pending) → redirects to provider → provider callback → `/api/payment/capture` marks paid + decrements stock.

**Integrations:** AWS S3 images, SMTP via nodemailer, Tawk.to chat, PWA manifest + service worker, Google Fonts (Poppins).

**~16 API endpoints, ~37 pages.** Full detail in the audit that generated this plan.

---

## 2. Target architecture

```
New Approach/                         <-- Django project root
├── manage.py
├── requirements.txt
├── .env.example
├── pyproject.toml                    # ruff/black config
├── config/                           # Django project package
│   ├── settings/ (base, dev, prod)
│   ├── urls.py, wsgi.py, asgi.py
├── apps/
│   ├── accounts/     # User, Address, auth, password reset, Google OAuth
│   ├── catalog/      # Category, Product, Review, QA, Setting
│   ├── cart/         # Cart, GuestCart, merge-on-login
│   ├── orders/       # Order, line items, status
│   ├── payments/     # COD, Tamara, Tabby adapters, capture webhook
│   ├── wishlist/     # WishedProduct
│   ├── marketing/    # AdBanner, featured/new rails
│   └── core/         # shared models, middleware, storage, pagination
├── templates/        # Django templates (base, partials, pages)
├── static/           # CSS (Tailwind), JS (HTMX/Alpine), icons
├── media/            # local dev uploads
└── prisma_reference/ # read-only copy of source schema.prisma for reference
```

**Rendering:** server-rendered Django templates + HTMX for partial swaps (cart add, wishlist toggle, Q&A post, review submit) + Alpine.js for small client state. Tailwind for styling (replacing styled-components).

**APIs:** DRF only where needed (cart sync for guest→user merge, mobile/SPA clients later). Server-rendered pages don't need a JSON API layer — avoid the double-work the old stack did.

**Auth:** Django `auth` + `django-allauth` (handles Credentials + Google OAuth + email verification + password reset in one package, replacing NextAuth).

**Storage:** `django-storages[s3]` for product images, reusing the existing S3 bucket.

**Async/email:** `django-anymail` or plain SMTP via Django's mail backend for password reset; Celery + Redis later if Tamara/Tabby callbacks need retries.

---

## 3. Data model mapping (Prisma → Django ORM)

| Prisma model | Django app | Notes on change |
|---|---|---|
| User | `accounts.User` (AbstractUser) | custom user with `email` as USERNAME_FIELD; keep `referral_source`, `referral_other` |
| Account/Session/VerificationToken | — | replaced by allauth's built-in tables |
| Category | `catalog.Category` | self-FK for hierarchy, `properties=JSONField` |
| Product | `catalog.Product` | `images=ArrayField`, `color_variants=JSONField`, `properties=JSONField`, FK to Category |
| Review | `catalog.Review` | FK Product; `images=ArrayField` |
| QA | `catalog.QA` | FK Product; nullable `answer`, `answered_at` |
| Setting | `catalog.Setting` | `name` unique, `value=JSONField` |
| Cart | `cart.Cart` | `identifier` unique (user email OR guest UUID); `items=JSONField` |
| GuestCart | — | collapsed into `Cart` (identifier handles both cases) — the old dual model was redundant |
| WishedProduct | `wishlist.WishedProduct` | FK User + FK Product; unique_together |
| Address | `accounts.Address` | OneToOne User (email-based lookup replaced by FK) |
| Order | `orders.Order` | keep Stripe-shape `line_items=JSONField` for provider compat; `status` as TextChoices (`pending/paid/shipped/delivered/cancelled`) |
| AdBanner | `marketing.AdBanner` | ordering on `order, created_at` |

**Breaking simplifications worth making now:**
- Drop `GuestCart` duplicate.
- Address as FK to User (allow multiple later) rather than email-keyed unique.
- `status` as enum choices, not free string.
- `line_items` keep JSON for provider compatibility but also write normalized `OrderItem` rows for reporting.

---

## 4. URL / view mapping (Next pages → Django URLs)

| Next page/API | Django URL | View |
|---|---|---|
| `/` | `/` | `catalog.views.home` (featured + new + categories + banners) |
| `/products` | `/products/` | `catalog.views.product_list` (filters: category, brand, sort, q) |
| `/product/[id]` | `/product/<slug:slug>/` | `catalog.views.product_detail` (reviews, Q&A, related) — switch to slug for SEO |
| `/categories` | `/categories/` | `catalog.views.category_index` |
| `/category/[id]` | `/category/<slug:slug>/` | `catalog.views.category_detail` |
| `/brand/[brand]` | `/brand/<str:brand>/` | `catalog.views.brand_detail` |
| `/search` | `/search/` | `catalog.views.search` (Postgres `trigram` / `SearchVector`) |
| `/signin`, `/signup`, `/forgot-password`, `/reset-password` | `/accounts/...` | allauth views, templates overridden |
| `/cart` | `/cart/` | `cart.views.cart_page` |
| `/account` | `/account/` | `accounts.views.dashboard` (orders, wishlist, address) |
| `/order-tracking` | `/orders/track/` | `orders.views.track` |
| `/api/checkout` | `/checkout/` (POST) | `payments.views.checkout` (dispatches to provider) |
| `/api/payment/capture` | `/payments/capture/` | `payments.views.capture` (provider callback) |
| `/checkout/tamara/success\|cancel`, `/checkout/tabby/...` | same paths | `payments.views.tamara_return`, `tabby_return` |
| `/api/cart` | `/api/cart/` (DRF) | kept for guest cart client sync |
| `/api/wishlist` toggle | `/wishlist/toggle/` (HTMX POST) | returns fragment |
| `/api/reviews`, `/api/qa` | HTMX POST endpoints | return rendered partials |
| `/api/adbanner`, `/api/quicklinks`, `/api/products`, `/api/categories` | not needed as JSON — rendered server-side |

---

## 5. Payment flow (ported)

**Checkout view (`POST /checkout/`):**
1. Validate form (address, phone, items, payment_method).
2. Create `Order(status="pending", paid=False, provider=...)`.
3. Dispatch:
   - `cod` → decrement stock, return redirect to `/orders/<id>/thank-you/`.
   - `tamara` → POST to `TAMARA_BASE_URL/checkout` with Bearer token, store `provider_ref`, redirect to `checkout_url`.
   - `tabby` → POST to `TABBY_API_URL/api/v2/checkout`, redirect to `installments[0].web_url`.
4. Return URLs point at `/payments/capture/?order_id=&provider=`.

**Capture view:** verify with provider (signed callback or GET verification), mark `paid=True, status="paid"`, decrement stock atomically inside `transaction.atomic()` + `select_for_update()` to prevent oversell.

Adapters live in `apps/payments/providers/{cod,tamara,tabby}.py` behind a common interface so Stripe or others plug in later without touching the view.

---

## 6. Frontend conversion plan

- Replace styled-components with **Tailwind CSS** (+ `django-tailwind`). Each component becomes a template partial under `templates/components/`.
- HTMX for: add-to-cart, wishlist toggle, review/Q&A submit, cart quantity ±, search suggestions. No SPA rewrite needed.
- Alpine.js for dropdowns, mobile nav, image gallery, color swatch selection.
- Keep SweetAlert2 and react-icons replaced with **Heroicons** (SVG partials) + native `<dialog>`/Alpine for modals.
- PWA: serve `manifest.json` + a service worker from `static/` via `WhiteNoise` or nginx.
- Tawk.to and WhatsApp float: include as template partials in `base.html`.

---

## 7. Data migration from existing Postgres

The current DB is already Postgres (Prisma-managed). Two options:

**A. Clean cut (recommended for dev):** point Django at a fresh DB; seed with fixtures or a one-off import script that reads from the old DB via raw SQL and writes through Django ORM. Order matters: Users → Categories → Products → AdBanners → Settings → Addresses → Orders → Cart items → Reviews/QA/Wishlist.

**B. In-place adoption:** `python manage.py inspectdb` against the Prisma DB, hand-edit models to match, then use `--fake-initial` migrations. Faster but you inherit Prisma's naming/conventions (snake-case vs camelCase mismatches, NextAuth tables to drop).

Go with **A**. One import script in `scripts/import_from_prisma.py`, idempotent, runnable per-table.

**Password hashes:** bcryptjs output is compatible with Django's `BCryptSHA256PasswordHasher` only with care — bcrypt hashes directly work via `BCryptPasswordHasher`. Add it to `PASSWORD_HASHERS` as the fallback so existing users can log in and get rehashed on next login.

---

## 8. Env vars (Django equivalents)

```
DATABASE_URL=postgres://...
SECRET_KEY=...
DEBUG=1
ALLOWED_HOSTS=localhost,...
SITE_URL=http://localhost:8000                    # was NEXT_PUBLIC_BASE_URL

# Google OAuth (via allauth)
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=

# Email
EMAIL_HOST=, EMAIL_HOST_USER=, EMAIL_HOST_PASSWORD=, DEFAULT_FROM_EMAIL=

# S3
AWS_ACCESS_KEY_ID=, AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=adib-next-ecommerce
AWS_S3_REGION_NAME=eu-north-1

# Payments
TAMARA_BASE_URL=, TAMARA_API_KEY=
TABBY_API_URL=, TABBY_SECRET_KEY=
CURRENCY=AED
```

---

## 9. Phased implementation plan

**Phase 0 — Scaffold (0.5 day)**
- `django-admin startproject config .`
- Create apps listed above with `startapp`.
- Split settings (base/dev/prod), wire `django-environ`, install Tailwind.
- Set up Postgres locally, run empty migrations, confirm `/admin` works.

**Phase 1 — Accounts & auth (1 day)**
- Custom `User` model (email login). Migrate before first makemigrations.
- Install `django-allauth`, configure Credentials + Google.
- Email verification + password reset templates.
- Login/signup/forgot/reset pages styled to match brand (`#740DC2`).

**Phase 2 — Catalog (1.5 days)**
- Models: Category (self-FK, slug), Product (images array, JSON props, slug), Setting.
- Admin configuration (inline images, rich filters, import via fixtures).
- Public views: home, product list with filters, product detail, category, brand, search.
- Templates + Tailwind styling.

**Phase 3 — Cart & wishlist (1 day)**
- `Cart` model with `identifier` (session key for guests, user.id for auth).
- HTMX endpoints: add, update qty, remove, clear.
- Guest→user merge on login (allauth signal).
- Wishlist toggle endpoint + `/account/wishlist/`.

**Phase 4 — Orders & checkout (1.5 days)**
- `Order` model + `OrderItem` normalized rows.
- Checkout form (address reused from account).
- Payment adapter interface; implement COD first end-to-end.
- Thank-you page, order history, order tracking page.

**Phase 5 — Tamara + Tabby (1 day)**
- Port request payloads from `pages/api/checkout.js` line-by-line.
- Implement `/payments/capture/` with atomic stock decrement.
- Add return-URL templates (success/cancel for each provider).

**Phase 6 — Reviews, Q&A, ad banners (0.5 day)**
- Models + HTMX submit endpoints + admin moderation.
- Home-page rails: featured (from Setting), new products, ad banner carousel.

**Phase 7 — Integrations & polish (0.5 day)**
- S3 via django-storages.
- Tawk.to + WhatsApp float partials.
- PWA manifest + service worker.
- Error pages (404/500), sitemap, robots.txt.

**Phase 8 — Data import + cutover (1 day)**
- Write `scripts/import_from_prisma.py`.
- Dry-run against a copy of prod DB; verify counts per table.
- Plan prod cutover (DNS, HTTPS, gunicorn + nginx or a PaaS).

**Total:** ~8 focused days of work.

---

## 10. Tests & quality gates

- `pytest-django` + `factory-boy` for models/views.
- Golden tests per payment adapter with `responses`/`httpx_mock` to pin the provider JSON shape.
- `ruff` + `black` + `mypy` (optional) via pre-commit.
- GitHub Actions: lint + test + migrations check on every PR.

---

## 11. Open questions to confirm before coding

1. **Keep the same Postgres DB** (import approach) or start fresh with seeded demo data?
2. **Product URLs:** migrate to slugs (SEO win, requires adding slug field) or keep numeric IDs (zero-friction)?
3. **Single address** per user (current) or multi-address now while we're redesigning?
4. **Admin UI:** Django admin is enough, or do you want a bespoke dashboard like the existing one?
5. **Frontend:** Django templates + HTMX (this plan, fastest) or keep a separate React/Next front and have Django be pure DRF?
6. **Currency/i18n:** AED only, or plan for multi-currency + multi-language from day one?

Answer these and Phase 0 can start immediately.
