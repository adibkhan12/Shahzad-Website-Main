import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../core/api.service';
import { Order } from '../../core/models';

@Component({
  selector: 'app-order-track',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container-x py-12 max-w-xl">
      <div class="eyebrow">Orders</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-8">Track your order</h1>
      <p class="text-sm text-neutral-500 mb-8">Enter your reference and the email used at checkout.</p>
      <form (ngSubmit)="submit()" class="space-y-3">
        <div><label class="label">Order reference</label><input [(ngModel)]="reference" name="reference" class="input" /></div>
        <div><label class="label">Email</label><input [(ngModel)]="email" name="email" type="email" class="input" /></div>
        <button class="btn-primary">Look up order</button>
      </form>
      <div *ngIf="error()" class="mt-6 text-red-600 text-sm">{{ error() }}</div>
      <div *ngIf="order() as o" class="mt-8 card p-5 animate-fade-in">
        <div class="flex items-center justify-between">
          <div class="font-mono text-sm">{{ o.short_ref }}</div>
          <span class="chip">{{ o.status }}</span>
        </div>
        <div class="mt-1 text-sm">Total: <span class="font-semibold">{{ o.total }} {{ o.currency }}</span></div>
        <div class="text-xs text-neutral-500 mt-1">{{ o.created_at | date: 'medium' }}</div>
      </div>
    </div>
  `,
})
export class OrderTrackComponent {
  private api = inject(ApiService);
  // Seeded sample — overwrite with your own reference + email.
  reference = '';
  email = 'demo@shahzad.ae';
  order = signal<Order | null>(null);
  error = signal('');

  submit() {
    this.order.set(null); this.error.set('');
    this.api.post<Order>('/orders/track/', { reference: this.reference, email: this.email }).subscribe({
      next: (o) => this.order.set(o),
      error: (e) => this.error.set(e?.error?.detail || 'Not found.'),
    });
  }
}
