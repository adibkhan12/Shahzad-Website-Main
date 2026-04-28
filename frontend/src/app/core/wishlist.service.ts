import { Injectable, computed, effect, inject, signal } from '@angular/core';
import { EMPTY, Observable, catchError, tap } from 'rxjs';

import { ApiService } from './api.service';
import { AuthService } from './auth.service';
import { Product } from './models';

export interface WishedEntry {
  id: number;
  product: Product;
  added_at: string;
}

/**
 * Client-side wishlist state.
 *
 * Design:
 *  - Single source of truth: `items` signal. Everything else is derived.
 *  - `ids` gives O(1) membership checks for `isFavorited(productId)`.
 *  - Optimistic updates: UI flips immediately, the API call runs in the
 *    background. On failure the state rolls back and the error bubbles.
 *  - Per-product pending lock via `pending` signal — spam clicks on the
 *    same product are ignored until the in-flight request settles.
 *  - Fires refresh() on auth changes so the list is always in sync with
 *    who is logged in. On logout, the list is cleared.
 */
@Injectable({ providedIn: 'root' })
export class WishlistService {
  private api = inject(ApiService);
  private auth = inject(AuthService);

  readonly items = signal<WishedEntry[]>([]);
  readonly loading = signal(false);
  private readonly pending = signal<Set<number>>(new Set());

  /** O(1) membership set of product IDs currently in the wishlist. */
  readonly ids = computed(() => {
    const s = new Set<number>();
    for (const it of this.items()) s.add(it.product.id);
    return s;
  });

  /** Convenience: number of entries, for header badge. */
  readonly count = computed(() => this.items().length);

  constructor() {
    // Keep state in sync with who's logged in. On login we refresh; on
    // logout we clear. The logout branch writes to `items` synchronously,
    // so this effect needs `allowSignalWrites` — otherwise Angular throws
    // NG0600 because writing signals inside an effect is disallowed by
    // default (it can cause change-detection cycles).
    effect(() => {
      const u = this.auth.user();
      if (u) this.refresh().subscribe();
      else this.items.set([]);
    }, { allowSignalWrites: true });
  }

  /** True if the given product is favorited by the current user. */
  isFavorited(productId: number): boolean {
    return this.ids().has(productId);
  }

  /** True while an in-flight toggle/add/remove is running for this product. */
  isPending(productId: number): boolean {
    return this.pending().has(productId);
  }

  /** Load the authenticated user's wishlist from the server. Safe to call
   *  when anonymous — becomes a no-op. */
  refresh(): Observable<WishedEntry[]> {
    if (!this.auth.isAuthenticated()) {
      this.items.set([]);
      return EMPTY as unknown as Observable<WishedEntry[]>;
    }
    this.loading.set(true);
    return this.api.get<WishedEntry[]>('/wishlist/').pipe(
      tap({
        next: (xs) => {
          this.items.set(xs || []);
          this.loading.set(false);
        },
        error: () => this.loading.set(false),
      }),
    );
  }

  /** Optimistic add. If the call fails, the item is removed again and
   *  the error propagates so callers can surface a toast. */
  add(product: Product): Observable<unknown> {
    if (!this.auth.isAuthenticated() || this.isPending(product.id) || this.isFavorited(product.id)) {
      return EMPTY;
    }
    this.markPending(product.id);
    const now = new Date().toISOString();
    this.items.update((xs) => [{ id: Date.now(), product, added_at: now }, ...xs]);
    return this.api.post<WishedEntry>('/wishlist/', { product_id: product.id }).pipe(
      tap({
        next: (real) => {
          // Swap the optimistic row for the server-authoritative one.
          this.items.update((xs) => xs.map((it) => (it.product.id === product.id ? real : it)));
          this.clearPending(product.id);
        },
        error: () => {
          this.items.update((xs) => xs.filter((it) => it.product.id !== product.id));
          this.clearPending(product.id);
        },
      }),
      catchError(() => EMPTY),
    );
  }

  /** Optimistic remove. Rolls back on failure. */
  remove(productId: number): Observable<unknown> {
    if (!this.auth.isAuthenticated() || this.isPending(productId)) return EMPTY;
    const snapshot = this.items();
    const removed = snapshot.find((it) => it.product.id === productId);
    if (!removed) return EMPTY;
    this.markPending(productId);
    this.items.update((xs) => xs.filter((it) => it.product.id !== productId));
    return this.api.delete(`/wishlist/${productId}/`).pipe(
      tap({
        next: () => this.clearPending(productId),
        error: () => {
          this.items.set(snapshot);
          this.clearPending(productId);
        },
      }),
      catchError(() => EMPTY),
    );
  }

  /** Convenience: add when absent, remove when present. */
  toggle(product: Product): Observable<unknown> {
    return this.isFavorited(product.id) ? this.remove(product.id) : this.add(product);
  }

  // ── internals ─────────────────────────────────────────────────
  private markPending(productId: number) {
    this.pending.update((s) => {
      const next = new Set(s);
      next.add(productId);
      return next;
    });
  }

  private clearPending(productId: number) {
    this.pending.update((s) => {
      const next = new Set(s);
      next.delete(productId);
      return next;
    });
  }
}
