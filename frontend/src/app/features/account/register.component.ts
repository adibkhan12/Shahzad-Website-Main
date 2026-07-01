import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { environment } from '../../../environments/environment';
import { AuthService } from '../../core/auth.service';
import { CartService } from '../../core/cart.service';

declare global {
  interface Window { google?: any; }
}

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslateModule],
  template: `
    <div class="grid md:grid-cols-2 min-h-[calc(100vh-4rem)]">
      <div class="hidden md:flex bg-ink text-white p-12 flex-col justify-between">
        <div class="eyebrow text-neutral-400">{{ 'brandShort' | translate }}</div>
        <div>
          <h2 class="display text-5xl leading-[0.95] tracking-tight">{{ 'auth.createYour' | translate }}<br/><em class="text-brand-300">{{ 'auth.account' | translate }}</em></h2>
          <p class="mt-6 text-neutral-400 max-w-sm text-sm leading-relaxed">{{ 'auth.signUpHint' | translate }}</p>
        </div>
        <div class="text-xs text-neutral-500">{{ 'auth.noShare' | translate }}</div>
      </div>

      <div class="flex items-center justify-center p-8 md:p-16">
        <div class="w-full max-w-sm">
          <h1 class="display text-3xl md:text-4xl">{{ 'auth.createBtn' | translate }}</h1>
          <p class="text-sm text-neutral-500 mt-2">{{ 'auth.alreadyRegistered' | translate }}
            <a routerLink="/account/login" class="text-ink font-medium hover:underline">{{ 'auth.signIn' | translate }}</a>
          </p>

          <form (ngSubmit)="submit()" class="mt-8 space-y-4">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="label">{{ 'auth.firstName' | translate }}</label>
                <input [(ngModel)]="form.first_name" name="first_name" class="input" />
              </div>
              <div>
                <label class="label">{{ 'auth.lastName' | translate }}</label>
                <input [(ngModel)]="form.last_name" name="last_name" class="input" />
              </div>
            </div>
            <div>
              <label class="label">{{ 'auth.email' | translate }}</label>
              <input type="email" [(ngModel)]="form.email" name="email" required [placeholder]="'auth.emailPlaceholder' | translate" class="input" />
            </div>
            <div>
              <label class="label">{{ 'auth.password' | translate }}</label>
              <input type="password" [(ngModel)]="form.password" name="password" required minlength="8" [placeholder]="'auth.passwordPlaceholder' | translate" class="input" />
            </div>
            <div>
              <label class="label">{{ 'auth.referralSource' | translate }}</label>
              <select [(ngModel)]="form.referral_source" name="referral_source" class="input">
                <option value="">{{ 'auth.selectOne' | translate }}</option>
                <option value="google">{{ 'auth.referralGoogle' | translate }}</option>
                <option value="instagram">{{ 'auth.referralInstagram' | translate }}</option>
                <option value="friend">{{ 'auth.referralFriend' | translate }}</option>
                <option value="other">{{ 'auth.referralOther' | translate }}</option>
              </select>
            </div>
            <input *ngIf="form.referral_source === 'other'" [(ngModel)]="form.referral_other" name="referral_other"
                   [placeholder]="'auth.referralOtherPlaceholder' | translate" class="input" />
            <div *ngIf="error()" class="text-red-600 text-sm">{{ error() }}</div>
            <button [disabled]="loading()" class="btn-primary w-full">
              {{ (loading() ? 'auth.creating' : 'auth.createBtn') | translate }}
            </button>
          </form>

          <div *ngIf="googleClientId" class="my-6 flex items-center gap-3">
            <div class="hairline flex-1"></div>
            <span class="text-xs text-neutral-400 uppercase tracking-wider">{{ 'auth.or' | translate }}</span>
            <div class="hairline flex-1"></div>
          </div>
          <div *ngIf="googleClientId" id="google-btn" class="flex justify-center"></div>
        </div>
      </div>
    </div>
  `,
})
export class RegisterComponent implements OnInit {
  private auth = inject(AuthService);
  private cart = inject(CartService);
  private router = inject(Router);
  form: any = {
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    referral_source: '',
    referral_other: '',
  };
  loading = signal(false);
  error = signal('');
  googleClientId = environment.googleClientId;

  ngOnInit() { if (this.googleClientId) this.loadGoogle(); }

  submit() {
    this.loading.set(true); this.error.set('');
    this.auth.register(this.form).subscribe({
      next: () => {
        this.loading.set(false);
        this.afterAuth();
      },
      error: (e) => {
        this.loading.set(false);
        const body = e?.error || {};
        const msg = Object.values(body).flat().join(' ') || 'Registration failed.';
        this.error.set(msg);
      },
    });
  }

  private loadGoogle() {
    const s = document.createElement('script');
    s.src = 'https://accounts.google.com/gsi/client';
    s.async = true;
    s.onload = () => {
      window.google?.accounts.id.initialize({
        client_id: this.googleClientId,
        callback: (r: any) => this.onGoogle(r.credential),
      });
      window.google?.accounts.id.renderButton(document.getElementById('google-btn'),
        { theme: 'outline', size: 'large', shape: 'pill', width: 320 });
    };
    document.body.appendChild(s);
  }

  onGoogle(idToken: string) {
    this.auth.google(idToken).subscribe({
      next: () => this.afterAuth(),
      error: (e) => this.error.set(e?.error?.detail || 'Google sign-in failed.'),
    });
  }

  private afterAuth() {
    this.cart.mergeAfterLogin().subscribe();
    this.router.navigate(['/account']);
  }
}
