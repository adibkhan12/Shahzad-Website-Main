import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { environment } from '../../../environments/environment';
import { AuthService } from '../../core/auth.service';
import { CartService } from '../../core/cart.service';

declare global {
  interface Window { google?: any; }
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslateModule],
  template: `
    <div class="grid md:grid-cols-2 min-h-[calc(100vh-4rem)]">
      <div class="hidden md:flex bg-ink text-white p-12 flex-col justify-between">
        <div class="eyebrow text-neutral-400">{{ 'brandShort' | translate }}</div>
        <div>
          <h2 class="display text-5xl leading-[0.95] tracking-tight">{{ 'auth.welcomeBack1' | translate }}<br/><em class="text-brand-300">{{ 'auth.welcomeBack2' | translate }}</em></h2>
          <p class="mt-6 text-neutral-400 max-w-sm text-sm leading-relaxed">{{ 'auth.signInHint' | translate }}</p>
        </div>
        <div class="text-xs text-neutral-500">{{ 'auth.trustedSince' | translate }}</div>
      </div>

      <div class="flex items-center justify-center p-8 md:p-16">
        <div class="w-full max-w-sm">
          <h1 class="display text-3xl md:text-4xl">{{ 'auth.signIn' | translate }}</h1>
          <p class="text-sm text-neutral-500 mt-2">{{ 'auth.newHere' | translate }}
            <a routerLink="/account/register" class="text-ink font-medium hover:underline">{{ 'auth.createAccount' | translate }}</a>
          </p>

          <form (ngSubmit)="submit()" class="mt-8 space-y-4">
            <div>
              <label class="label">{{ 'auth.email' | translate }}</label>
              <input type="email" [(ngModel)]="email" name="email" required [placeholder]="'auth.emailPlaceholder' | translate" class="input" />
            </div>
            <div>
              <label class="label">{{ 'auth.password' | translate }}</label>
              <input type="password" [(ngModel)]="password" name="password" required placeholder="••••••••" class="input" />
            </div>
            <div *ngIf="error()" class="text-red-600 text-sm">{{ error() }}</div>
            <button [disabled]="loading()" class="btn-primary w-full">
              {{ (loading() ? 'auth.signingIn' : 'auth.signIn') | translate }}
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
export class LoginComponent implements OnInit {
  private auth = inject(AuthService);
  private cart = inject(CartService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  email = '';
  password = '';
  loading = signal(false);
  error = signal('');
  googleClientId = environment.googleClientId;

  ngOnInit() { if (this.googleClientId) this.loadGoogle(); }

  submit() {
    this.loading.set(true); this.error.set('');
    this.auth.login(this.email, this.password).subscribe({
      next: () => { this.loading.set(false); this.afterLogin(); },
      error: (e) => { this.loading.set(false); this.error.set(e?.error?.detail || 'Login failed.'); },
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
      next: () => this.afterLogin(),
      error: (e) => this.error.set(e?.error?.detail || 'Google sign-in failed.'),
    });
  }

  afterLogin() {
    this.cart.mergeAfterLogin().subscribe();
    const next = this.route.snapshot.queryParamMap.get('next') || '/account';
    this.router.navigateByUrl(next);
  }
}
