import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../core/api.service';
import { RepairBooking } from '../../core/models';

@Component({
  selector: 'app-repair-status',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container-x py-12 max-w-xl">
      <div class="eyebrow">Repairs</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-8">Booking status</h1>
      <form (ngSubmit)="lookup()" class="space-y-3">
        <div><label class="label">Reference</label><input [(ngModel)]="reference" name="reference" class="input" /></div>
        <div><label class="label">Phone</label><input [(ngModel)]="phone" name="phone" class="input" /></div>
        <button class="btn-primary">Look up</button>
      </form>
      <div *ngIf="error()" class="mt-6 text-red-600 text-sm">{{ error() }}</div>
      <div *ngIf="booking() as b" class="mt-8 card p-5 animate-fade-in">
        <div class="font-mono text-sm">{{ b.short_ref }}</div>
        <div class="mt-1 font-medium">{{ b.device_brand }} {{ b.device_model }}</div>
        <div class="flex gap-2 mt-3">
          <span class="chip">{{ b.status }}</span>
          <span *ngIf="b.quoted_price" class="chip">Quote: {{ b.quoted_price }} AED</span>
        </div>
      </div>
    </div>
  `,
})
export class RepairStatusComponent {
  private api = inject(ApiService);
  reference = '';
  phone = '+971501234567';
  booking = signal<RepairBooking | null>(null);
  error = signal('');
  lookup() {
    this.booking.set(null); this.error.set('');
    this.api.post<RepairBooking>('/repairs/bookings/status/', { reference: this.reference, phone: this.phone }).subscribe({
      next: (b) => this.booking.set(b),
      error: (e) => this.error.set(e?.error?.detail || 'Not found.'),
    });
  }
}
