import { Injectable, computed, inject, signal } from '@angular/core';
import { tap } from 'rxjs';

import { ApiService } from './api.service';
import { Cart } from './models';

const EMPTY: Cart = { items: [], subtotal: '0.00', count: 0 };

@Injectable({ providedIn: 'root' })
export class CartService {
  private api = inject(ApiService);
  readonly cart = signal<Cart>(EMPTY);
  readonly count = computed(() => this.cart().count);
  readonly subtotal = computed(() => this.cart().subtotal);

  refresh() {
    return this.api.get<Cart>('/cart/').pipe(tap((c) => this.cart.set(c || EMPTY)));
  }

  add(productId: number, quantity = 1) {
    return this.api
      .post<Cart>('/cart/add/', { product_id: productId, quantity })
      .pipe(tap((c) => this.cart.set(c)));
  }

  update(itemId: number, quantity: number) {
    return this.api
      .patch<Cart>(`/cart/items/${itemId}/`, { quantity })
      .pipe(tap((c) => this.cart.set(c)));
  }

  remove(itemId: number) {
    return this.api.delete<Cart>(`/cart/items/${itemId}/`).pipe(tap((c) => this.cart.set(c)));
  }

  clear() {
    return this.api.post<Cart>('/cart/clear/', {}).pipe(tap((c) => this.cart.set(c)));
  }

  mergeAfterLogin() {
    return this.api.post<Cart>('/cart/merge/', {}).pipe(tap((c) => this.cart.set(c)));
  }
}
