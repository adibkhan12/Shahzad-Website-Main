import { CommonModule } from '@angular/common';
import { Component, Input, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { CartService } from '../core/cart.service';
import { Product } from '../core/models';
import { TiltDirective } from './tilt.directive';
import { WishlistHeartComponent } from './wishlist-heart.component';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule, RouterLink, TiltDirective, WishlistHeartComponent, TranslateModule],
  template: `
    <div class="tilt-stage">
      <div appTilt [max]="5"
           class="group relative rounded-2xl p-2 -m-2 transition-all duration-[900ms] ease-smooth
                  hover:bg-gradient-to-b hover:from-white hover:via-white hover:to-brand-50/60
                  hover:shadow-[0_8px_40px_-12px_rgba(168,85,247,0.28)]">

        <!-- Image tile. The wishlist heart is a sibling of the anchor so
             its click can't bubble into a route navigation. The heart
             component itself also stops propagation internally. -->
        <div class="relative aspect-square bg-gradient-to-br from-neutral-100 to-neutral-50
                    dark:from-neutral-900 dark:to-neutral-950 rounded-2xl overflow-hidden">
          <a [routerLink]="['/products', product.slug]" class="block w-full h-full">
            <img *ngIf="product.primary_image" [src]="product.primary_image" [alt]="product.title"
                 class="absolute inset-0 w-full h-full object-cover transition-all duration-[1400ms] ease-smooth group-hover:scale-[1.06]" />
            <span class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/0 to-transparent group-hover:from-black/5 transition-all duration-700"></span>
          </a>
          <span *ngIf="product.on_sale"
                class="pointer-events-none absolute top-3 start-3 px-2.5 py-1 text-[10px] uppercase tracking-wider bg-ink text-white rounded-full z-10">{{ 'product.sale' | translate }}</span>
          <app-wishlist-heart [product]="product" overlay />
        </div>

        <div class="pt-3.5 pb-1">
          <div class="text-[11px] uppercase tracking-[0.14em] font-medium text-neutral-500 dark:text-neutral-300/80">{{ product.brand?.name }}</div>
          <a [routerLink]="['/products', product.slug]"
             class="mt-1 block text-[15px] font-semibold tracking-tight line-clamp-2 leading-snug
                    text-neutral-900 dark:text-white
                    hover:text-brand-600 dark:hover:text-brand-300 transition-colors">
            {{ product.title }}
          </a>
          <div class="mt-2 flex items-baseline gap-2 price">
            <ng-container *ngIf="product.on_sale; else regularPrice">
              <span class="price price-sale text-base">{{ product.sale_price }} {{ 'common.currency' | translate }}</span>
              <span class="price-was">{{ product.price }}</span>
            </ng-container>
            <ng-template #regularPrice>
              <span class="font-bold text-[15px] text-neutral-900 dark:text-white">{{ product.price }} {{ 'common.currency' | translate }}</span>
            </ng-template>
          </div>
        </div>
        <button (click)="add()" [disabled]="adding"
                class="btn btn-primary btn-futura w-full h-10 mt-2 opacity-0 translate-y-1
                       group-hover:opacity-100 group-hover:translate-y-0
                       transition-all duration-[900ms] ease-smooth
                       disabled:opacity-60">
          {{ adding ? ('product.adding' | translate) : ('product.addToCart' | translate) }}
        </button>
      </div>
    </div>
  `,
})
export class ProductCardComponent {
  @Input({ required: true }) product!: Product;
  private cart = inject(CartService);
  adding = false;

  add() {
    this.adding = true;
    this.cart.add(this.product.id, 1).subscribe({
      next: () => (this.adding = false),
      error: () => (this.adding = false),
    });
  }
}
