import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { CartService } from '../../core/cart.service';
import { Address, Paginated } from '../../core/models';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container-x py-12 max-w-5xl">
      <div class="eyebrow">Checkout</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-10">Complete your order</h1>

      <div class="grid md:grid-cols-[1fr_380px] gap-10">
        <form (ngSubmit)="submit()" class="space-y-8">
          <!-- 1. Region -->
          <section>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-500 mb-4">1 · Deliver to</h2>
            <div class="grid grid-cols-2 gap-3">
              <label *ngFor="let r of regions"
                     class="card p-4 cursor-pointer transition"
                     [class.border-ink]="form.region === r.value">
                <input type="radio" [(ngModel)]="form.region" name="region" [value]="r.value"
                       (change)="onRegionChange()" class="hidden" />
                <div class="text-2xl mb-1">{{ r.flag }}</div>
                <div class="font-medium text-sm">{{ r.label }}</div>
                <div class="text-xs text-neutral-500 mt-0.5">{{ r.fee }} AED · {{ r.days }} days</div>
                <div *ngIf="r.value === 'KSA'" class="text-[11px] text-neutral-400 mt-1">Mecca · Madina · Jeddah only</div>
              </label>
            </div>
          </section>

          <!-- 2. Contact & shipping -->
          <section>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-500 mb-4">2 · Contact & address</h2>
            <div *ngIf="addresses().length" class="card p-4 mb-4">
              <label class="label">Use saved address</label>
              <select (change)="applyAddress($event)" class="input">
                <option value="">— Enter manually —</option>
                <option *ngFor="let a of addresses()" [value]="a.id">{{ a.name }} · {{ a.city }}</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="col-span-2"><label class="label">Full name</label><input [(ngModel)]="form.name" name="name" required class="input" /></div>
              <div><label class="label">Email</label><input type="email" [(ngModel)]="form.email" name="email" required class="input" /></div>
              <div><label class="label">Phone</label><input [(ngModel)]="form.phone" name="phone" required class="input" /></div>
              <div class="col-span-2"><label class="label">Address line 1</label><input [(ngModel)]="form.address_line1" name="address_line1" required class="input" /></div>
              <div class="col-span-2"><label class="label">Address line 2</label><input [(ngModel)]="form.address_line2" name="address_line2" class="input" /></div>
              <!-- City: dropdown for KSA, free input for UAE -->
              <div>
                <label class="label">City</label>
                <select *ngIf="form.region === 'KSA'" [(ngModel)]="form.city" name="city" required class="input">
                  <option value="">— Pick a city —</option>
                  <option *ngFor="let c of ksaCities" [value]="c">{{ c }}</option>
                </select>
                <input *ngIf="form.region !== 'KSA'" [(ngModel)]="form.city" name="city" required class="input" />
              </div>
              <div><label class="label">Postal code</label><input [(ngModel)]="form.postal_code" name="postal_code" class="input" /></div>
              <div class="col-span-2"><label class="label">Country</label><input [(ngModel)]="form.country" name="country" class="input" /></div>
            </div>
          </section>

          <!-- 3. Payment method -->
          <section>
            <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-500 mb-4">3 · Payment method</h2>
            <div class="space-y-2">
              <label *ngFor="let pm of methods"
                     class="card p-4 flex items-center gap-4 cursor-pointer transition"
                     [class.border-ink]="form.payment_method === pm.value">
                <input type="radio" [(ngModel)]="form.payment_method" name="payment_method" [value]="pm.value" class="accent-ink" />
                <div class="flex-1">
                  <div class="font-medium text-sm">{{ pm.label }}</div>
                  <div class="text-xs text-neutral-500 mt-0.5">{{ pm.desc }}</div>
                </div>
                <div class="text-xs text-neutral-400">{{ pm.tag }}</div>
              </label>
            </div>
          </section>

          <div *ngIf="error()" class="text-red-600 text-sm">{{ error() }}</div>
          <button [disabled]="loading() || cart.cart().items.length === 0" class="btn-primary w-full h-12 text-base">
            {{ loading() ? 'Processing…' : 'Place order · ' + grandTotal().toFixed(2) + ' AED' }}
          </button>
        </form>

        <aside class="card p-6 h-fit md:sticky md:top-24">
          <h3 class="font-semibold mb-4">Your order</h3>
          <div class="space-y-3 max-h-64 overflow-y-auto">
            <div *ngFor="let i of cart.cart().items" class="flex gap-3 items-center">
              <div class="w-12 h-12 rounded-lg bg-neutral-100 overflow-hidden shrink-0">
                <img *ngIf="i.product.primary_image" [src]="i.product.primary_image" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-sm font-medium truncate">{{ i.product.title }}</div>
                <div class="text-xs text-neutral-500">Qty {{ i.quantity }}</div>
              </div>
              <div class="text-sm font-semibold whitespace-nowrap">{{ i.line_total }}</div>
            </div>
          </div>
          <div class="hairline my-4"></div>
          <div class="space-y-1.5 text-sm">
            <div class="flex justify-between">
              <span class="text-neutral-500">Subtotal</span>
              <span>{{ subtotal().toFixed(2) }} AED</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-500">Shipping ({{ form.region }})</span>
              <span>{{ shippingFee().toFixed(2) }} AED</span>
            </div>
            <div *ngIf="bnplSurcharge() > 0" class="flex justify-between text-amber-700">
              <span>BNPL service fee (9%)</span>
              <span>+{{ bnplSurcharge().toFixed(2) }} AED</span>
            </div>
          </div>
          <div class="hairline my-4"></div>
          <div class="flex justify-between items-baseline">
            <span class="font-medium">Total</span>
            <span class="text-2xl font-semibold">{{ grandTotal().toFixed(2) }} AED</span>
          </div>
          <div *ngIf="form.region === 'KSA'" class="mt-3 text-[11px] text-neutral-500">
            Estimated delivery: 15–20 days to {{ form.city || 'KSA' }}.
          </div>
        </aside>
      </div>
    </div>
  `,
})
export class CheckoutComponent implements OnInit {
  private api = inject(ApiService);
  private router = inject(Router);
  cart = inject(CartService);
  auth = inject(AuthService);

  addresses = signal<Address[]>([]);
  // Seeded sample address — overridden by logged-in user's saved address when available.
  form: any = {
    name: 'Ahmed Karim',
    email: 'ahmed.karim@example.ae',
    phone: '+971501234567',
    address_line1: 'Rolla Square, Al Wahda St',
    address_line2: 'Building 42, Apt 7',
    city: 'Sharjah',
    postal_code: '00000',
    country: 'UAE',
    region: 'UAE',
    payment_method: 'cod',
  };
  loading = signal(false);
  error = signal('');
  ksaCities = ['Mecca', 'Madina', 'Jeddah'];
  regions = [
    { value: 'UAE', label: 'United Arab Emirates', flag: '🇦🇪', fee: 30, days: '1–3' },
    { value: 'KSA', label: 'Saudi Arabia', flag: '🇸🇦', fee: 150, days: '15–20' },
  ];
  methods = [
    { value: 'cod', label: 'Cash on delivery', desc: 'Pay when the driver hands over your order.', tag: 'Default' },
    { value: 'tamara', label: 'Tamara — pay in 4 (9% service fee)', desc: 'Split into 4 instalments, interest-free.', tag: 'BNPL' },
    { value: 'tabby', label: 'Tabby — pay in 4 (9% service fee)', desc: 'Pay 25% now, 25% monthly.', tag: 'BNPL' },
  ];

  // ----- live order math -----
  subtotal(): number {
    return Number(this.cart.cart().subtotal || 0);
  }

  shippingFee(): number {
    return this.form.region === 'KSA' ? 150 : 30;
  }

  bnplSurcharge(): number {
    if (this.form.payment_method === 'tamara' || this.form.payment_method === 'tabby') {
      return Math.round(this.subtotal() * 9) / 100;
    }
    return 0;
  }

  grandTotal(): number {
    return this.subtotal() + this.shippingFee() + this.bnplSurcharge();
  }

  onRegionChange() {
    // Clear any city the user typed for UAE if they switch to KSA, since the
    // KSA selector only accepts the three allowed cities.
    if (this.form.region === 'KSA' && !this.ksaCities.includes(this.form.city)) {
      this.form.city = '';
    }
  }

  ngOnInit() {
    const u = this.auth.user();
    if (u) {
      this.form.email = u.email;
      this.form.name = u.full_name || u.email.split('@')[0];
      this.api.get<Paginated<Address>>('/accounts/addresses/').subscribe((r) => {
        this.addresses.set(r.results || []);
        const def = r.results?.find((a) => a.is_default) || r.results?.[0];
        if (def) this.applySelected(def);
      });
    }
  }

  applyAddress(e: Event) {
    const id = Number((e.target as HTMLSelectElement).value);
    const a = this.addresses().find((x) => x.id === id);
    if (a) this.applySelected(a);
  }

  applySelected(a: Address) {
    this.form = {
      ...this.form,
      name: a.name || this.form.name,
      phone: a.phone, address_line1: a.address_line1, address_line2: a.address_line2,
      city: a.city, postal_code: a.postal_code, country: a.country,
    };
  }

  submit() {
    this.loading.set(true); this.error.set('');
    this.api.post<{ reference: string; redirect_url: string }>('/payments/checkout/', this.form).subscribe({
      next: (r) => {
        this.loading.set(false);
        this.cart.refresh().subscribe();
        if (r.redirect_url?.startsWith('http')) window.location.href = r.redirect_url;
        else this.router.navigateByUrl(r.redirect_url);
      },
      error: (e) => {
        this.loading.set(false);
        const body = e?.error || {};
        this.error.set(body.detail || Object.values(body).flat().join(' ') || 'Checkout failed.');
      },
    });
  }
}
