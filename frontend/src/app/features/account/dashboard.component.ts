import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { forkJoin } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { LanguageService } from '../../core/language.service';
import { Address, Order, Paginated } from '../../core/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, TranslateModule],
  template: `
    <div class="container-x py-12 max-w-5xl">
      <div class="eyebrow">{{ 'nav.dashboard' | translate }}</div>
      <h1 class="display text-4xl md:text-5xl mt-1">{{ 'dashboard.greeting' | translate: { name: firstName() } }}</h1>

      <div class="grid md:grid-cols-2 gap-4 mt-10">
        <a routerLink="/orders" class="card card-lift p-6 block">
          <div class="eyebrow">{{ 'dashboard.orders' | translate }}</div>
          <div class="text-4xl font-semibold mt-2">{{ orders().length }}</div>
          <div class="text-sm text-neutral-500 mt-1">{{ 'dashboard.ordersHint' | translate }}</div>
        </a>
        <a routerLink="/account/addresses" class="card card-lift p-6 block">
          <div class="eyebrow">{{ 'dashboard.addresses' | translate }}</div>
          <div class="text-4xl font-semibold mt-2">{{ addresses().length }}</div>
          <div class="text-sm text-neutral-500 mt-1">{{ 'dashboard.addressesHint' | translate }}</div>
        </a>
      </div>

      <div class="mt-12">
        <div class="flex items-end justify-between mb-4">
          <h2 class="display text-2xl md:text-3xl">{{ 'dashboard.recentOrders' | translate }}</h2>
          <a routerLink="/orders" class="text-sm text-neutral-500 hover:text-ink transition">{{ 'home.seeAll' | translate }} →</a>
        </div>
        <div *ngIf="orders().length === 0" class="text-sm text-neutral-500">
          {{ 'dashboard.noOrders' | translate }}
          <a routerLink="/products" class="underline">{{ 'dashboard.startShopping' | translate }}</a>.
        </div>
        <div class="divide-y divide-neutral-200/70">
          <a *ngFor="let o of orders().slice(0, 5)" [routerLink]="['/orders', o.reference]"
             class="py-4 flex items-center gap-4 hover:bg-neutral-50/60 -mx-2 px-2 rounded transition">
            <span class="font-mono text-xs text-neutral-500">{{ o.short_ref }}</span>
            <span class="text-sm font-medium">{{ o.total }} {{ o.currency }}</span>
            <span class="chip">{{ o.status }}</span>
            <span class="ms-auto text-xs text-neutral-500">{{ o.created_at | date: 'MMM d, y' : undefined : lang.current() }}</span>
          </a>
        </div>
      </div>
    </div>
  `,
})
export class DashboardComponent implements OnInit {
  auth = inject(AuthService);
  lang = inject(LanguageService);
  private api = inject(ApiService);
  orders = signal<Order[]>([]);
  addresses = signal<Address[]>([]);

  firstName(): string {
    const u = this.auth.user();
    return (u?.first_name || u?.full_name?.split(' ')[0] || u?.email?.split('@')[0] || '').trim();
  }

  ngOnInit() {
    forkJoin({
      orders: this.api.get<Paginated<Order>>('/orders/'),
      addresses: this.api.get<Paginated<Address>>('/accounts/addresses/'),
    }).subscribe(({ orders, addresses }) => {
      this.orders.set(orders.results || []);
      this.addresses.set(addresses.results || []);
    });
  }
}
