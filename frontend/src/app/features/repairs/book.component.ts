import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { RepairBooking, RepairService } from '../../core/models';

@Component({
  selector: 'app-repair-book',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container-x py-12 max-w-xl">
      <div class="eyebrow">Repairs</div>
      <h1 class="display text-4xl md:text-5xl mt-1">Book a repair</h1>
      <div *ngIf="service() as s" class="mt-2 text-sm text-neutral-500">
        <span class="font-medium text-ink">{{ s.name }}</span> · from {{ s.base_price }} AED · ~{{ s.est_minutes }} min
      </div>

      <form (ngSubmit)="submit()" class="mt-10 grid grid-cols-2 gap-3">
        <div class="col-span-2"><label class="label">Full name</label><input [(ngModel)]="form.name" name="name" required class="input" /></div>
        <div><label class="label">Email</label><input [(ngModel)]="form.email" name="email" type="email" required class="input" /></div>
        <div><label class="label">Phone</label><input [(ngModel)]="form.phone" name="phone" required class="input" /></div>
        <div><label class="label">Device brand</label><input [(ngModel)]="form.device_brand" name="device_brand" required class="input" /></div>
        <div><label class="label">Device model</label><input [(ngModel)]="form.device_model" name="device_model" required class="input" /></div>
        <div class="col-span-2"><label class="label">Describe the issue</label><textarea [(ngModel)]="form.issue" name="issue" required rows="4" class="input"></textarea></div>
        <div class="col-span-2"><label class="label">Preferred drop-off date</label><input [(ngModel)]="form.preferred_drop_off" name="preferred_drop_off" type="date" class="input" /></div>
        <div *ngIf="error()" class="col-span-2 text-red-600 text-sm">{{ error() }}</div>
        <button class="btn-primary col-span-2 h-11 mt-2">Submit booking request</button>
      </form>
    </div>
  `,
})
export class RepairBookComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private auth = inject(AuthService);
  service = signal<RepairService | null>(null);
  // Seeded sample repair enquiry — edit fields to book your own.
  form: any = {
    name: 'Ahmed Karim',
    email: 'ahmed.karim@example.ae',
    phone: '+971501234567',
    device_brand: 'Apple',
    device_model: 'iPhone 13 Pro',
    issue: 'Cracked screen after a drop yesterday — touch works, but display has a diagonal line. No water damage.',
    preferred_drop_off: '',
  };
  error = signal('');

  ngOnInit() {
    const u = this.auth.user();
    if (u) { this.form.email = u.email; this.form.name = u.full_name || u.email.split('@')[0]; }
    this.route.paramMap.subscribe((p) => {
      const slug = p.get('slug');
      if (slug) this.api.get<RepairService>(`/repairs/services/${slug}/`).subscribe((s) => this.service.set(s));
    });
  }

  submit() {
    this.error.set('');
    const payload = { ...this.form, service: this.service()?.id || null };
    this.api.post<RepairBooking>('/repairs/bookings/', payload).subscribe({
      next: (b) => this.router.navigate(['/repairs/confirm', b.reference]),
      error: (e) => this.error.set(e?.error?.detail || 'Booking failed.'),
    });
  }
}
