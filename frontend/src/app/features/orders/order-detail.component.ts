import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { Order } from '../../core/models';

@Component({
  selector: 'app-order-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div *ngIf="order() as o" class="container-x py-12 max-w-3xl">
      <a routerLink="/orders" class="text-sm text-neutral-500 hover:text-ink transition">← Back to orders</a>
      <div class="flex items-end justify-between mt-4 flex-wrap gap-3">
        <div>
          <div class="eyebrow">Order</div>
          <h1 class="display text-4xl md:text-5xl mt-1">{{ o.short_ref }}</h1>
          <div class="text-sm text-neutral-500 mt-1">{{ o.created_at | date: 'EEEE, MMMM d, y' }}</div>
        </div>
        <div class="flex gap-2 flex-wrap">
          <span class="chip">{{ o.status }}</span>
          <span class="chip">{{ o.payment_method }}</span>
          <span *ngIf="o.paid" class="chip !bg-emerald-50 !text-emerald-700">Paid</span>
        </div>
      </div>

      <div class="mt-10 card p-6">
        <div class="flex items-center justify-between">
          <div *ngFor="let step of steps; let i = index; let last = last" class="flex-1 flex items-center">
            <div class="flex flex-col items-center text-center flex-1">
              <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium transition"
                   [class.bg-ink]="stepActive(i)" [class.text-white]="stepActive(i)"
                   [class.bg-neutral-100]="!stepActive(i)" [class.text-neutral-400]="!stepActive(i)">
                {{ i+1 }}
              </div>
              <div class="text-xs mt-2" [class.text-ink]="stepActive(i)" [class.text-neutral-400]="!stepActive(i)">{{ step }}</div>
            </div>
            <div *ngIf="!last" class="h-px flex-1 mx-1" [class.bg-ink]="stepActive(i+1)" [class.bg-neutral-200]="!stepActive(i+1)"></div>
          </div>
        </div>
      </div>

      <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-500 mt-12 mb-4">Items</h2>
      <div class="divide-y divide-neutral-200/70 card overflow-hidden">
        <div *ngFor="let i of o.items" class="flex gap-4 p-4 items-center">
          <div class="w-16 h-16 rounded-lg bg-neutral-100 overflow-hidden shrink-0">
            <img *ngIf="i.image" [src]="i.image" class="w-full h-full object-cover" />
          </div>
          <div class="flex-1">
            <div class="text-sm font-medium">{{ i.title }}</div>
            <div class="text-xs text-neutral-500">{{ i.quantity }} × {{ i.unit_price }}</div>
          </div>
          <div class="text-sm font-semibold">{{ i.line_total }}</div>
        </div>
      </div>

      <div class="flex justify-between mt-4 font-semibold text-xl">
        <span>Total</span><span>{{ o.total }} {{ o.currency }}</span>
      </div>

      <h2 class="text-sm font-semibold uppercase tracking-wider text-neutral-500 mt-12 mb-4">Ship to</h2>
      <div class="card p-5 text-sm text-neutral-700 space-y-0.5">
        <div class="font-medium text-ink">{{ o.name }}</div>
        <div>{{ o.address_line1 }} {{ o.address_line2 }}</div>
        <div>{{ o.city }} {{ o.postal_code }}, {{ o.country }}</div>
        <div class="text-neutral-500 pt-2">{{ o.phone }} · {{ o.email }}</div>
      </div>
    </div>
  `,
})
export class OrderDetailComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  order = signal<Order | null>(null);
  steps = ['Placed', 'Paid', 'Shipped', 'Delivered'];

  stepActive(i: number): boolean {
    const s = this.order()?.status;
    const order: Record<string, number> = { pending: 0, paid: 1, shipped: 2, delivered: 3, cancelled: 0, failed: 0 };
    return s ? i <= (order[s] ?? 0) : false;
  }

  ngOnInit() {
    this.route.paramMap.subscribe((p) => {
      const ref = p.get('reference')!;
      this.api.get<Order>(`/orders/${ref}/`).subscribe((o) => this.order.set(o));
    });
  }
}
