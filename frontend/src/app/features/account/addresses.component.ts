import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../core/api.service';
import { Address, Paginated } from '../../core/models';

@Component({
  selector: 'app-addresses',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container-x py-12 max-w-3xl">
      <div class="eyebrow">Account</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-8">Saved addresses</h1>

      <div *ngIf="items().length === 0" class="text-sm text-neutral-500 mb-8">No saved addresses yet.</div>
      <div class="space-y-3">
        <div *ngFor="let a of items()" class="card p-5 flex items-start gap-4">
          <div class="flex-1">
            <div class="flex items-center gap-2">
              <div class="font-medium">{{ a.name }}</div>
              <span *ngIf="a.is_default" class="chip chip-active !py-0.5 !text-[10px]">Default</span>
            </div>
            <div class="text-sm text-neutral-600 mt-1">{{ a.address_line1 }} {{ a.address_line2 }}</div>
            <div class="text-sm text-neutral-600">{{ a.city }} {{ a.postal_code }}, {{ a.country }}</div>
            <div class="text-sm text-neutral-500 mt-1">{{ a.phone }}</div>
          </div>
          <div class="flex flex-col gap-1 text-xs">
            <button *ngIf="!a.is_default" (click)="makeDefault(a)" class="text-neutral-700 hover:text-ink transition">Make default</button>
            <button (click)="remove(a)" class="text-red-600 hover:text-red-700 transition">Delete</button>
          </div>
        </div>
      </div>

      <div class="mt-12">
        <h2 class="display text-2xl mb-5">Add new address</h2>
        <form (ngSubmit)="save()" class="grid grid-cols-2 gap-3">
          <div class="col-span-2"><label class="label">Name</label><input [(ngModel)]="form.name" name="name" required class="input" /></div>
          <div><label class="label">Phone</label><input [(ngModel)]="form.phone" name="phone" class="input" /></div>
          <div><label class="label">Email (optional)</label><input type="email" [(ngModel)]="form.email" name="email" class="input" /></div>
          <div class="col-span-2"><label class="label">Address line 1</label><input [(ngModel)]="form.address_line1" name="address_line1" required class="input" /></div>
          <div class="col-span-2"><label class="label">Address line 2</label><input [(ngModel)]="form.address_line2" name="address_line2" class="input" /></div>
          <div><label class="label">City</label><input [(ngModel)]="form.city" name="city" required class="input" /></div>
          <div><label class="label">Postal code</label><input [(ngModel)]="form.postal_code" name="postal_code" class="input" /></div>
          <div class="col-span-2"><label class="label">Country</label><input [(ngModel)]="form.country" name="country" class="input" /></div>
          <label class="col-span-2 flex items-center gap-2 text-sm"><input type="checkbox" [(ngModel)]="form.is_default" name="is_default" /> Make this my default address</label>
          <button class="btn-primary col-span-2 mt-2">Save address</button>
        </form>
      </div>
    </div>
  `,
})
export class AddressesComponent implements OnInit {
  private api = inject(ApiService);
  items = signal<Address[]>([]);
  // Seeded sample so the "Add address" form renders full; clear fields to save a real one.
  form: any = {
    name: 'Ahmed Karim',
    phone: '+971501234567',
    email: 'ahmed.karim@example.ae',
    address_line1: 'Rolla Square, Al Wahda St',
    address_line2: 'Building 42, Apt 7',
    city: 'Sharjah',
    postal_code: '00000',
    country: 'UAE',
    is_default: true,
  };

  ngOnInit() { this.load(); }
  load() { this.api.get<Paginated<Address>>('/accounts/addresses/').subscribe((r) => this.items.set(r.results || [])); }
  save() {
    this.api.post<Address>('/accounts/addresses/', this.form).subscribe(() => {
      this.form = {
        name: '', phone: '', email: '',
        address_line1: '', address_line2: '',
        city: 'Sharjah', postal_code: '', country: 'UAE',
        is_default: false,
      };
      this.load();
    });
  }
  remove(a: Address) { this.api.delete(`/accounts/addresses/${a.id}/`).subscribe(() => this.load()); }
  makeDefault(a: Address) { this.api.post(`/accounts/addresses/${a.id}/make_default/`, {}).subscribe(() => this.load()); }
}
