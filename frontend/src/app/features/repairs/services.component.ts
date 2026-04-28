import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { Paginated, RepairService } from '../../core/models';

@Component({
  selector: 'app-repair-services',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <!-- Hero -->
    <section class="bg-gradient-to-br from-neutral-50 to-brand-50/40 border-b border-neutral-200/70">
      <div class="container-x py-16 md:py-24 grid md:grid-cols-2 gap-10 items-center">
        <div>
          <div class="eyebrow">On-site repairs · In-store only</div>
          <h1 class="display text-5xl md:text-6xl leading-[0.95] tracking-tight mt-4">
            Walk in.<br/><em class="text-brand">Walk out fixed.</em>
          </h1>
          <p class="mt-6 text-neutral-600 max-w-md">Every repair is done on-site by our technicians at our Rolla, Sharjah flagship — no couriers, no third parties. Genuine parts and a 1-year warranty on every job.</p>
          <a routerLink="/repairs/status" class="mt-6 inline-flex text-sm text-ink hover:underline">Check status of a booking →</a>
        </div>
        <div class="flex gap-3 justify-self-end md:pl-16">
          <div class="w-40 aspect-[3/4] rounded-3xl bg-ink text-white p-6 flex flex-col justify-end">
            <div class="text-3xl">📱</div>
            <div class="mt-auto text-sm">Phones</div>
          </div>
          <div class="w-40 aspect-[3/4] rounded-3xl bg-brand text-white p-6 flex flex-col justify-end mt-8">
            <div class="text-3xl">💻</div>
            <div class="mt-auto text-sm">Laptops</div>
          </div>
        </div>
      </div>
    </section>

    <div class="container-x py-12">
      <div class="flex flex-wrap gap-2 mb-10">
        <button (click)="filter.set('')" class="chip" [class.chip-active]="!filter()">All</button>
        <button *ngFor="let d of devices()" (click)="filter.set(d.value)"
                class="chip" [class.chip-active]="filter() === d.value">{{ d.label }}</button>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
        <a *ngFor="let s of filtered()" [routerLink]="['/repairs/book', s.slug]"
           class="card card-lift p-6 block group">
          <div class="text-3xl mb-3">{{ s.icon }}</div>
          <h3 class="font-medium text-[15px]">{{ s.name }}</h3>
          <p class="text-sm text-neutral-500 mt-1.5 line-clamp-2">{{ s.short_desc }}</p>
          <div class="mt-5 flex items-center justify-between">
            <div class="font-semibold">{{ s.base_price }} AED</div>
            <div class="text-xs text-neutral-500">~{{ s.est_minutes }} min</div>
          </div>
        </a>
      </div>
    </div>
  `,
})
export class RepairServicesComponent implements OnInit {
  private api = inject(ApiService);
  services = signal<RepairService[]>([]);
  devices = signal<{ value: string; label: string }[]>([]);
  filter = signal('');
  filtered = () => this.filter() ? this.services().filter(s => s.device === this.filter()) : this.services();

  ngOnInit() {
    this.api.get<Paginated<RepairService>>('/repairs/services/').subscribe((r) => this.services.set(r.results || []));
    this.api.get<any[]>('/repairs/services/devices/').subscribe((d) => this.devices.set(d || []));
  }
}
