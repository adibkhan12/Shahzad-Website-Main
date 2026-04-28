# Admin Panel Guide

Access: **http://localhost:8000/admin/**

Login: `admin@shahzad.ae` / `Admin1234!`

## Dashboard (home)

After login you land on a dashboard with 4 KPIs:
- **Orders today** (+ this-week count)
- **Revenue last 30 days** (+ all-time)
- **Total products** (+ low-stock and out-of-stock counts)
- **Open repair bookings**

Below that: recent orders table + order-status breakdown bars.

## Left sidebar groups
- **Catalog** — Products, Categories, Reviews, Questions, Banners
- **Sales** — Orders, Carts
- **Services** — Repair services, Repair bookings
- **Users** — Customers, Addresses, Wishlists

---

## Adding a product

1. Sidebar → **Catalog → Products → Add product** (top-right "Add +" button).
2. Fill: title (slug auto-fills), brand, category, description.
3. Pricing: price, compare-at-price (shown struck-through if set), stock.
4. **Upload images**: scroll to **Product images** inline at the bottom, click *Add another image*, pick file(s). First image is used as the primary thumbnail everywhere.
5. (Optional) toggle **Featured** to surface on home page.
6. Save.

## Editing / deleting
- Click the thumbnail or title on the product list to edit.
- Bulk-edit `price`, `stock`, `featured` directly in the list (inline editable).
- Select checkboxes → use **Actions** dropdown at the top:
  - Mark selected as featured / Remove featured
  - Set stock to 0 (out of stock) / Restock to 15
  - **Duplicate selected products** (creates a copy you can then edit)
  - Delete selected products

## Bulk import / export

Product admin has **Import** and **Export** buttons (top-right).

Export: pick columns, format (CSV / XLSX / JSON), download.

Import: upload a CSV/XLSX with columns:
```
id, title, slug, brand, category, price, compare_at_price, stock, is_featured, description
```
- `slug` is the unique key — existing slugs update, new slugs create.
- `category` is the category *name* (auto-created if missing).

## Orders

- Click a reference to open.
- Bulk actions: **Mark paid / shipped / delivered / cancelled**.
- Edit the `status` directly (colored pill updates live).
- Items are shown as a read-only inline.

## Repair bookings
- Set a `quoted_price` directly in the list.
- Bulk actions: **Mark quoted / in progress / ready / completed**.

## Banners (home-page hero tiles)
- Catalog → Banners → Add.
- Upload an `image_file` OR paste an image URL, set text, button label, link, colour.
- `order` controls display order (lower first). Top 3 show on the home page.

## Categories
- Upload a category image the same way (`image_file`).
- Set a `parent` to create nested categories.

## Users & addresses
- **Customers** list shows email, name, sign-up date, referral source.
- Click a user to edit; their saved addresses show as an inline.

## Site settings (key/value)
- Catalog → Settings — free-form JSON settings surfaced at `/api/v1/core/config/`.
- Useful for things like WhatsApp number, banner overrides, feature flags.

## Tips
- Top-right has a global search (🔍) — searches across products, orders, users by reference/email/title.
- **History** button on any change page shows full edit audit trail.
- **View on site** button on a product opens the frontend page.
