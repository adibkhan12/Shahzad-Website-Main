import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { Order } from '../../core/models';

@Component({
  selector: 'app-checkout-return',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container-x py-24 max-w-xl text-center">
      <div *ngIf="statusParam === 'success'" class="animate-fade-in">
        <div class="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 mx-auto flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M5 13l4 4L19 7"/></svg>
        </div>
        <h1 class="display text-4xl mt-6">Thank you.</h1>
        <p *ngIf="order() as o" class="mt-3 text-neutral-600">
          Your order <span class="font-mono text-ink">{{ o.short_ref }}</span> has been received. We've emailed your receipt.
        </p>
        <div class="mt-8 flex items-center justify-center gap-3">
          <a routerLink="/orders" class="btn-primary">View my orders</a>
          <a routerLink="/products" class="btn-outline">Keep shopping</a>
        </div>
      </div>
      <div *ngIf="statusParam === 'cancel'" class="animate-fade-in">
        <div class="w-16 h-16 rounded-full bg-red-50 text-red-600 mx-auto flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
        </div>
        <h1 class="display text-4xl mt-6">Payment cancelled.</h1>
        <p class="mt-3 text-neutral-600">No charge was made. You can try again or pick a different method.</p>
        <a routerLink="/cart" class="btn-primary mt-8">Back to cart</a>
      </div>
    </div>
  `,
})
export class ReturnComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  order = signal<Order | null>(null);
  statusParam = '';

  ngOnInit() {
    this.route.paramMap.subscribe((p) => {
      this.statusParam = p.get('status') || '';
      const provider = p.get('provider')!;
      const reference = p.get('reference')!;
      const endpoint = this.statusParam === 'success' ? '/payments/confirm/' : '/payments/cancel/';
      this.api.post<Order>(endpoint, { provider, reference }).subscribe({
        next: (o: any) => this.order.set(o?.reference ? o : null),
      });
    });
  }
}
