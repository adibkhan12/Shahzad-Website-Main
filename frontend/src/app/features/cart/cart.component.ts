import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { CartService } from '../../core/cart.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslateModule],
  template: `
    <div class="container-x py-12 max-w-5xl">
      <div class="eyebrow">{{ 'cart.title' | translate }}</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-10">{{ 'cart.title' | translate }}</h1>

      <div *ngIf="cart.cart().items.length === 0" class="py-20 text-center">
        <div class="text-6xl mb-4 opacity-30">🛒</div>
        <p class="text-neutral-500">{{ 'cart.empty' | translate }}</p>
        <a routerLink="/products" class="btn-primary mt-6 inline-flex">{{ 'wishlist.browseProducts' | translate }}</a>
      </div>

      <div *ngIf="cart.cart().items.length > 0" class="grid md:grid-cols-[1fr_380px] gap-10">
        <div class="space-y-4">
          <div *ngFor="let i of cart.cart().items" class="group flex items-center gap-4 py-5 border-b border-neutral-200/70">
            <a [routerLink]="['/products', i.product.slug]" class="w-24 h-24 rounded-xl bg-neutral-100 overflow-hidden shrink-0">
              <img *ngIf="i.product.primary_image" [src]="i.product.primary_image"
                   class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
            </a>
            <div class="flex-1 min-w-0">
              <div class="eyebrow">{{ i.product.brand }}</div>
              <a [routerLink]="['/products', i.product.slug]" class="mt-0.5 block text-sm font-medium hover:text-brand-600 transition truncate">{{ i.product.title }}</a>
              <div class="text-sm text-neutral-500 mt-0.5">{{ i.product.price }} {{ 'common.currency' | translate }}</div>
            </div>
            <div class="flex items-center border border-neutral-200 rounded-full overflow-hidden">
              <button (click)="update(i.id, i.quantity-1)" class="w-9 h-9 text-neutral-500 hover:bg-neutral-50">−</button>
              <input type="number" [ngModel]="i.quantity" (ngModelChange)="update(i.id, $event)"
                     min="1" class="w-10 h-9 text-center border-0 focus:outline-none text-sm" />
              <button (click)="update(i.id, i.quantity+1)" class="w-9 h-9 text-neutral-500 hover:bg-neutral-50">+</button>
            </div>
            <div class="w-24 text-end text-sm font-semibold">{{ i.line_total }} {{ 'common.currency' | translate }}</div>
            <button (click)="remove(i.id)" class="w-8 h-8 text-neutral-400 hover:text-red-600 transition" [attr.aria-label]="'cart.remove' | translate">
              <svg class="w-4 h-4 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75">
                <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m2 0v14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6h12Z"/>
              </svg>
            </button>
          </div>
        </div>

        <aside class="card p-6 h-fit md:sticky md:top-24">
          <h2 class="font-semibold mb-4">{{ 'checkout.orderSummary' | translate }}</h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between"><span class="text-neutral-500">{{ 'cart.subtotal' | translate }}</span><span>{{ cart.cart().subtotal }} {{ 'common.currency' | translate }}</span></div>
            <div class="flex justify-between"><span class="text-neutral-500">{{ 'cart.shipping' | translate }}</span><span class="text-emerald-600">{{ 'cart.shippingFree' | translate }}</span></div>
          </div>
          <div class="hairline my-4"></div>
          <div class="flex justify-between items-baseline">
            <span class="font-medium">{{ 'cart.total' | translate }}</span>
            <span class="text-2xl font-semibold">{{ cart.cart().subtotal }} {{ 'common.currency' | translate }}</span>
          </div>
          <a routerLink="/checkout" class="btn-primary w-full mt-6">{{ 'cart.checkout' | translate }}
            <svg class="w-4 h-4 dir-flip" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
          <div class="mt-5 flex justify-center gap-2 text-[11px] text-neutral-500 flex-wrap">
            <span class="chip">{{ 'footer.cashOnDelivery' | translate }}</span>
            <span class="chip">Tamara</span>
            <span class="chip">Tabby</span>
          </div>
        </aside>
      </div>
    </div>
  `,
})
export class CartComponent {
  cart = inject(CartService);
  update(id: number, qty: number) { if (qty >= 0) this.cart.update(id, qty).subscribe(); }
  remove(id: number) { this.cart.remove(id).subscribe(); }
}
