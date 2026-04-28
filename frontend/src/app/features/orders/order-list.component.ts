import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { Order, Paginated } from '../../core/models';

@Component({
  selector: 'app-order-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container-x py-12 max-w-4xl">
      <div class="eyebrow">Account</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-10">My orders</h1>
      <div *ngIf="orders().length === 0" class="text-sm text-neutral-500">You have no orders yet.</div>
      <div class="divide-y divide-neutral-200/70">
        <a *ngFor="let o of orders()" [routerLink]="['/orders', o.reference]"
           class="block py-5 flex items-center gap-4 hover:bg-neutral-50/60 -mx-2 px-2 rounded transition">
          <span class="font-mono text-xs text-neutral-500 w-16">{{ o.short_ref }}</span>
          <span class="text-sm font-medium">{{ o.total }} {{ o.currency }}</span>
          <span class="chip">{{ o.status }}</span>
          <span *ngIf="o.paid" class="chip !bg-emerald-50 !text-emerald-700">Paid</span>
          <span class="ml-auto text-xs text-neutral-500">{{ o.created_at | date: 'MMM d, y' }}</span>
          <svg class="w-3.5 h-3.5 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </a>
      </div>
    </div>
  `,
})
export class OrderListComponent implements OnInit {
  private api = inject(ApiService);
  orders = signal<Order[]>([]);
  ngOnInit() { this.api.get<Paginated<Order>>('/orders/').subscribe((r) => this.orders.set(r.results || [])); }
}
