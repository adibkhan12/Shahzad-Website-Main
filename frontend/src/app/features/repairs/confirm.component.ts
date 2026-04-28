import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { RepairBooking } from '../../core/models';

@Component({
  selector: 'app-repair-confirm',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div *ngIf="booking() as b" class="container-x py-24 max-w-xl text-center animate-fade-in">
      <div class="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 mx-auto flex items-center justify-center">
        <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M5 13l4 4L19 7"/></svg>
      </div>
      <h1 class="display text-4xl mt-6">Booking received.</h1>
      <p class="mt-3 text-neutral-600">Reference: <span class="font-mono text-ink">{{ b.short_ref }}</span></p>
      <p class="mt-2 text-sm text-neutral-500 max-w-sm mx-auto">We'll contact you on {{ b.phone }} within 2 hours with a quote and next steps.</p>
      <a routerLink="/repairs/status" class="btn-outline mt-8 inline-flex">Check booking status</a>
    </div>
  `,
})
export class RepairConfirmComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  booking = signal<RepairBooking | null>(null);
  ngOnInit() {
    this.route.paramMap.subscribe((p) => {
      const ref = p.get('reference')!;
      this.api.get<RepairBooking>(`/repairs/bookings/${ref}/`).subscribe((b) => this.booking.set(b));
    });
  }
}
