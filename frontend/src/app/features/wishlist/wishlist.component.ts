import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { CartService } from '../../core/cart.service';
import { WishlistService } from '../../core/wishlist.service';
import { WishlistHeartComponent } from '../../shared/wishlist-heart.component';

/**
 * /wishlist — the signed-in user's saved products.
 *
 * Layout: responsive grid of product tiles. Each tile has:
 *   - A product image (links to the product detail page)
 *   - Title + brand + price
 *   - "Move to cart" button — adds to cart and removes from wishlist
 *   - Heart button (same component used on product cards) for quick remove
 *
 * Empty state: soft illustration + CTA back to /products.
 */
@Component({
  selector: 'app-wishlist',
  standalone: true,
  imports: [CommonModule, RouterLink, WishlistHeartComponent, TranslateModule],
  template: `
    <div class="container-x py-12 min-h-[60vh]">
      <div class="flex items-end justify-between mb-8">
        <div>
          <div class="eyebrow">{{ 'wishlist.eyebrow' | translate }}</div>
          <h1 class="display text-3xl md:text-5xl mt-1">{{ 'wishlist.title' | translate }}</h1>
          <p *ngIf="wl.count() > 0" class="text-sm text-neutral-500 mt-2">
            {{ (wl.count() === 1 ? 'wishlist.itemCount' : 'wishlist.itemsCount') | translate: { count: wl.count() } }}
          </p>
        </div>
        <a *ngIf="wl.count() > 0" routerLink="/products"
           class="hidden md:inline text-sm text-neutral-500 hover:text-ink transition">
          {{ 'common.continueShopping' | translate }} →
        </a>
      </div>

      <!-- Empty state ─────────────────────────────────────────── -->
      <div *ngIf="!wl.loading() && wl.count() === 0"
           class="flex flex-col items-center text-center py-24 px-6">
        <div class="relative w-40 h-40 mb-8">
          <div class="absolute inset-0 rounded-full bg-gradient-to-br from-pink-100 to-brand-50"></div>
          <svg class="absolute inset-0 m-auto text-pink-400" width="72" height="72"
               viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
               stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </div>
        <h2 class="display text-2xl md:text-3xl">{{ 'wishlist.empty' | translate }}</h2>
        <p class="text-neutral-500 mt-2 max-w-md">
          {{ 'wishlist.emptyHint' | translate }}
        </p>
        <a routerLink="/products" class="btn btn-primary mt-8">{{ 'wishlist.browseProducts' | translate }}</a>
      </div>

      <!-- Loading placeholder ─────────────────────────────────── -->
      <div *ngIf="wl.loading() && wl.count() === 0"
           class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div *ngFor="let _ of [1,2,3,4]"
             class="aspect-square rounded-2xl bg-neutral-100/80 animate-pulse"></div>
      </div>

      <!-- Grid ────────────────────────────────────────────────── -->
      <div *ngIf="wl.count() > 0"
           class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 md:gap-8">
        <div *ngFor="let item of wl.items()" class="group relative">
          <div class="relative aspect-square rounded-2xl overflow-hidden
                      bg-gradient-to-br from-neutral-100 to-neutral-50
                      dark:from-neutral-900 dark:to-neutral-950">
            <a [routerLink]="['/products', item.product.slug]" class="block w-full h-full">
              <img *ngIf="item.product.primary_image"
                   [src]="item.product.primary_image" [alt]="item.product.title"
                   class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 ease-smooth group-hover:scale-[1.04]" />
            </a>
            <span *ngIf="item.product.on_sale"
                  class="pointer-events-none absolute top-3 start-3 px-2.5 py-1 text-[10px] uppercase tracking-wider bg-ink text-white rounded-full z-10">{{ 'product.sale' | translate }}</span>
            <app-wishlist-heart [product]="item.product" overlay />
          </div>

          <div class="pt-3">
            <div class="text-[11px] uppercase tracking-[0.14em] font-medium text-neutral-500">
              {{ item.product.brand?.name }}
            </div>
            <a [routerLink]="['/products', item.product.slug]"
               class="mt-1 block text-[15px] font-semibold tracking-tight line-clamp-2 leading-snug
                      text-neutral-900 hover:text-brand-600 transition-colors">
              {{ item.product.title }}
            </a>
            <div class="mt-2 flex items-baseline gap-2">
              <ng-container *ngIf="item.product.on_sale; else regPrice">
                <span class="price price-sale text-base">{{ item.product.sale_price }} {{ 'common.currency' | translate }}</span>
                <span class="price-was">{{ item.product.price }}</span>
              </ng-container>
              <ng-template #regPrice>
                <span class="font-bold text-[15px]">{{ item.product.price }} {{ 'common.currency' | translate }}</span>
              </ng-template>
            </div>

            <div class="mt-3 flex gap-2">
              <button (click)="moveToCart(item.product.id)"
                      [disabled]="moving.has(item.product.id)"
                      class="btn btn-primary flex-1 h-10 !text-xs">
                {{ (moving.has(item.product.id) ? 'wishlist.moving' : 'wishlist.moveToCart') | translate }}
              </button>
              <button (click)="wl.remove(item.product.id).subscribe()"
                      [disabled]="wl.isPending(item.product.id)"
                      class="btn btn-outline h-10 !text-xs"
                      [attr.aria-label]="'wishlist.removeFromWishlist' | translate">
                {{ 'wishlist.remove' | translate }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
})
export class WishlistComponent implements OnInit {
  wl = inject(WishlistService);
  private cart = inject(CartService);
  moving = new Set<number>();

  ngOnInit() {
    // Service has an effect() that refreshes on auth changes, but call
    // explicitly so a direct visit to /wishlist always re-syncs.
    this.wl.refresh().subscribe();
  }

  moveToCart(productId: number) {
    if (this.moving.has(productId)) return;
    this.moving.add(productId);
    this.cart.add(productId, 1).subscribe({
      next: () => {
        this.moving.delete(productId);
        this.wl.remove(productId).subscribe();
      },
      error: () => this.moving.delete(productId),
    });
  }
}
